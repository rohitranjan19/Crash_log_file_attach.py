import json
import boto3
import os
import email
import email.utils
import email.mime.application

# Initialize clients
s3_client = boto3.client('s3')
ses_client = boto3.client('ses')

# Environment variables
SENDER_EMAIL = os.environ['SENDER_EMAIL']
RECIPIENT_EMAIL = os.environ['RECIPIENT_EMAIL']
SES_REGION = os.environ['SES_REGION']

def lambda_handler(event, context):
    try:
        # Get bucket and object key from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Get the object from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read()
        
        # Create the email
        msg = email.mime.multipart.MIMEMultipart()
        msg['Subject'] = 'New Crash Log Uploaded'
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Date'] = email.utils.formatdate(localtime=True)
        msg['Message-ID'] = email.utils.make_msgid()
        
        # Email body
        body = email.mime.text.MIMEText(f'A new crash log has been uploaded to the bucket {bucket}.\n\nFile name: {key}')
        msg.attach(body)
        
        # Attachment
        attachment = email.mime.application.MIMEApplication(file_content)
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
