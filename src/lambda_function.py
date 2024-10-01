import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')

    user_pool_id = 'us-east-1_wpcoi58H6' 
    email = event.get('email')
    password = event.get('password') 

    if not email or not password:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Email and password are required.'})
        }

    try:
        response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId='63du3pl8ed26fs5vhofpqeqlah', 
            AuthFlow='ADMIN_NO_SRP_AUTH', 
            AuthParameters={
                'USERNAME': email, 
                'PASSWORD': password
            }
        )

        # Retorna a resposta com os tokens de autenticação
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Login successful',
                'accessToken': response['AuthenticationResult']['AccessToken'],
                'expiresIn': response['AuthenticationResult']['ExpiresIn'],
                'tokenType': response['AuthenticationResult']['TokenType'],
            })
        }

    except ClientError as e:
        error_message = str(e)
        print(f"Error: {error_message}")

        if "NotAuthorizedException" in error_message:
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Invalid email or password.'})
            }
        return {
            'statusCode': 500,
            'body': json.dumps({'message': error_message})
        }
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
