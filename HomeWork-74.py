import json

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
        return {
            'statusCode': 404,
            'body': json.dumps('Empty path not supported')   
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