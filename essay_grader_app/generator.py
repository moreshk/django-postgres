# essay_grader_app/generator.py

def generate_test():
    return "Hello World"

import json
import os
from dotenv import load_dotenv
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY in the .env file.")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def generate_test_data(exam_type, essay_type, grade):
    # ... (Place the logic from the Flask code here) ...


    # This is an LLMChain to create a task for a particular exam
    print(exam_type, essay_type,grade)

    llm = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")


    naplan_narrative_template = """You are a test task creator for {test_type}. I will provide you the test type and your job is to create a prompt for a narrative (story) writing task for a test taker.

    Sample Tasks for {test_type}
    Sample 1: Imagine
    Task: "Imagine if a character found an object that made something amazing happen. Write a narrative (story) about the adventure. You can use the characters and objects on this page OR you can make up your own."

    Sample 2: What a mess!
    Task: "Today you are going to write a narrative (a story). The idea for your story is `What a mess!` Your story might be about a messy person, an untidy place or a complicated or tricky situation. 
    It might be a mix-up between people, or it might be about a plan gone wrong. It could be about a broken promise or friendship, or an unexpected event that causes confusion."

    Sample 3: Found
    Task: "Today you are going to write a narrative or story. The idea for your story is `FOUND`. Your story might be about finding a lost pet, hidden treasures or new friends.
    It could be about finding the solution to a problem or finding an opportunity to do something different and exciting. Your story could be about how people in difficult situations find courage, help or understanding."

    Sample 4: The Box
    Task: "Today you are going to write a narrative or story. The idea for your story is `The Box`. What is inside the Box? How did it get there? Is it valuable? Perhaps it is alive! 
    The Box might reveal a message or something that was hidden. What happens in your story if the Box is opened?"

    You will use the above examples only as a guideline for framing the task and create a new task and description randomly on a different topic. No need to use the word Sample in the task description. 

    Create 5 such tasks and descriptions based on the above guidelines. In your output mention these 5 tasks and format the output as Title:  and Description: .
    """

    ielts_template = """You are a test task creator for {test_type}. I will provide you the test type and your job is to create a task for a test taker.

    You will provide a topic and ask the user if they agree or disagree, provide pros and cons etc and provide their views on the topic.

    Sample Tasks for {test_type}
    Sample 1: Technology
    Task: "Some people believe that technological advancements lead to the loss of traditional cultures. To what extent do you agree or disagree?"

    Sample 2: Education
    Task: "Some educators argue that every child should be taught how to play a musical instrument. Discuss the advantages and disadvantages of this. Give your own opinion."

    Sample 3: Environment
    Task: "Climate change is now an accepted threat to our planet, but there is not enough political action to control excessive consumerism and pollution. Discuss both views and give your own opinion."

    Sample 4: Health
    Task: "Some people think that governments should focus on reducing healthcare costs, rather than funding arts and sports. Do you agree or disagree?"

    Sample 5: Society
    Task: "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion."

    Sample 6: Work
    Task: "Remote work is becoming increasingly popular. Discuss the advantages and disadvantages of working from home."

    Sample 7: Global Issues
    Task: "Some people argue that developed countries have a higher obligation to combat climate change than developing countries. Discuss both sides and give your own opinion."

    Sample 8: Science
    Task: "Genetic engineering is an important issue in modern society. Some people think that it will improve people’s lives in many ways. Others feel that it may be a threat to life on earth. Discuss both these views and give your own opinion."

    You will use the above examples only as a guideline for framing the task and create a new task and description randomly on a different topic. No need to use the word Sample in the task description. 

    Create 5 such tasks and descriptions based on the above guidelines. In your output mention these 5 tasks and format the output as Title:  and Description: .
    """

    naplan_pesuasive_template = """You are a test task creator for {test_type}. I will provide you the test type and your job is to create a prompt for a persuasive writing task for a test taker.

    Sample Tasks for {test_type}
    Sample 1: Too much money is spent on toys and games
    Task: "People like to play with toys and games to have fun and to relax. Some people think that too much money is spent on toys and games. They think the money could be used for more
important things. What do you think? Do you agree or disagree? Perhaps you can think of ideas for both sides of this topic. Write to convince a reader of your opinions"

    Sample 2: Change a rule or law
    Task: "Rules and laws tell us what we can and cannot do. Choose a rule or law that you think needs to change. It could be a home or school rule. It could be a rule of a game or sport. It could be a law that everyone
has to follow. The change should make the rule or law better. Write to convince a reader why this rule or law should be changed."

    Sample 3: Hero Award
    Task: "A hero is someone you admire. Choose a hero who you think deserves an award. The person you choose could be someone from your family or community or could be someone
well-known to everyone. The person may be young or old, male or female. Write to convince a reader why the person you have chosen is special and should be given an award." 
    
    Sample 4: Everyone should learn to cook.
    
    Task: "Do you agree? Do you disagree? Perhaps you can think of ideas for both sides. Write to convince a reader of your opinion. "

    Sample 5: Try this activity
    Task: "Choose a sport, hobby or activity that you are interested in. Write to persuade a reader why they should try your chosen activity. "

    You will use the above examples only as a guideline for framing the task and create a new task and description randomly on a different topic. No need to use the word Sample in the task description. 

    Create 5 such tasks and descriptions based on the above guidelines. In your output mention these 5 tasks and format the output as Title:  and Description: .
    """


    # Select the appropriate template based on exam_type and essay_type
    if exam_type == "IELTS":
        template = ielts_template
    elif exam_type == "NAPLAN" and essay_type == "Narrative":
        template = naplan_narrative_template
    elif exam_type == "NAPLAN" and essay_type == "Persuasive":
        template = naplan_pesuasive_template
    else:
        # Default to IELTS template (or any other default you prefer)
        template = ielts_template


    prompt_template = PromptTemplate(input_variables=["test_type"], template=template)
    task_creator_chain = LLMChain(llm=llm, prompt=prompt_template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    template = """You are a test task selector. I will provide you a list of five tasks and their respective descriptions below. 

    {five_tasks}

    You will select one of the tasks randomly and output it along with its description in a json format that has the following fields:

    "title": "picked randomly from the ten tasks",
    "description": "description for the randomly picked title"
    """

    prompt_template = PromptTemplate(input_variables=["five_tasks"], template=template)
    task_selector_chain = LLMChain(llm=llm, prompt=prompt_template)

    # print(task_selector_chain.run(writing_task))

    # This is the overall chain where we run these two chains in sequence.
    from langchain.chains import SimpleSequentialChain
    overall_chain = SimpleSequentialChain(chains=[task_creator_chain, task_selector_chain], verbose=True)


    generated_data = overall_chain.run(exam_type)
    try:
        generated_data = json.loads(generated_data)
    except (json.JSONDecodeError, TypeError):
        pass

    if isinstance(generated_data, dict):
        title = generated_data.get('title', 'Default Title')
        description = generated_data.get('description', 'Default Description')
        result = f"Title: {title}\nDescription: {description}"
        
        # Check if the exam_type is "naplan" and essay_type is "persuasive"
        if exam_type.lower() == "naplan" and essay_type.lower() == "persuasive":
            additional_text = """
Start with an introduction.
An introduction lets a reader know what
you are going to write about.
• Write your reasons for your choice.
Why is it important for others to get
involved in this activity? Explain your
reasons.
• Finish with a conclusion.
A conclusion sums up your reasons
so that a reader is convinced of your
opinion.
Remember to:
• plan your writing
• use paragraphs to organise your ideas
• write in sentences
• choose your words carefully to convince a reader of your opinion
• pay attention to your spelling and punctuation
• check and edit your writing so it is clear.
"""
            result += additional_text  # Append the additional text to the result

    # Check if the exam_type is "naplan" and essay_type is "narrative"
        if exam_type.lower() == "naplan" and essay_type.lower() == "narrative":
            narrative_text = """
    Think about:
    • the characters in your story
    • when and where your story takes place
    • the complication or problem and how it is solved
    • how the story ends.
    Remember to:
    • plan your story before you start
    • choose your words carefully
    • write in sentences
    • pay attention to your spelling, punctuation and
    paragraphs
    • check and edit your writing.
    """
            result += narrative_text  # Append the narrative text to the result

        return result
    else:
        return "Error: Unexpected data format"

      