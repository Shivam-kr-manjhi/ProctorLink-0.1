from transformers import BertTokenizer, BertModel 
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from sklearn.metrics.pairwise import cosine_similarity
import language_tool_python
# from gingerit.gingerit import GingerIt
import numpy as np
import torch
import spacy
import math

def get_sentence_embeddings(sentences):

    #Load pre-trained Bert Model and tokenizer
    #bert have its own embedding layer so it can get encodings for the numerical tokens generated by the tokenizer
    #pre-trained tokenizer is already have some rule for tokenizing and have lasrge corpus of words already mapped 
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    #Tokenize and encode the sentence
    inputs = tokenizer( sentences, return_tensors = 'pt', padding = True, truncation=True, max_length = 512 )


    #Get the hidden states from the BERT model
    #tranformer is implemented by pytorch and hence different from the other tensorflow frmaworks there is no inference(prediction) part so we have to explicity stop the gredient process with no_grad() 
    with torch.no_grad():
        output = model(**inputs)

    
    #extract the embeddings(vector) corresponding to the [CLS] token for each sentences
    cls_embeddings = output.last_hidden_state[:, 0, :]
    
    return cls_embeddings


#example usage
# sentences = [
#     "A transformer is a deep learning architecture introduced in the 'Attention is All You Need' paper. It's used for sequence-to-sequence tasks in natural language processing, leveraging self-attention mechanisms to capture contextual relationships",
#     # "Here is another sentence"
#     # "is this the first sentence"
#     "A transformer is a type of deep learning architecture designed for sequence processing tasks. Unlike traditional recurrent neural networks, it utilizes self-attention mechanisms to capture contextual dependencies, enabling more effective modeling of long-range dependencies in sequences."
# ]

# embeddings = get_sentence_embeddings( sentences )


# for i, embedding in enumerate(embeddings):
#     print(f"embedding of sentence {i+1} : {embedding}")

# print(embeddings.shape)


def get_similarityScore( UserAnswer, ExpectedAnswer ):
    
    sentences = [ UserAnswer, ExpectedAnswer ]
    embeddings = get_sentence_embeddings( sentences )

    vect1 = embeddings[0]
    vect2 = embeddings[1]

    vect1 = np.array(vect1).reshape(1,-1)
    vect2 = np.array(vect2).reshape(1,-1)

    similarity = cosine_similarity( vect1, vect2 )

    return similarity[0][0]



# print( get_similarityScore(" i'm good what about you" , " I'm fine how are you"))
# print( get_similarity(embeddings[0], embeddings[1] ))

# def get_GrammerScore( sentence ):
    
#    #Create an instance of GingerIt() -> [ The gingerit package in Python is a wrapper for the Ginger Software API, which is a grammar and spell checker.]
#    parser = GingerIt()
  
#    result =  parser.parse(sentence)


def get_keyPointsScore( question, Answer ):

    # load the spacy model
    model = spacy.load("en_core_web_sm")

    # pass the quesion to the model and get the ouput as doc
    que_doc = model(question)
    
    # Extract named Entities from the question
    Named_entities_in_ques = [ ent.text  for ent in que_doc.ents ]

    #Extract keywords using dependency parsing 

    # Subjects (nsubj): These would be words acting as the subjects in the sentence.
    # Direct Objects (dobj): Words that are directly receiving the action of the verb.
    # Prepositional Objects (pobj): Words that follow prepositions and act as the object of that preposition.
    question_keywords = [ token.text for token in que_doc if token.dep_ in ('nsubj', 'dobj', 'pobj')]
    
    # Extract noun phrases
    noun_phrases_in_ques = [ chunk.text for chunk in que_doc.noun_chunks ]
    
    # combine all three and now try to find  this set in answer as well 
    que_keyPoints = set( Named_entities_in_ques + question_keywords + noun_phrases_in_ques )

    # Run model for answer as well
    answer_doc = model(Answer)

    # Extract named entities from the answer
    Named_entities_in_ans = [ ent.text for ent in answer_doc.ents ]

    #Extracting keywords and noun phrases
    ans_keywords = [token.text for token in answer_doc if token.dep_ in ('nsubj', 'dobj', 'pobj')]
    noun_phrases_in_ans = [chunk.text for chunk in answer_doc.noun_chunks]

    # combine all three of them 
    answer_points = set( Named_entities_in_ans + ans_keywords + noun_phrases_in_ans )


    # cclculate number of key points coverd in the answer

    covered_points =  que_keyPoints.intersection( answer_points )
    coverage_score = len( covered_points) / len(que_keyPoints)

    return coverage_score


