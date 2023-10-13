 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

def check_relevance(user_response, title, description, essay_type, grade):
    print(essay_type, grade, title, description)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

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