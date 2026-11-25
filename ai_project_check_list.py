from dotenv import load_dotenv
import os
import openai
from openai import OpenAI
import logging
import json


logger = logging.getLogger(__name__) #https://allwin-raju.medium.com/python-file-logging-a-step-by-step-filehandler-tutorial-2be24a6e5aa5?sk=3971aca3e9c37b3c702fa6e03807c91e
handler = logging.FileHandler('file.log')  
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s") #https://middleware.io/blog/python-logging-format/
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)



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

    logger.info("Usuário inseriu o texto")
        
    return user_input


def creating_client ():
    client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url=os.environ.get('BASE_URL'),
    timeout=10.0 #https://github.com/openai/openai-python?tab=readme-ov-file#timeouts
)
    logger.info("Cliente acessado")

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
        
        logger.info("Feita a leitura do arquivo json contendo as configurações")
        print(response.output_text)
        logger.info("Resposta gerada")
        
    except openai.BadRequestError as e:
        print(f"Erro 400: Verifique se os parâmetros informados estão corretos ") 
        logger.error(f" {e}")

    except openai.AuthenticationError as e: 
        print(f'Erro 401: Verifique se sua API key está válida ')
        logger.error(f" {e}")

    except openai.PermissionDeniedError as e: 
        print(f"Erro 403: Verifique se seu usuário possui as permissões necessárias")
        logger.error(f" {e}")       
    except openai.NotFoundError as e: 
        print(f"Erro 404: Modelo de llm escolhido não existe ou URL indicada para esse incorreta")
        logger.error(f" {e}")

    except openai.UnprocessableEntityError as e: 
         print(f"Erro 422: Verifique se os parâmetros não estão fora dos padrões")
         logger.error(f" {e}")

    except openai.RateLimitError as e: 
        print(f"Erro 429: Limite de requisições feitas permitidas atingido. Aguarde alguns instantes e tente novamente")
        logger.error(f" {e}")

    except openai.InternalServerError as e: 
         print(f"Error >=500: Serviço temporariamente indisponível. Tente novamente mais tarde")
         logger.error(f" {e}")

    except openai.APITimeoutError as e:
         print('A requisição levou muito tempo para ser completada, isso pode ser devido a problemas de conexão ou sistema sobrecarregado.Tente novamente mais tarde ')
         logger.error(f" {e}")

    except openai.APIConnectionError as e: 
        print(f"Verifique a conexão com a internet e tente novamente mais tarde. Se o problema persistir verifique se há algum erro na configuração do proxy, certificado SSL ou Firewall")
        logger.error(f" {e}")

    except Exception  as e:
        print(f'Houve algum erro: {e} ')
        logger.error(f" {e}")

        
            #https://stackoverflow.com/questions/76363168/openai-api-how-do-i-handle-errors-in-python/ https://github.com/openai/openai-python?tab=readme-ov-file#handling-errors
            #https://developers.openai.com/api/docs/guides/error-codes#python-library-error-types
#
            
calling_llm()