import json
import datetime 
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')

def logOut(event, context):
    table = dynamodb.Table('Players')
    if event['httpMethod'] == 'GET':
        if event['queryStringParameters']:
            params = event['queryStringParameters']
            if 'Username' in params :
                currentUserName = params['Username']
                UserName = table.get_item(Key={'user_id':currentUserName})
                if 'Item' in UserName:
                    updateInfo(currentUserName)
                    return {
                        'statusCode': 200,
                        'body': '' + currentUserName +' has logged out the game'
                    }
                return error('user did not find')
            else:
                return error('did not fine username in body')
        else :
            return error('you did not send a queryStringParameters')
    else:
        return error('Change your postman to Get mode')

def error(msg):
    return {
        'statusCode': 200,
        'body': msg
    }
    
def updateInfo(user_name):
table = dynamodb.Table('Players')
table.update_item(
    Key = {
        'user_id' : user_name
    },
    UpdateExpression = 'SET logOutDate = currentDate',
    ExpressionAttributeValues={
        'currentDate':  datetime.datetime.now().strftime("%Y,%m,%d,%H,%M,%S"),
    }
)

    