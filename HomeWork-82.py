import json
import boto3
import time

s3 = boto3.client('s3')
bucket = "files-bucke"

def getFormat():
    format = {
        "key": "string",
        "body": "string",
    }
    return format

def handleEmptyPath():
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

def handleCreate(event):
    try:
        data = json.loads(event["body"])
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": "Invalid json input"})   
        }
    try:
        file_name = data["key"]
        file_body = data["body"]
        s3.put_object(
            Bucket=bucket,
            Key=str(time.time()) + "-" + file_name,
            Body=file_body
        )
        return {
            'statusCode': 200,
            'body': json.dumps({"success": "File created"})
        }
    except Exception as e:
        return {
            'statusCode': 404,
            'body': json.dumps({"error": str(e)})
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
    
    if path == "/":
        return handleEmptyPath()
    elif path == "/create":
        if method == "POST":
            return handleCreate(event)
        elif method == "GET":
            return {
                'statusCode': 200,
                'body': json.dumps(getFormat())   
            }
            
    
