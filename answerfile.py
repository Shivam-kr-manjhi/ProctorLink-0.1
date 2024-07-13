import Evaluation as Eval
import llm as llm

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
    evals = Eval.get_score( llm.questions, answer, 5 )
    print("***********************************" , evals ,"******************************************************")
    return evals