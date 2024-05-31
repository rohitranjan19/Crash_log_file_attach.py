import json
import boto3
import os
from email import utils, encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Initialize clients
s3_client = boto3.client('s3')
ses_client = boto3.client('ses', region_name=os.environ['SES_REGION'])

# Environment variables
SENDER_EMAIL = os.environ['SENDER_EMAIL']
RECIPIENT_EMAIL = os.environ['RECIPIENT_EMAIL']

def lambda_handler(event, context):
    try:
        # Log the environment variables for debugging
        print(f"SENDER_EMAIL: {SENDER_EMAIL}")
        print(f"RECIPIENT_EMAIL: {RECIPIENT_EMAIL}")
        print(f"SES_REGION: {os.environ['SES_REGION']}")

        # Get bucket and object key from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Get the object from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read()
        
        # Create the email
        msg = MIMEMultipart()
        msg['Subject'] = 'New Crash Log Uploaded'
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Date'] = utils.formatdate(localtime=True)
        msg['Message-ID'] = utils.make_msgid()
        
        # Email body
        body = MIMEText(f'A new crash log has been uploaded to the bucket {bucket}.\n\nFile name: {key}')
        msg.attach(body)
        
        # Attachment
        attachment = MIMEApplication(file_content)
        attachment.add_header('Content-Disposition', 'attachment', filename=key)
        msg.attach(attachment)
        
        # Send the email
        response = ses_client.send_raw_email(
            Source=SENDER_EMAIL,
            Destinations=[RECIPIENT_EMAIL],
            RawMessage={
                'Data': msg.as_string()
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Email sent successfully!')
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
