from django.shortcuts import render

# Create your views here.
# translator/views.py

from django.http import HttpResponse
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import os
import json

def random_sentence(request):
    llm = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")
    template = "Generate a random sentence with the input: {input_param}."
    prompt_template = PromptTemplate(input_variables=["input_param"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    result = chain.run({"input_param": "some value"})
    return render(request, 'translator/random_sentence.html', {'sentence': result})