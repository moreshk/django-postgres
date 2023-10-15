 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

# 0. Check for relevance of the input essay to the topic
def check_relevance(user_response, title, description, essay_type, grade):
    print("I am in check relevance")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Your job is to check relevance of the essay with respect to the task title and task description.
        If the essay is completely irrelevant then mention "Provided essay is not relevant to the title and description and cannot be graded further."
        If it is relevant (or has some degree of relevance) then mention "Provided essay input is relevant to the title and description.".
        """,
    )


    chain = LLMChain(llm=llm, prompt=relevance_prompt)

    inputs = {
        "essay": user_response,
        "task_title": title,
        "task_desc": description
    }

    # print(essay_type, title, description)
    feedback_from_api = chain.run(inputs)
    return feedback_from_api

def hello_world():
    return "Hello, World!"

# 1. Check for Audience criteria

def check_audience_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check audience")
    print(essay_type, grade, title, description)
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


# 2. Check Text structure

def check_text_structure_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check text structure")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of text structure (Scored out of 4)

        Grade 3 and Grade 5 criteria: 
        1 Point: The student provides a structure with recognizable components, though transitions might be inconsistent.
        2-3 Points: The student's writing has a clear introduction, body, and conclusion. Transitions between ideas are mostly smooth.
        4 Points: The writing is well-organized with effective transitions, guiding the reader seamlessly through a coherent argument.

        Grade 7 and Grade 9 criteria:
        1 Point: The student's writing has a structure, but it may occasionally lack depth or sophistication in transitions and organization.
        2-3 Points: The student's writing has a clear introduction, body, and conclusion. Transitions between ideas are smooth and enhance the flow, reflecting a deeper understanding of the topic.
        4 Points: The writing is expertly organized with seamless transitions, guiding the reader effortlessly through a well-structured, sophisticated, and nuanced argument.

        Keep in mind the students grade and the essay type. Grade 3 and 5 have the same criteria, Grade 7 and Grade 9 have the same criteria. 
        Be more lenient to the lower grades. So the same essay would score higher if written by a grade 3 vs for grade 5 even if the criteria was same. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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

# 3. Check Ideas

def check_ideas_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check ideas")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Ideas (Scored out of 5)

        Grade 3 and Grade 5 criteria: 
        1-2 Points: The student presents a simple argument or point of view with minimal supporting details.
        3-4 Points: The student's argument is clearer, with some relevant supporting details. The writing may occasionally lack depth or elaboration.
        5 Points: The student presents a well-thought-out argument, supported by relevant and detailed examples or reasons.

        Grade 7 and Grade 9 criteria:
        1-2 Points: The student presents a clear argument with supporting details, but these might occasionally lack originality or depth.
        3-4 Points: The student's argument is robust and demonstrates critical thinking. The writing showcases depth, relevance, and originality in its supporting evidence.
        5 Points: The student presents a comprehensive, insightful, and original argument, bolstered by highly relevant, detailed, and unique examples or reasons.

        Keep in mind the students grade and the essay type. Grade 3 and 5 have the same criteria, Grade 7 and Grade 9 have the same criteria. 
        Be more lenient to the lower grades. So the same essay would score higher if written by a grade 3 vs for grade 5 even if the criteria was same. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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

# 4. Persuasive Devices (Scored out of 4)

def check_persuasive_devices_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check ideas")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Persuasive Devices (Scored out of 4).

        Grade 3 and Grade 5 criteria: 
        1 Point: Some use of persuasive devices, though they may be basic or not always effective.
        2-3 Points: The student uses persuasive devices, such as rhetorical questions, emotive language, or anecdotes, with varying effectiveness.
        4 Points: The student skillfully employs a range of persuasive devices to enhance and strengthen their argument.

        Grade 7 and Grade 9 criteria:
        1 Point: The student employs persuasive devices, but they may lack variety or sophistication.
        2-3 Points: The student uses a diverse range of persuasive devices with consistent effectiveness, demonstrating a deeper understanding of rhetorical techniques.
        4 Points: The student adeptly and creatively uses a diverse range of persuasive devices, masterfully enhancing their argument with sophistication.

        Keep in mind the students grade and the essay type. Grade 3 and 5 have the same criteria, Grade 7 and Grade 9 have the same criteria. 
        Be more lenient to the lower grades. So the same essay would score higher if written by a grade 3 vs for grade 5 even if the criteria was same. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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

# 5. Vocabulary (Scored out of 5)

def check_vocabulary_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check vocabulary")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Vocabulary (Scored out of 5).

        Grade 3 and Grade 5 criteria: 
        1-2 Points: The student uses appropriate vocabulary for their age, though word choice might occasionally be repetitive or imprecise.
        3-4 Points: The student's vocabulary is varied, with words often chosen for effect and clarity.
        5 Points: The student's vocabulary is rich and purposeful, significantly enhancing the persuasive quality of the writing.

        Grade 7 and Grade 9 criteria:
        1-2 Points: The student's vocabulary is appropriate but might occasionally lack precision or sophistication.
        3-4 Points: The student's vocabulary is varied, sophisticated, and often chosen for its effect, enhancing clarity and persuasion.
        5 Points: The student's vocabulary is rich, sophisticated, and purposefully chosen, significantly elevating the persuasive quality of the writing with nuance.

        Keep in mind the students grade and the essay type. Grade 3 and 5 have the same criteria, Grade 7 and Grade 9 have the same criteria. 
        Be more lenient to the lower grades. So the same essay would score higher if written by a grade 3 vs for grade 5 even if the criteria was same. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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

# 6. Cohesion (Scored out of 4)

def check_cohesion_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check cohesion")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Cohesion (Scored out of 4).

        Grade 3 and Grade 5 criteria: 
        1 Point: The student's writing shows some connections between ideas, though these might be basic or unclear at times.
        2-3 Points: Use of referring words, text connectives, and other cohesive devices to link ideas, with occasional lapses.
        4 Points: The student masterfully controls multiple threads and relationships across the text, ensuring a cohesive and unified argument.

        Grade 7 and Grade 9 criteria:
        1 Point: The student's writing shows connections between ideas, but these might lack sophistication.
        2-3 Points: Effective use of advanced cohesive devices to link ideas, demonstrating a deeper understanding of textual flow.
        4 Points: The student expertly controls multiple threads and relationships across the text, ensuring a cohesive, unified, and flowing argument with advanced techniques.

        Keep in mind the students grade and the essay type. Grade 3 and 5 have the same criteria, Grade 7 and Grade 9 have the same criteria. 
        Be more lenient to the lower grades. So the same essay would score higher if written by a grade 3 vs for grade 5 even if the criteria was same. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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

# 7. Paragraphing (Scored out of 2)

def check_paragraphing_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check paragraphing")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Paragraphing (Scored out of 2).

        Grade 3 and Grade 5 criteria: 
        1 Point: The student groups related ideas into paragraphs, though there might be occasional lapses in coherence.
        2 Points: Ideas are effectively and logically grouped into clear paragraphs, enhancing the structure and flow of the argument.

        Grade 7 and Grade 9 criteria:
        1 Point: The student logically groups related ideas into paragraphs, but transitions might occasionally lack depth.
        2 Points: Ideas are effectively and logically grouped into clear paragraphs, enhancing the structure and flow of the argument with sophistication.

        Keep in mind the students grade and the essay type. Grade 3 and 5 have the same criteria, Grade 7 and Grade 9 have the same criteria. 
        Be more lenient to the lower grades. So the same essay would score higher if written by a grade 3 vs for grade 5 even if the criteria was same. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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

# 8. Sentence Structure (Scored out of 6)

def check_sentence_structure_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check Sentence Structure")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Sentence Structure (Scored out of 6).

        Grade 3 and Grade 5 criteria: 
        1-2 Points: The student forms sentences with occasional complexity, though there might be inconsistencies in clarity.
        3-4 Points: The student uses a mix of simple, compound, and some complex sentences, with few errors.
        5-6 Points: The student effectively employs a variety of sentence structures, enhancing the clarity, rhythm, and sophistication of the writing.

        Grade 7 and Grade 9 criteria:
        1-2 Points: The student forms sentences with complexity, but there might be occasional inconsistencies or errors.
        3-4 Points: The student effectively uses a mix of simple, compound, and complex sentences, enhancing clarity and rhythm with more advanced structures.
        5-6 Points: The student masterfully employs a diverse range of sentence structures, adding depth, clarity, and sophistication to the writing with nuance.

        Keep in mind the students grade and the essay type. Grade 3 and 5 have the same criteria, Grade 7 and Grade 9 have the same criteria. 
        Be more lenient to the lower grades. So the same essay would score higher if written by a grade 3 vs for grade 5 even if the criteria was same. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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


# 9. Punctuation (Scored out of 6)
def check_punctuation_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check punctuation")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Punctuation (Scored out of 6).

        Grade 3 and Grade 5 criteria: 
        1-2 Points: The student uses basic and some advanced punctuation with occasional errors.
        3-4 Points: The student correctly uses a range of punctuation, including quotation marks and apostrophes, with few mistakes.
        5-6 Points: Punctuation is used skillfully and accurately throughout the writing, significantly aiding the reader's understanding.

        Grade 7 and Grade 9 criteria:
        1-2 Points: The student uses a mix of basic and advanced punctuation with some errors.
        3-4 Points: The student accurately uses a wide range of punctuation, including more advanced forms, with few mistakes and for stylistic effect.
        5-6 Points: Punctuation is used expertly and accurately throughout the writing, not just for clarity but also for stylistic and rhetorical effect.

        Keep in mind the students grade and the essay type. Grade 3 and 5 have the same criteria, Grade 7 and Grade 9 have the same criteria. 
        Be more lenient to the lower grades. So the same essay would score higher if written by a grade 3 vs for grade 5 even if the criteria was same. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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

# 10. Spelling (Scored out of 6)

def check_spelling_persuasive(user_response, title, description, essay_type, grade):
    print("I am in check spelling")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Spelling (Scored out of 6).

        Grade 3 and Grade 5 criteria: 
        1-2 Points: The student spells most common words correctly, with errors in more challenging or less common words.
        3-4 Points: A majority of words, including challenging ones, are spelled correctly.
        5-6 Points: The student demonstrates an excellent grasp of spelling across a range of word types, with errors being very rare.

        Grade 7 and Grade 9 criteria:
        1-2 Points: The student spells most words correctly but may have errors with complex or specialized words.
        3-4 Points: A vast majority of words, including complex and specialized ones, are spelled correctly.
        5-6 Points: The student demonstrates an impeccable grasp of spelling across a diverse range of word types, including advanced and specialized vocabulary.

        Keep in mind the students grade and the essay type. Grade 3 and 5 have the same criteria, Grade 7 and Grade 9 have the same criteria. 
        Be more lenient to the lower grades. So the same essay would score higher if written by a grade 3 vs for grade 5 even if the criteria was same. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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

# 11. Narrative Audience (Scored out of 6)

def check_audience_narrative(user_response, title, description, essay_type, grade):
    print("I am in audience narrative")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Audience (Scored out of 6).
        Scoring guide: 
        0 - symbols or drawings which have the intention of conveying meaning.
        1 - response to audience needs is limited • contains simple written content. may be a title only OR • meaning is difficult to access OR • copied stimulus material, including prompt topic
        2 - shows basic awareness of audience expectations through attempting to orient the reader • provides some information to support reader understanding. may include simple narrative markers, e.g. – simple title – formulaic story opening: Long, long ago …; Once a boy was walking when … • description of people or places • reader may need to fill gaps in information • text may be short but is easily read.
        3 - orients the reader with an internally consistent story that attempts to support the reader by developing a shared understanding of context • contains sufficient information for the reader to follow the story fairly easily
        4 - supports reader understanding AND • begins to engage the reader
        5 - supports and engages the reader through deliberate choice of language and use of narrative devices.
        6 - caters to the anticipated values and expectations of the reader • influences or affects the reader through precise and sustained choice of language and use of narrative devices

        Keep in mind the students grade and the essay type. Be more lenient to the lower grades and stricter with higher grades in your scoring. 
        Even though all grades have the same criteria, the same essay would score higher if written by a grade 3 vs a grade 5. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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


# Criteria 2. Text structure: The organisation of narrative features including orientation, complication and resolution into an appropriate and effective text structure. 
# Score Range: 0-4 
# Scoring guide: 
# 0- no evidence of any structural components of a times equenced text • symbols or drawings • inappropriate genre, e.g. a recipe, argument • title only
# 1- minimal evidence of narrative structure, e.g. a story beginning only or a ‘middle’ with no orientation • a recount of events with no complication • note that not all recounts are factual • may be description
# 2- contains a beginning and a complication • where a resolution is present it is weak, contrived or ‘tacked on’ (e.g. I woke up, I died, They lived happily ever after) • a complication presents a problem to be solved, introduces tension, and requires a response. It drives the story forward and leads to a series of events or responses • complications should always be read in context • may also be a complete story where all parts of the story are weak or minimal (the story has a problem to be solved but it does not add to the tension or excitement).
# 3 - contains orientation, complication and resolution • detailed longer text may resolve one complication and lead into a new complication or layer a new complication onto an existing one rather than conclude
# 4- coherent, controlled and complete narrative, employing effective plot devices in an appropriate structure, and including an effective ending. sophisticated structures or plot devices include: – foreshadowing/flashback – red herring/cliffhanger – coda/twist – evaluation/reflection – circular/parallel plots


# Criteria 2. Text structure: The organisation of narrative features including orientation, complication and resolution into an appropriate and effective text structure. 
# Score Range: 0-4 
# Scoring guide: 
# 0- no evidence of any structural components of a times equenced text • symbols or drawings • inappropriate genre, e.g. a recipe, argument • title only
# 1- minimal evidence of narrative structure, e.g. a story beginning only or a ‘middle’ with no orientation • a recount of events with no complication • note that not all recounts are factual • may be description
# 2- contains a beginning and a complication • where a resolution is present it is weak, contrived or ‘tacked on’ (e.g. I woke up, I died, They lived happily ever after) • a complication presents a problem to be solved, introduces tension, and requires a response. It drives the story forward and leads to a series of events or responses • complications should always be read in context • may also be a complete story where all parts of the story are weak or minimal (the story has a problem to be solved but it does not add to the tension or excitement).
# 3 - contains orientation, complication and resolution • detailed longer text may resolve one complication and lead into a new complication or layer a new complication onto an existing one rather than conclude
# 4- coherent, controlled and complete narrative, employing effective plot devices in an appropriate structure, and including an effective ending. sophisticated structures or plot devices include: – foreshadowing/flashback – red herring/cliffhanger – coda/twist – evaluation/reflection – circular/parallel plots


# Criteria 2. Text structure: The organisation of narrative features including orientation, complication and resolution into an appropriate and effective text structure. 
# Score Range: 0-4 
# Scoring guide: 
# 0- no evidence of any structural components of a times equenced text • symbols or drawings • inappropriate genre, e.g. a recipe, argument • title only
# 1- minimal evidence of narrative structure, e.g. a story beginning only or a ‘middle’ with no orientation • a recount of events with no complication • note that not all recounts are factual • may be description
# 2- contains a beginning and a complication • where a resolution is present it is weak, contrived or ‘tacked on’ (e.g. I woke up, I died, They lived happily ever after) • a complication presents a problem to be solved, introduces tension, and requires a response. It drives the story forward and leads to a series of events or responses • complications should always be read in context • may also be a complete story where all parts of the story are weak or minimal (the story has a problem to be solved but it does not add to the tension or excitement).
# 3 - contains orientation, complication and resolution • detailed longer text may resolve one complication and lead into a new complication or layer a new complication onto an existing one rather than conclude
# 4- coherent, controlled and complete narrative, employing effective plot devices in an appropriate structure, and including an effective ending. sophisticated structures or plot devices include: – foreshadowing/flashback – red herring/cliffhanger – coda/twist – evaluation/reflection – circular/parallel plots


# Criteria 2. Text structure: The organisation of narrative features including orientation, complication and resolution into an appropriate and effective text structure. 
# Score Range: 0-4 
# Scoring guide: 
# 0- no evidence of any structural components of a times equenced text • symbols or drawings • inappropriate genre, e.g. a recipe, argument • title only
# 1- minimal evidence of narrative structure, e.g. a story beginning only or a ‘middle’ with no orientation • a recount of events with no complication • note that not all recounts are factual • may be description
# 2- contains a beginning and a complication • where a resolution is present it is weak, contrived or ‘tacked on’ (e.g. I woke up, I died, They lived happily ever after) • a complication presents a problem to be solved, introduces tension, and requires a response. It drives the story forward and leads to a series of events or responses • complications should always be read in context • may also be a complete story where all parts of the story are weak or minimal (the story has a problem to be solved but it does not add to the tension or excitement).
# 3 - contains orientation, complication and resolution • detailed longer text may resolve one complication and lead into a new complication or layer a new complication onto an existing one rather than conclude
# 4- coherent, controlled and complete narrative, employing effective plot devices in an appropriate structure, and including an effective ending. sophisticated structures or plot devices include: – foreshadowing/flashback – red herring/cliffhanger – coda/twist – evaluation/reflection – circular/parallel plots

# 12. Narrative Text Structure (0 - 4)

def check_text_structure_narrative(user_response, title, description, essay_type, grade):
    print("I am in text structure narrative")
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    relevance_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc", "grade", "essay_type"],
        template="""You are an essay grader for Naplan. Your inputs are

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Students Grade: {grade}

        Essay Type: {essay_type}

        Your task is to grade the provided essay on the criteria of Text Structure (Scored out of 4).
        Scoring guide: 
        0 - no evidence of any structural components of a times equenced text • symbols or drawings • inappropriate genre, e.g. a recipe, argument • title only
        1 - minimal evidence of narrative structure, e.g. a story beginning only or a `middle` with no orientation • a recount of events with no complication • note that not all recounts are factual • may be description
        2 - contains a beginning and a complication • where a resolution is present it is weak, contrived or `tacked on` (e.g. I woke up, I died, They lived happily ever after) • a complication presents a problem to be solved, introduces tension, and requires a response. It drives the story forward and leads to a series of events or responses • complications should always be read in context • may also be a complete story where all parts of the story are weak or minimal (the story has a problem to be solved but it does not add to the tension or excitement).
        3 - contains orientation, complication and resolution • detailed longer text may resolve one complication and lead into a new complication or layer a new complication onto an existing one rather than conclude
        4 - coherent, controlled and complete narrative, employing effective plot devices in an appropriate structure, and including an effective ending. sophisticated structures or plot devices include: - foreshadowing/flashback - red herring/cliffhanger - coda/twist - evaluation/reflection - circular/parallel plots

        Keep in mind the students grade and the essay type. Be more lenient to the lower grades and stricter with higher grades in your scoring. 
        Even though all grades have the same criteria, the same essay would score higher if written by a grade 3 vs a grade 5. Same for grade 7 vs grade 9.
        Provide feedback on the input essay in terms of what if anything was done well and what can be improved. Try to include examples.
        Keep your response limited to less than 5 sentences and format your response as Feedback: (your feedback) Grade: (your grade)/(Scored out of).
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
