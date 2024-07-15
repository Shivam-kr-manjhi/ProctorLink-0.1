from Evaluation import get_score
from llm import get_questions

answer=[]

def reset():
    global answer
    answer.clear()

def insert(s):
    global answer
    answer.append(s)

def getans():
    global answer
    return answer

def getEvaluation():
    questions = get_questions()
    print(questions)
    evals = get_score( questions, answer, 5 )
    print(evals)
    return evals