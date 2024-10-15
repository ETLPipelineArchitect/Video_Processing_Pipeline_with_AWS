import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Retrieve video metadata
        response = s3.head_object(Bucket=bucket, Key=key)
        metadata = {
            'video_key': key,
            'content_type': response['ContentType'],
            'content_length': response['ContentLength']
        }
        
        # Save metadata to S3
        metadata_key = f'metadata/{key.split('/')[-1].split('.')[0]}.json'
        s3.put_object(
            Bucket='your-bucket',
            Key=metadata_key,
            Body=json.dumps(metadata)
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Metadata extraction complete.')
    }