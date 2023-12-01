# translator/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from .forms import TranslationForm
import os
import json
from .models import Translation

@login_required
def random_sentence(request):
    llm = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")
    template = "Generate a random sentence with respect to the following: {input_param}."
    prompt_template = PromptTemplate(input_variables=["input_param"], template=template)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    result = chain.run({"input_param": "stock trading technical or fundamental analysis"})
    
    sentence = result

    if request.method == 'POST':
        form = TranslationForm(request.POST)
        if form.is_valid():
            translation = form.save(commit=False)
            translation.user = request.user
            translation.english_text = sentence
            translation.status = 'Submitted'
            translation.save()
            return redirect('random_sentence')
    else:
        form = TranslationForm(initial={'translated_language': request.user.language})

    return render(request, 'translator/random_sentence.html', {'sentence': sentence, 'form': form})


@login_required
def user_translations(request):
    translations = Translation.objects.filter(user=request.user)
    return render(request, 'translator/user_translations.html', {'translations': translations})
