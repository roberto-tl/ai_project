from dotenv import load_dotenv
import os
import openai
from openai import OpenAI
import logging
import json




load_dotenv()

def config_json_func():
    with open("config.json") as j:
        json_config=json.load(j)

    return json_config

    
def user_input_func (): #CAPTURA DA ENTRADA
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
    base_url=os.environ.get('BASE_URL'),
    timeout=10.0 #https://github.com/openai/openai-python?tab=readme-ov-file#timeouts
)

    return client
def calling_llm():
    try:
        client_func_return = creating_client()
        response = client_func_return.responses.create( #
            model=config_json_func()["configs"]["model"],
            reasoning={"effort": config_json_func()["configs"]["effort"]},
            max_output_tokens = config_json_func()["configs"]["max_output_token"],
            stream=config_json_func()["configs"]["stream"],
            temperature=config_json_func()["configs"]["temperature"],
            input=[
                {"role": "system", "content": config_json_func()["configs"]["role_system_content"]},
                {"role": "user", "content": user_input_func()},], #https://platform.openai.com/docs/guides/text#message-roles-and-instruction-following 
            )
        print(response.output_text)
        
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
    except Exception  as e:
        print(f'Houve algum erro: {e} ')
        
            #https://stackoverflow.com/questions/76363168/openai-api-how-do-i-handle-errors-in-python/ https://github.com/openai/openai-python?tab=readme-ov-file#handling-errors
            #https://developers.openai.com/api/docs/guides/error-codes#python-library-error-types
#
            
calling_llm()