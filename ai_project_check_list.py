from dotenv import load_dotenv
import os
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
        
    except Exception as error_catch:
        if '401' in str(error_catch): #https://api-docs.deepseek.com/quick_start/error_codes
            print('Houve um erro de autenticação - favor verificar sua key')
            
        else:
            print(f'Houve algum outro erro: {error_catch}')
            
creating_client()
calling_llm()