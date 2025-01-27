import json
import logging
import boto3
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.client("s3")
bucket = "calculator-files"

def checkIfDigit(object):
    try:
        int(object)
        return True
    except:
        return False

def getResultFormat(number_1, number_2, operator):
    number_1 = int(number_1)
    number_2 = int(number_2)
    if operator == "*":
        calculation = number_1 * number_2
    elif operator == "/":
        calculation = number_1 / number_2
    elif operator == "+":
        calculation = number_1 + number_2
    elif operator == "-":
        calculation = number_1 - number_2
    result = str(number_1) + " " + operator + " " + str(number_2) + " = " + str(calculation)
    return {"result": result}  

def getCalculation(number_1, number_2, operator):
    if not checkIfDigit(number_1):
        return {"error": "'" + str(number_1) + "' should be integer but got " + str(type(number_1))}
    if not checkIfDigit(number_2):
        return {"error": "'" + str(number_2) + "' should be integer but got " + str(type(number_2))}
    number_2 = int(number_2)
    if number_2 == 0 and operator == "/":
        return {"error": "Division by zero"}
    
    if operator in {"*", "/", "+", "-"}:
        return getResultFormat(number_1, number_2, operator)
    else:
        return {"error": "Operator '" + str(operator) + "' not supported"}

def getFormat():
    format = {
        "number_1": "int",
        "number_2": "int",
        "operator": "str, within {'*', '/', '+', '-'}"
    }
    return format

def lambda_handler(event, context):
    try:
        method = event["httpMethod"]
        path = event["path"]
    except:
        return {
            'statusCode': 404,
            'body': json.dumps('error')   
        }

    if path == "/":
        logger.info("User tried to log in to path '/'")
        if method == "GET":
            try:
                output = {}
                response = s3.list_objects(Bucket=bucket)
                if "Contents" in response:
                    try:
                        for obj in response["Contents"]:
                            file_name = obj["Key"]
                            file_data = s3.get_object(Bucket=bucket, Key=file_name)
                            output[file_name] = file_data["Body"].read().decode("utf-8")
                    except Exception as e:
                        return {
                            'statusCode': 404,
                            'body': json.dumps("error: " + str(e))
                        }
                return {
                    'statusCode': 200,
                    'body': json.dumps(output)   
                }
            except Exception as e:
                return {
                    'statusCode': 404,
                    'body': json.dumps("error: " + str(e))
                }
    elif path == "/calc":
        if method == "GET":
            return {
                'statusCode': 200,
                'body': json.dumps(getFormat())   
            }
        elif method == "POST":
            try:
                try:
                    data = json.loads(event["body"])
                except:
                    return {
                        'statusCode': 400,
                        'body': json.dumps({"error": "Invalid json input", "format": getFormat()})   
                    }
                num1 = data["number_1"]
                num2 = data["number_2"]
                operator = data["operator"]

                result = getCalculation(num1, num2, operator)

                s3.put_object(
                    Bucket=bucket,
                    Key=str(time.time()),
                    Body=result["result"]
                )

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
            except Exception as e:
                return {
                    'statusCode': 400,
                    'body': json.dumps({"error": "Bad request, " + str(e)})  
                }