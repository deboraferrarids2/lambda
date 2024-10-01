import json

def lambda_handler(event, context):
    # Obtém o CPF do corpo da requisição
    body = json.loads(event['body'])
    cpf = body.get('cpf')
    
    # Lógica de autenticação (simulada)
    if cpf == "123.456.789-00":  # Exemplo de CPF "válido"
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Autenticação bem-sucedida',
                'cpf': cpf
            })
        }
    else:
        return {
            'statusCode': 401,
            'body': json.dumps({
                'message': 'CPF não encontrado ou inválido'
            })
        }
