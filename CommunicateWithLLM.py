
# InferenceClient is  used for direct communication with huggingface inference API's
#  HuggingFaceHub's funtion like 
#         hub = HuggingFaceHub(
#             repo_id="model-repo-id",
#             api_token="your_hf_api_token"
#         )
# doesn't work properlly
import os
from huggingface_hub import InferenceClient  
from langchain.prompts import PromptTemplate



# huggingface api key is environmented privately
API_KEY =  os.environ.get('HuggingFace_API_KEY')
# print(API_KEY)


# The InferenceClient is designed to facilitate communication with models hosted on the Hugging Face Hub via their Inference API. It provides a straightforward interface to send requests to a specified model endpoint and retrieve responses.

# Initialization
# To initialize the InferenceClient, you need to provide:

# model_id: The identifier for the model hosted on Hugging Face Hub (e.g., "mistralai/Mistral-7B-Instruct-v0.3").
# token: Your Hugging Face API token, which is used for authentication.
client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.3",
    token=API_KEY,
)



def getQuestions( subject, number_of_questions ) :
        

        prompt_template = PromptTemplate(
            input_variables=["subject" , "number_of_questions"],
            template="Generate {number_of_questions} challenging, graduate-level questions on {subject}. Each question should cover advanced topics, be well-defined, specific, within 150 words, in a single paragraph, and separated by '\n'. Topics include theoretical concepts, mathematical foundations, and practical applications."
        )
   
        prompt = prompt_template.format( subject = subject , number_of_questions = number_of_questions )
        # print( prompt)

        #  this is an text generation model which accepts the input in the formate of list of dictionarys defining the role and content 
        #  for exampple :
        # [ {" role" : "user" , " contecnt" : "hi, there how are you"}
        #  {" role" : "model" , " contecnt" : "hello, i'm good what about you"}]
        #  these type of structure may used in the meamory creation for model, here the model can read previous context and response in a better way

        messages = [
            {"role": "user", "content": prompt}
        ]

        questions = ""


        # "messages" ->  should be a list of dictionaries where each dictionary represents a message with roles and content.
        # "max_tokens" (optional) ->   specifies the maximum number of tokens to generate for each message.
        # "stream" (optional) ->   controls whether to stream the responses back in real-time.
        for message in client.chat_completion(
            messages = messages,
            max_tokens=1000, 
            stream=True, 
        ):

            questions += str(message.choices[0].delta.content )

        questions = questions.split("\n")
        questions = [ question for question in questions if question != "" ]
        
        return questions




def getAnswers( questions ):
      
      Answers = [ ]

      prompt_template = PromptTemplate(
    
            input_variables=["question",],
            template="Answer the following question in a single paragraph using formal academic language. Your response should be clear, concise, and detailed, appropriate for a graduate-level understanding. Avoid using bullet points or lists. The answer should serve as a benchmark for evaluating student responses.                                                     Question: [{question}]"
       )
      
      for ques in questions:
            
            if len(ques) > 5:
                  
                prompt = prompt_template.format( question = ques )

                messages = [ {"role": "user", "content": prompt } ]
                # print(prompt)
                
                answer = ""

                # "messages" ->  should be a list of dictionaries where each dictionary represents a message with roles and content.
                # "max_tokens" (optional) ->   specifies the maximum number of tokens to generate for each message.
                # "stream" (optional) ->   controls whether to stream the responses back in real-time.
                for message in client.chat_completion(
                    messages = messages,
                    max_tokens=500, 
                    stream=True, 
                ):

                    answer += str(message.choices[0].delta.content )
                
                Answers.append(answer)



      return Answers
      





