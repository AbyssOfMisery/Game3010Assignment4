import json
import datetime 
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')

def LogIn(event, context):
    table = dynamodb.Table('Players')
    # we'll start by saving entries
    if event['httpMethod'] == 'POST':
        if 'body' in event and event['body']:
            body_text = event['body']
            body = json.loads(body_text)
            if 'Password' in body and 'Username' in body :
                if not body['Username']:
                    return error_object('Bad Request - Username cannot be blank')
                if not body['Password']:
                    return error_object('Bad Request - Password cannot be blank')
                user_id = body['Username']
                user_pwd = body['Password']
                this_user = table.get_item(Key={'user_id':user_id})
                if 'Item' in this_user:
                    item = this_user['Item']
                    if item['Password'] == user_pwd:
                        table.update_item(
                            Key = {
                                'user_id' : user_id
                            },
                            UpdateExpression = 'SET LoginDate = :currentDate',
                            ExpressionAttributeValues={
                                ':currentDate':  datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                            }
                        )

                        return {
                            'statusCode': 200,
                            'body': 'User logged in successfully'
                        }
                return error('username or password wrong please check again')
            else:
                return error('Can not find username or password in text')
        else :
      
            return error('no massage in body text')
    else:
        return error('Please change your postman to post mode')

def error(mgs):
    return {
        'statusCode': 200,
        'body': mgs 
    }