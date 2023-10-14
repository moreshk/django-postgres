 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

# Check for relevance of the input essay to the topic
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

# Check for Audience criteria

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
        Keep your response limited to less than 5 sentences and provide a numeric (not range) overall grade.
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


# Check Text structure

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
        Keep your response limited to less than 5 sentences and provide a numeric (not range) overall grade.
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

# Check Ideas

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
        Keep your response limited to less than 5 sentences and provide a numeric (not range) overall grade.
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