import json
import datetime 
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Players')
    if event['httpMethod'] == 'GET':
        if event['queryStringParameters']:
            params = event['queryStringParameters']
            if 'Username' in params and params['Username']:
                user_id = params['Username']
                this_User = table.get_item(Key={'user_id':user_id})
                if 'Item' in this_User:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(this_User['Item'], cls = CustomJsonEncoder)
                    }
                return error('No info is matched')
            else:
                return error('Username did not sent, please add username in params')
        else :

            return error('You have to add username in params in postman')
    else:
        return error('Please change your postman to Get mode')


def error(msg):
    return {
        'statusCode': 200,
        'body': msg
    }
    
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

