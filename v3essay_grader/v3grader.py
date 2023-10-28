 
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from spellchecker import SpellChecker
import requests
import re
import os
from dotenv import load_dotenv
from .models import Rubric, Criteria
load_dotenv()

# 0. Check for relevance of the input essay to the topic
def check_relevance(user_response, title, description, essay_type, grade):
    print("I am in check relevance")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Essay Type: {essay_type}

        Your job is to check relevance of the essay with respect to the task title and task description and essay type.
        If the essay is completely irrelevant then mention "Provided input is not relevant to the title and description and cannot be graded further."
        If it is relevant (or has some degree of relevance) then mention "Provided input is relevant to the title and description.".
        """,
    )


    chain = LLMChain(llm=llm, prompt=relevance_prompt)

    inputs = {
        "essay": user_response,
        "task_title": title,
        "task_desc": description,
        "essay_type": essay_type,
    }

    # print(essay_type, title, description)
    feedback_from_api = chain.run(inputs)
    return feedback_from_api



# 1. Check for Audience criteria

def check_criteria(user_response, title, description, essay_type, grade, rubric_id):
    print("I am in check criteria internal function")
    # print("Rubric id: ", rubric_id)
    # print(essay_type, grade, title, description)

# Fetch the Rubric instance with the given rubric_id
    rubric = Rubric.objects.get(id=rubric_id)

    # Fetch the Criteria instances related to the Rubric instance
    criteria_set = Criteria.objects.filter(rubric=rubric)

    # Create a list to store the dataset
    dataset = []

    # Iterate over the Criteria instances
    for criteria in criteria_set:
        # Create a dictionary with the Rubric and Criteria data
        data = {
            'rubric_name': rubric.name,
            'state': rubric.state,
            'city': rubric.city,
            'school': rubric.school,
            'essay_type': rubric.essay_type,
            'grade': rubric.grade,
            'curriculum': rubric.curriculum,
            # 'created_at': rubric.created_at,
            'criteria_name': criteria.criteria_name,
            'max_score': criteria.max_score,
            'criteria_desc': criteria.criteria_desc,
            'spell_check': criteria.spell_check,
        }

        # Add the dictionary to the dataset
        dataset.append(data)

    # Print the dataset
    print(dataset)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Audience (Scored out of 6)

        Grade 3 and Grade 5 criteria: 
        1-2 Points: The student shows an awareness of the reader but may not consistently engage or persuade throughout the piece.
        3-4 Points: The student engages the reader with a clear intent to persuade. The tone is mostly consistent, and the reader's interest is maintained.
        5-6 Points: The student effectively engages, orients, and persuades the reader throughout, demonstrating a strong connection with the audience.

        Grade 7 and Grade 9 criteria:
        1-2 Points: The student demonstrates an understanding of the reader but may occasionally lack depth in engagement or persuasion.
        3-4 Points: The student consistently engages the reader, demonstrating a mature intent to persuade with a nuanced and consistent tone.
        5-6 Points: The student masterfully engages, orients, and persuades the reader, showcasing a sophisticated and insightful connection with the audience.

        Keep in mind the students grade and the essay type. Grade 3 and 5 have the same criteria, Grade 7 and Grade 9 have the same criteria. 
        Be more lenient to the lower grades. So the same essay would score higher if written by a grade 3 vs for grade 5 even if the criteria was same. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
        Remember that your grade cannot exceed 6.
 """,
    )


    chain = LLMChain(llm=llm, prompt=relevance_prompt)

    inputs = {
        "essay": user_response,
        "task_title": title,
        "task_desc": description,
        "grade": grade,
        "essay_type": essay_type,
    }

    # print(essay_type, title, description)
    feedback_from_api = chain.run(inputs)
    print(feedback_from_api)
    return feedback_from_api



# Spell check using BING API

def spell_check(text):
    print("I am in Bing Spell check")
    subscription_key = os.environ.get('BING_SPELLCHECK_KEY')

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Ocp-Apim-Subscription-Key": subscription_key,
    }
    
    endpoint_url = "https://api.bing.microsoft.com/v7.0/spellcheck"
    text_to_check = text.replace('\n', ' ').replace('\r', ' ')

    data = {
        "text": text_to_check,
        "mode": "proof",  # Use 'proof' mode for comprehensive checks
    }

    response = requests.post(endpoint_url, headers=headers, data=data)
    
    output = ""  # Initialize the output string

    if response.status_code == 200:
        result = response.json()
        for flagged_token in result.get('flaggedTokens', []):
            token = flagged_token['token']
            for suggestion in flagged_token.get('suggestions', []):
                suggested_token = suggestion['suggestion']
                if suggested_token.replace(token, '').strip() in ["", ":", ";", ",", ".", "?", "!"]:
                    continue
                if " " not in suggested_token:
                    output += f"Misspelled word: {token}\n"
                    output += f"Suggestion: {suggested_token}\n"
    else:
        output += f"Error: {response.status_code}\n"
        output += response.text + "\n"

    # If no mistakes were found, update the output to indicate this.
    if not output:
        output = "No spelling mistakes found"

    print("Response from Bing Spell check:", output)
    return output

# 10. Spelling (Scored out of 6)
def check_spelling_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check spelling")
    print(essay_type, grade, title, description)

    spell_check_response = spell_check(user_response);

    # Making a second run to generate the grading

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    verification_prompt = PromptTemplate(
        input_variables=["essay", "mistakes", "grade"],
        template="""You are an spelling grader verifier for Naplan. Your inputs are

        Essay: {essay}

        Spelling mistakes: {mistakes}

        Students Grade: {grade}

        Another grader has already done the work of finding the spelling mistakes in the essay.

        You will then grade the essay on spellings using the below criteria.

        Grade 3 and Grade 5 criteria: 
        1-2 Points: The student spells most common words correctly, with errors in more challenging or less common words.
        3-4 Points: A majority of words, including challenging ones, are spelled correctly.
        5-6 Points: The student demonstrates an excellent grasp of spelling across a range of word types, with errors being very rare.

        Grade 7 and Grade 9 criteria:
        1-2 Points: The student spells most words correctly but may have errors with complex or specialized words.
        3-4 Points: A vast majority of words, including complex and specialized ones, are spelled correctly.
        5-6 Points: The student demonstrates an impeccable grasp of spelling across a diverse range of word types, including advanced and specialized vocabulary.

        In feedback also mention your reasoning behind the grade you assign and be generous in your grading if no spelling mistakes were received as input.
        Format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
        """,
    )

    chain = LLMChain(llm=llm, prompt=verification_prompt)

    inputs = {
        "essay": user_response,
        "mistakes": spell_check_response,
        "grade": grade,
    }

    # print(essay_type, title, description)
    second_feedback = chain.run(inputs)
    print("second run", second_feedback)

    return second_feedback

