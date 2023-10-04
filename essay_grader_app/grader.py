 
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

def grade_essay(user_response, title, description, exam_type, essay_type, grade):
    print(exam_type, essay_type, grade)
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

    ielts_prompt = PromptTemplate(
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

    naplan_persuasive_grade3_prompt = PromptTemplate(
        input_variables=["essay", "task_title", "task_desc"],
        template="""You are an essay grader for Naplan persuasive writing task for grade 3 students. You will follow the below criteria and grade the students on all the provided criteria using the provided guidelines.

        Grade 3 Persuasive Writing Grading Criteria

1. Audience (Scored out of 6)

1-2 Points: The student shows a basic awareness of the reader. The writing may have moments where it addresses the reader but lacks consistent engagement.
3-4 Points: The student attempts to engage the reader throughout the piece. There's an evident effort to persuade the reader, though it may not always be effective.
5-6 Points: The student consistently engages and orients the reader. The writing effectively persuades and connects with the reader throughout.
2. Text Structure (Scored out of 4)

1 Point: The student provides a basic structure with a beginning, middle, and end, though transitions might be lacking.
2-3 Points: The student organizes the text with a clear introduction, body, and conclusion. Some transitions are used to connect ideas.
4 Points: The writing has a clear and effective structure. Transitions are smoothly integrated, guiding the reader through the argument.
3. Ideas (Scored out of 5)

1-2 Points: The student presents a simple argument or point of view with minimal supporting details.
3-4 Points: The student's argument is clearer, with some relevant supporting details. The writing may occasionally lack depth or elaboration.
5 Points: The student presents a well-thought-out argument, supported by relevant and detailed examples or reasons.
4. Persuasive Devices (Scored out of 4)

1 Point: Minimal use of persuasive devices. The student may rely on basic statements without much elaboration.
2-3 Points: The student uses some persuasive devices, such as repetition or rhetorical questions, though not always effectively.
4 Points: The student effectively uses a range of persuasive devices to enhance their argument.
5. Vocabulary (Scored out of 5)

1-2 Points: The student uses basic vocabulary suitable for their age. Word choice may occasionally hinder clarity.
3-4 Points: The student uses a varied vocabulary, with some words chosen for effect.
5 Points: The student's vocabulary is varied and purposeful, enhancing the persuasive quality of the writing.
6. Cohesion (Scored out of 4)

1 Point: The student's writing may lack clear connections between ideas.
2-3 Points: Some use of referring words and text connectives to link ideas, though not always effectively.
4 Points: The student effectively controls multiple threads and relationships across the text, creating a cohesive argument.
7. Paragraphing (Scored out of 2)

1 Point: The student attempts to group related ideas into paragraphs, though transitions might be abrupt.
2 Points: Ideas are effectively grouped into clear paragraphs, enhancing the clarity and flow of the argument.
8. Sentence Structure (Scored out of 6)

1-2 Points: The student forms simple sentences, with occasional errors that might hinder clarity.
3-4 Points: The student uses a mix of simple and compound sentences, with few errors.
5-6 Points: The student effectively uses a variety of sentence structures, enhancing the clarity and rhythm of the writing.
9. Punctuation (Scored out of 6)

1-2 Points: The student uses basic punctuation (periods, question marks) with some errors.
3-4 Points: The student correctly uses a range of punctuation, including commas and apostrophes, with occasional errors.
5-6 Points: Punctuation is used effectively and accurately throughout the writing, aiding the reader's understanding.
10. Spelling (Scored out of 6)

1-2 Points: The student spells simple words correctly, with errors in more challenging words.
3-4 Points: Most words, including some challenging ones, are spelled correctly.
5-6 Points: The student demonstrates a strong grasp of spelling, with errors being rare.

        Task Title: {task_title}

        Task Description: {task_desc}

        Essay: {essay}

        Grade the essay based on the provided guidelines while providing a 2-3 lines justifying the specic score you provided for each of the criteria. Dont provide a range, use a specific number for the score. Mention your score and what it is out of for each criteria. 
        For each criteria mention what is good in the input essay, and how if it all it cab be improved to meet the guidelines better. For spelling mistakes and grammatical errors, specifically mention the sentences where the errors are by quoting them.
        Finally sum up the individual scores to provide an overall score out of 48.
        """,
    )

 # Determine which prompt to use based on the parameters
    if exam_type.strip().lower() == "ielts":
        prompt = ielts_prompt
    elif exam_type.strip().lower() == "naplan":
        if essay_type.strip().lower() == "persuasive":
            if grade == "Grade 3":
                prompt = naplan_persuasive_grade3_prompt
        #     elif grade == "Grade 5":
        #         prompt = naplan_persuasive_grade5_prompt  # Placeholder, you'll need to define this
        #     elif grade == "Grade 7":
        #         prompt = naplan_persuasive_grade7_prompt  # Placeholder, you'll need to define this
        #     elif grade == "Grade 9":
        #         prompt = naplan_persuasive_grade9_prompt  # Placeholder, you'll need to define this
        # elif essay_type.strip().lower() == "narrative":
        #     if grade == "Grade 3":
        #         prompt = naplan_narrative_grade3_prompt  # Placeholder, you'll need to define this
        #     # ... [Continue for other grades and essay types] ...

    chain = LLMChain(llm=llm, prompt=prompt)

    inputs = {
        "essay": user_response,
        "task_title": title,
        "task_desc": description
    }

    feedback_from_api = chain.run(inputs)
    return feedback_from_api
