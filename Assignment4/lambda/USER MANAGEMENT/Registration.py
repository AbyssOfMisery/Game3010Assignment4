import json
import datetime 
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Players')
    if event['httpMethod'] == 'PUT':
        if 'body' in event:
            raw_text = event['body']
            body = json.loads(raw_text)
            if 'Username' in body and 'Email' in body and 'Password' in body and body['Username'] and body['Email'] and body['Password']:
                user_id = body['Username']
                userNameCheck = table.get_item(Key={'user_id':user_id})
     
                new_user = {
                    'user_id' : body['Username'],
                    'Password': body['Password'],
                    'Email': body['Email'],
                }
                table.put_item(
                    Item = new_user
                )
                return {
                    'statusCode': 200,
                    'body': 'User registered successfully'
                }
            else:
                return error('Body doesnt have username, password or email')
        else :
            return error('You send a body info ')        
    else:
        return error('Change your postman to put mode and send username, password and email inside body')

def error(msg):
    return {
        'statusCode': 200,
        'body': msg
    }
