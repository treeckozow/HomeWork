import json
import logging
import boto3
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.client("s3")
bucket = "calculator-files"

def getResult(number_1, number_2, operator):
    try:
        number_1 = int(number_1)
    except:
        return {"error": "'" + str(number_1) + "' should be integer but got " + str(type(number_1))}
    try:
        number_2 = int(number_2)
    except:
        return {"error": "'" + str(number_2) + "' should be integer but got " + str(type(number_2))}
    
    if operator == "*":
        calculation = number_1 * number_2
    elif operator == "/":
        if number_2 == 0:
            logger.info("User tried to divide by zero")
            return {"error": "Division by zero"}
        calculation = number_1 / number_2
    elif operator == "+":
        calculation = number_1 + number_2
    elif operator == "-":
        calculation = number_1 - number_2
    else:
        logger.info("User tried to use unsupported operator: " + str(operator))
        return {"error": "Operator '" + str(operator) + "' not supported"}
    
    result = str(number_1) + " " + operator + " " + str(number_2) + " = " + str(calculation)
    saveToBucket(result)
    return {"result": result} 

def saveToBucket(result):
    global bucket
    file_name = str(time.time()) + ".txt"
    s3.put_object(
        Bucket=bucket,
        Key=file_name,
        Body=result
    )
    return file_name

def getFormat():
    format = {
        "number_1": "int",
        "number_2": "int",
        "operator": "str, within {'*', '/', '+', '-'}"
    }
    return format

def getCalculationHistory():
    global bucket
    output = {}
    response = s3.list_objects(Bucket=bucket)
    if "Contents" in response:
        for obj in response["Contents"]:
            file_name = obj["Key"]
            file_data = s3.get_object(Bucket=bucket, Key=file_name)
            output[file_name] = file_data["Body"].read().decode("utf-8")
    return {
        'statusCode': 200,
        'body': json.dumps(output)   
    }

def handleEmptypath(method):
    if method == "GET":
        try:
            return getCalculationHistory()
        except Exception as e:
            logger.warning("An unexpected error has occurred. " + str(e))
            return {
                'statusCode': 400,
                'body': json.dumps("error: " + str(e))
            }
    else:
        logger.info("User tried to use unsupported method: " + str(method))
        return {
            'statusCode': 400,
            'body': json.dumps("error: Method '" + str(method) + "' not supported")
        }

def handleCalcPath(method, event):
    if method == "GET":
        return {
            'statusCode': 200,
            'body': json.dumps(getFormat())   
        }
    elif method == "POST":
        try:
            data = json.loads(event["body"])
        except:
            logger.info("User tried to use unsupported format: " + str(event["body"]))
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Invalid json input", "format": getFormat()})   
            }

        num1 = data["number_1"]
        num2 = data["number_2"]
        operator = data["operator"]
        result = getResult(num1, num2, operator)

        if "result" in result:
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps(result)  
            }
    else:
        logger.info("User tried to use unsupported method: " + str(method))
        return {
            'statusCode': 400,
            'body': json.dumps("error: Method '" + str(method) + "' not supported")
        }
 
def lambda_handler(event, context):
    try:
        method = event["httpMethod"]
        path = event["path"]
    except:
        return {
            'statusCode': 404,
            'body': json.dumps('error')   
        }

    try:
        if path == "/":
            logger.info("User tried to log in to path '/'")
            return handleEmptypath(method)
        elif path == "/calc":
            logger.info("User tried to log in to path '/calc'")
            return handleCalcPath(method, event)
    except Exception as e:
        logger.warning("An unexpected error has occurred. " + str(e))
        return {
            'statusCode': 400,
            'body': json.dumps("error: " + str(e))
        } 