
# apikey = "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"
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


# The InferenceClient is designed to facilitate communication with models hosted on the Hugging Face Hub via their Inference API. It provides a straightforward interface to send requests to a specified model endpoint and retrieve responses.

# Initialization
# To initialize the InferenceClient, you need to provide:

# model_id: The identifier for the model hosted on Hugging Face Hub (e.g., "mistralai/Mistral-7B-Instruct-v0.3").
# token: Your Hugging Face API token, which is used for authentication.
client = InferenceClient(
    "mistralai/Mistral-7B-Instruct-v0.3",
    token=API_KEY,
)


prompt_template = PromptTemplate(
    input_variables=["subject" , "number_of_questions"],
    template="Generate {number_of_questions} detailed and challenging questions on the subject of {subject}. The questions should cover a range of advanced topics within {subject}, including but not limited to, theoretical concepts, mathematical foundations, practical applications. Ensure that each question is well-defined, specific, and requires a deep understanding of the subject matter. The questions should be suitable for a graduate-level course and designed to test a student's comprehensive knowledge and critical thinking skills in {subject}."
)

prompt = prompt_template.format( subject = "Machine learning" , number_of_questions = 10 )
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





