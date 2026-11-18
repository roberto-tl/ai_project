from dotenv import load_dotenv
import os
import openai
from openai import OpenAI
import logging



load_dotenv()

def user_input_func ():
    user_message_when_none = 'You must insert a text to continue: '
    user_message_when_type_dif_text = 'Text only: '
    user_input = input('Insert a text to create a checklist:')
    while len(user_input) == 0 :
        user_input = input(user_message_when_none)
        
    if type(user_input) != str:
        user_input = input(user_message_when_type_dif_text)
        
    return user_input

def creating_client ():
    client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com",
    timeout=10.0 #https://github.com/openai/openai-python?tab=readme-ov-file#timeouts
)

    return client

def calling_llm():
    try:
        client_func_return = creating_client()
        response = client_func_return.chat.completions.create(
            model="deepseek-flash",
            messages=[
                {"role": "system", "content": "change the user input into a checklist. when its able for this. Use emojis and squares at the beginning to make easier for read when the constraints are c."},
                {"role": "system", "content": "the content must be something that is able to create a check list, not all the text inserted are able for this. It must contain itens like recipes, shopping list for example and not questions"},
                {"role": "user", "content": user_input_func()},], 
            stream=False,
            reasoning_effort="low"
            )
        print(response.choices[0].message.content)
        
    #https://stackoverflow.com/questions/76363168/openai-api-how-do-i-handle-errors-in-python/ https://github.com/openai/openai-python?tab=readme-ov-file#handling-errors
    #https://developers.openai.com/api/docs/guides/error-codes#python-library-error-types
    
    except openai.BadRequestError as e:
        print(f"Erro 400: Verifique se os parâmetros informados estão corretos ") 
    except openai.AuthenticationError as e: 
        print(f'Erro 401: Verifique se sua API key está válida ')
    except openai.PermissionDeniedError as e: 
        print(f"Erro 403: Verifique se seu usuário possui as permissões necessárias")        
    except openai.NotFoundError as e: 
        print(f"Erro 404: Modelo de llm escolhido não existe ou URL indicada para esse incorreta")
    except openai.UnprocessableEntityError as e: 
        print(f"Erro 422: Verifique se os parâmetros não estão fora dos padrões")
    except openai.RateLimitError as e: 
        print(f"Erro 429: Limite de requisições feitas permitidas atingido. Aguarde alguns instantes e tente novamente")
    except openai.InternalServerError as e: 
        print(f"Error >=500: Serviço temporariamente indisponível. Tente novamente mais tarde")
    except openai.APITimeoutError as e:
        print('A requisição levou muito tempo para ser completada, isso pode ser devido a problemas de conexão ou sistema sobrecarregado.Tente novamente mais tarde ')
    except openai.APIConnectionError as e: 
        print(f"Verifique a conexão com a internet e tente novamente mais tarde. Se o problema persistir verifique se há algum erro na configuração do proxy, certificado SSL ou Firewall")

            
creating_client()
calling_llm()