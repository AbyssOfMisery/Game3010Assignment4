import json
import datetime 
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Players')
    if event['httpMethod'] == 'POST':
        if 'body' in event:
            request_text = event['body']
            body = json.loads(request_text)
            if 'Username' in body and 'Email' in body and 'Password' in body and body['Username'] and body['Email'] and body['Password']:
                user_id = body['Username']
                this_user = table.get_item(Key={'user_id':user_id})
                if 'Item' in this_user:
                    table.update_item(
                        Key = {
                            'user_id' : user_id
                        },
                        UpdateExpression = 'SET Email = :email, Password = :password',
                        ExpressionAttributeValues={
                            ':email': body['Email'],
                            ':password':  body['Password'],
                        }
                    )

                    return {
                        'statusCode': 200,
                        'body': 'User info updated'
                    }
                else:
                    return error('This User isn not registered')
            else:
                return error('body raw text does not have Username, Password or Email')
        else :
            # BAD Request
            return error('no body massage is send')
    else:
        return error('Change your postman to post mode')


def error(msg):
    return {
        'statusCode': 200,
        'body': msg
    }