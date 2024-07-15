import CommunicateWithLLM as LLM

subject = ""
questions = []


def insert_subject( sub ):
    global subject, questions  # Use global to modify the global variables
    subject = sub
    questions = LLM.getQuestions( sub, 5 )
    # print("question walah part is done ****************************************** " , len(questions) ,"->>",sub )
    for que in questions:
        print(que, "\n\n\n\n" )



def askQA(index):
    return questions[int(index)]



def get_questions():
    global questions
    return questions


# you write all your code here

# just make sure that you have the above askQA function always so that it can be fetched

# now

# if u want question , u have it in the this file itself

# for user answer

from answerfile import getans


# this will return list of answer


# now u will have question , userans , and the actual answer will also be generated in this file itself.

# make sure to get the final stats in to an array  and a fucntion that will return it when called.
# so that i can render it on stats page.

# thanks.