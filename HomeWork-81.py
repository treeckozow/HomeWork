import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    buckets_dict = {}
    print("Existing buckets: ")
    for bucket in response["Buckets"]:
        objects = s3.list_objects_v2(Bucket=bucket["Name"])
        if 'Contents' in objects:
            objects_list = []
            for object in objects['Contents']:
                objects_list.append({"Name": object["Key"], "Size": str(object["Size"]) + " bytes"})
            buckets_dict[bucket["Name"]] = objects_list
        else:
            buckets_dict[bucket["Name"]] = "None"
    print(buckets_dict)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
