from langchain_core.tools import tool,InjectedToolArg
from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq
import requests
import json
from typing import Annotated
from dotenv import load_dotenv

load_dotenv()

@tool
def get_conversion_rate(base_currency:str,target_currency:str)->int:
    '''you are a langchain currency conversion tool you have to you have to fatch factor of two currency
    '''
    url=f'https://v6.exchangerate-api.com/v6/57415b607000f4123643143a/pair/{base_currency}/{target_currency}'
    response=requests.get(url)
    return response.json()
# print(get_conversion_rate.args)

@tool
def multifly(base_currency_value:int,conversion_rate:Annotated[float,InjectedToolArg])->float:
    '''you have to multiply the base_currency_value with the conversion rate'''
    return base_currency_value*conversion_rate

llm=ChatGroq(model='openai/gpt-oss-120b',temperature=0.2)
# tool binding process
llm_with_tools=llm.bind_tools([get_conversion_rate,multifly])
quary=[HumanMessage('give me the conversion rate of 10 USD to PKR')]

ai_message=llm_with_tools.invoke(quary)

quary.append(ai_message)

# excution of tool and conversion rate
conversion_rate=None
while ai_message.tool_calls:
    for tool_call in ai_message.tool_calls:
        if tool_call['name']==get_conversion_rate.name:
            tool_message1=get_conversion_rate.invoke(tool_call)
            # 
            conversion_rate=json.loads(tool_message1.content)['conversion_rate']
            quary.append(tool_message1)
        elif tool_call['name']==multifly.name:
            tool_call['args']['conversion_rate']=conversion_rate
            tool_message2=multifly.invoke(tool_call)
            quary.append(tool_message2)
    ai_message=llm_with_tools.invoke(quary)
    quary.append(ai_message)
print(ai_message.content)





