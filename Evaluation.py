import AnswerEvaluationStream as EVAL
import CommunicateWithLLM as LLM

Similarity_parameter = 0.25
perplexity_parameter = 0.25
keyPoint_parameter = 0.25
Grammer_parameter = 0.25


# def get_evaluation( questionss , Answers ) :
number_of_questions = 3
# UserAnswers = []
questions =  LLM.getQuestions( "object oreinted programming" , 3 )
# for que in questions:
#     print("*******************")
#     print("------->>>>>" , end = " ")
#     print(len(que))
#     print(que)
#     print("*****************")
#     print("\n\n\n\n\n\n\n\n")
# print(len(questions)) 

# for ans in Answers:
#     print("*******************")
#     print("------->>>>>" , end = " ")
#     print(len(ans))
#     print(ans)
#     print("*****************")
#     print("\n\n\n\n\n\n\n\n")

def get_score( questions, UserAnswers , number_of_questions ):
    
    ModelAnswers = LLM.getAnswers( questions )
    UserAnswers = ModelAnswers

    TotalScore = 0

    for i in range( number_of_questions ):
        
        #  get  similarity score
        SimilarityScore = EVAL.get_similarityScore( UserAnswer=UserAnswers[i] , ExpectedAnswer=ModelAnswers[i] )

        # get perplexityscore
        PerplexityScore = EVAL.get_perplexityScore( UserAnswers[i] )

        # get get_keyPointsScore score
        keyPointsScore = EVAL.get_keyPointsScore( question= questions[i] , Answer=UserAnswers[i] )

        # get Grammer score
        GrammerScore = EVAL.get_grammerScore( UserAnswers[i] )

        CurrAnswerEVAl =  (SimilarityScore * Similarity_parameter) + (PerplexityScore * perplexity_parameter) + (keyPointsScore * keyPoint_parameter) + (GrammerScore * Grammer_parameter)


        TotalScore += CurrAnswerEVAl


    print(TotalScore)   
