import json
import boto3
import os

#sns_client = boto3.client('sns')
#SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    # Extract bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Construct the message
   # message = f"A new crash log has been uploaded to the bucket {bucket_name}.\n\nFile name: {object_key}"
   # subject = "New Crash Log Uploaded"
    
    # Publish the message to the SNS topic
   # response = sns_client.publish(
   #     TopicArn=SNS_TOPIC_ARN,
   #     Subject=subject,
   #     Message=message
   # )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent!')
    }
