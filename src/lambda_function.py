import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Inicializa o cliente do Cognito
    client = boto3.client('cognito-idp')

    user_pool_id = 'us-east-1_wpcoi58H6'  # Substitua pelo seu User Pool ID
    email = event.get('email')  # Assume que o evento inclui 'email'
    password = event.get('password')  # Assume que o evento inclui 'password'

    if not email or not password:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Email and password are required.'})
        }

    try:
        # Busca o usuário pelo email
        filter_string = f'email="{email}"'  # Ajuste conforme o nome do atributo
        response = client.list_users(
            UserPoolId=user_pool_id,
            Filter=filter_string
        )

        # Verifica se o usuário foi encontrado
        if not response['Users']:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found.'})
            }

        # Obtém o username do usuário encontrado
        username = response['Users'][0]['Username']
        print(f"Username found: {username}")

        # Tenta autenticar o usuário
        auth_response = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId='63du3pl8ed26fs5vhofpqeqlah',  # Substitua pelo seu Client ID
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': username,  # Usa o username encontrado
                'PASSWORD': password
            }
        )

        # Retorna a resposta com os tokens de autenticação
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Login successful',
                'accessToken': auth_response['AuthenticationResult']['AccessToken'],
                'expiresIn': auth_response['AuthenticationResult']['ExpiresIn'],
                'tokenType': auth_response['AuthenticationResult']['TokenType'],
            })
        }

    except ClientError as e:
        error_message = str(e)
        print(f"Error: {error_message}")

        # Retorna uma mensagem de erro apropriada
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
        # Captura qualquer outra exceção
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