# print( get_keyPointsScore("how are you?", "i'm fine what about you"))



def map_perplexity_to_score(perplexity):

    if perplexity <= 1:
        return 1.0
    elif perplexity <= 20:
        return 1.0 - ((perplexity - 1)*(0.1)) / 20  # Linear interpolation between 1.0 and 0.9
    elif perplexity <= 50:
        return 0.9 - ((perplexity - 20)*(0.1)) / 30  # Linear interpolation between 0.9 and 0.8
    elif perplexity <= 70:
        return 0.8 - ((perplexity - 50)*(0.1)) / 20  # Linear interpolation between 0.8 and 0.7
    elif perplexity <= 90:
        return 0.7 - ((perplexity - 70)*(0.1)) / 20  # Linear interpolation between 0.7 and 0.6
    elif perplexity <= 120:
        return 0.6 - ((perplexity - 90)*(0.1)) / 20  # Linear interpolation between 0.6 and 0.5
    elif perplexity <= 140:
        return 0.5 - ((perplexity - 120)*(0.1)) / 20  # Linear interpolation between 0.5 and 0.4
    elif perplexity <= 160:
        return 0.4 - ((perplexity - 140)*(0.1))/ 20  # Linear interpolation between 0.4 and 0.3
    elif perplexity <= 180:
        return 0.3 - ((perplexity - 160)*(0.1)) / 20  # Linear interpolation between 0.3 and 0.2
    elif perplexity <= 200:
        return 0.2 - ((perplexity - 180)*(0.1)) / 20  # Linear interpolation between 0.2 and 0.1
    elif perplexity <= 220:
        return 0.1 - ((perplexity - 200)*(0.1)) / 20  # Linear interpolation between 0.1 and 0.0
    else:
        return 0.0  # Scores less than 50 perplexity
    


def get_perplexityScore( sentence ):
   
   # Load pretrained model and tokenizer
   model_name = 'gpt2'
   model = GPT2LMHeadModel.from_pretrained(model_name)
   tokenizer = GPT2Tokenizer.from_pretrained(model_name)


   # ensure model is in evaluation mode
   model.eval()

   # tokenize the text
   inputs = tokenizer( sentence, return_tensors = 'pt')

   # get input ids and length
   input_ids = inputs['input_ids']
   length = input_ids.size(1)


   # compute loss ( negative log likelihood )
   with torch.no_grad():
       outputs = model( input_ids, labels=input_ids )
       loss = outputs.loss

   perplexity = math.exp(loss.item())

   print(perplexity)
   
   # formate upto one decimal place only 
   score = map_perplexity_to_score(perplexity)

   return score


# print(get_perplexityScore("Data science is a multidisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge and insights from structured and unstructured data. It combines aspects of statistics, computer science, and domain expertise to analyze data and make data-driven decisions"))



def get_grammerScore( sentence ):
    
    # Initialize LanguageTool for English 

    # The tool parses the sentence and applies a wide range of linguistic rules and patterns to identify potential errors. These rules cover grammatical correctness, spelling mistakes, punctuation issues, and stylistic suggestions.
    tool = language_tool_python.LanguageTool('en-US')

    # Details of matches
    # Each element in the matches list is a Match object, which contains the following attributes:

    # fromy and fromx: The starting position (line and character) of the error in the sentence.
    # toy and tox: The ending position (line and character) of the error in the sentence.
    # ruleId: The ID of the rule that identified the error.
    # message: A description of the error and how to fix it.
    # replacements: Suggested corrections for the error.
    # offset: The character offset of the error in the sentence.
    # length: The length of the error in characters.
    # context: The context around the error, useful for understanding the mistake.
    # contextoffset: The offset of the error within the context.
    # sentence: The full sentence that was checked.

    match = tool.check( sentence )
    
    num_errors = len( match )
    num_words = len(sentence.split())


    # Erro rate per word
    error_rate = num_errors / num_words if num_words > 0 else 0

    # Normalize the score: lower error rate means higher score
    # Assuming a maximum error rate of 1 error per word (which is very high)
    normalized_score = max(0, 1 - error_rate)
    
    return normalized_score



# good_sentence = "The quick brown fox jumps over the lazy dog."
# bad_sentence = "Fox brown quick the jumps dog lazy over the."

# print( get_grammerScore(bad_sentence))

    
