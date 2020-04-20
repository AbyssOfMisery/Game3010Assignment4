import json
import boto3
import decimal

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('MatchResult')
    if event['httpMethod'] == 'GET':
        if 'queryStringParameters' in event:
            params = event['queryStringParameters']
            print(params)
            if 'GameName' in params and 'Username' in params:
                game_name = params['GameName']
                user_name = params['Username']
                response = table.get_item(Key={'Username':user_name})
                if 'Item' in response:
                    item  = response['Item']
                    return {
                        'statusCode': 200,
                        'body': json.dumps(item,  cls = CustomJsonEncoder)
                    }
                else :
                    return error('This game history does not exist')
            else:
                return error('Need to sent Gamename and Username in the massage')
        else :
         
            return error('You have to active parameter in postman')
    else:
        return error('Change your postman in get mode')
        

def error(msg):
    return {
        'statusCode': 200,
        'body':  msg 
    }

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)
import json
import boto3
import decimal

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('MatchResult')
    if event['httpMethod'] == 'GET':
        if 'queryStringParameters' in event:
            params = event['queryStringParameters']
            print(params)
            if 'GameName' in params and 'Username' in params:
                game_name = params['GameName']
                user_name = params['Username']
                response = table.get_item(Key={'Username':user_name})
                if 'Item' in response:
                    item  = response['Item']
                    return {
                        'statusCode': 200,
                        'body': json.dumps(item,  cls = CustomJsonEncoder)
                    }
                else :
                    return error('This game history does not exist')
            else:
                return error('Need to sent Gamename and Username in the massage')
        else :
         
            return error('You have to active parameter in postman')
    else:
        return error('Change your postman in get mode')
        

def error(msg):
    return {
        'statusCode': 200,
        'body':  msg 
    }

class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)
