import json
import datetime 
import boto3
import decimal

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('RemoteSettings')
    if event['httpMethod'] == 'GET':
        if 'queryStringParameters' in event:
            params = event['queryStringParameters']
            if 'GameName' in params:
                game_name = params['GameName']
                response = table.get_item(Key={'GameName':game_name})
                if 'Item' in response:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(response['Item'], cls = CustomJsonEncoder)
                    }
                else :
                    return error('This game ' + game_name + ' does not exist')
            else:
                return error('you have to sent GameName in massage')
        else :
            return error('You did not sent a parameter')
    else:
        return error('Change your postman to Get mode')

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

