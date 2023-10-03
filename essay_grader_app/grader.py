 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

def grade_essay(user_response, title, description, exam_type, essay_type, grade):
    print(exam_type, essay_type, grade)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc"],
        template="""You are an essay grader for IELTS Writing Task 2. Your criteria for grading is how well the provided essay fulfils the requirements of the task, 
        including whether it has addressed all parts of the task description and provided a clear position. 
        The key points for your grading are:
        1. Does the essay address all parts of the prompt (task and task description).
        2. Provides a clear thesis statement that outlines the writers position.
        3. Support the writers arguments with relevant examples and evidence.
        
        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Grade the essay out of 10 on each of the 3 points. Provide detailed description about how much you graded the essay on each of the points and provide feedback on how it could improve. Finally provide the average grade based on the 3 grades.
        """,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    inputs = {
        "essay": user_response,
        "task_title": title,
        "task_desc": description
    }

    feedback_from_api = chain.run(inputs)
    return feedback_from_api
