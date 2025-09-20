import openai
from dotenv import dotenv_values

config = dotenv_values(".env")

openai.api_key = config["API_KEY"]


openai.api_key = "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"
def generate_response(prompt): #create a function to generate a paragraph
   #Create response variable to store the response from the API
   #Model parameter is the model to use
    #Prompt parameter is the prompt to use the main instructions
    #Max_tokens parameter dececides how long the response will be, the higher the longer. 75 words is 100 tokens
    #Temperature parameter decides the randomness of the response, the higher the more creative the loweer
    # the well defined. 0.3 is a good value to use. 
    #0: The same response every time.
    #1: A different response every time, even if it's the same prompt.


    response = openai.completions.create( 
        model = "gpt-3.5-turbo-instruct",
        prompt = "Write a paragraph about the following topic. " + prompt,
        max_tokens = 400,
        temperature = 0.3)
    
    #
    retrieve_blog = response.choices[0].text
    return retrieve_blog
 
print(generate_response("Why is Los Angeles the best city in the world?"))  

keep_writing = True

while keep_writing:
    answer = input("Do you want to write another blog? (yes/no): ")
    if answer.lower() == "yes":
        topic = input("What do you want to write about? ")
        print(generate_response(topic))
    elif answer.lower() == "no":
        keep_writing = False
    else:
        print("Please answer with 'yes' or 'no'.")