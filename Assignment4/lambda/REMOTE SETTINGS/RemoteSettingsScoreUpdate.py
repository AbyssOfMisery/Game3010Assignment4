import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('RemoteSettings')
    if event['httpMethod'] == 'POST':
        if 'body' in event:
            request_text = event['body']
            body = json.loads(request_text)
            if 'GameName' in body and 'Username' in body and 'Score' in body:
                game_name = body['GameName']
                response = table.get_item(Key={'GameName':game_name})
                if 'Item' in response:
                    game_UserName = body['Username']
                    game_Score = body['Score']
                    table.update_item(
                        Key = {
                            'GameName' : game_name
                        },
                        UpdateExpression = 'SET  Username = name , Score = result',
                        ExpressionAttributeValues={
                            'name': game_UserName,
                            'result' : game_Score
                        }
                    )
                    return {
                        'statusCode': 200,
                        'body': 'Update score' + game_name + ' for user '  + game_UserName + ' successed"}'
                    }
                else :
                    return error('This game' + game_name + 'does not exist')
            else:
                return error('You have to add GameName, Username add Score in body massage')
        else :

            return error('You did not sent a body massage')
    else:
        return error('Change your postmane to Get mode')

def error(msg):
    return {
        'statusCode': 200,
        'body': msg
    }

