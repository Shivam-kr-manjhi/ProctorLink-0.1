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
    TotalScore = 0
    AvgkeyPointsCovered = 0
    AvgReadabilityScore = 0
    AvgCurrectnessScore = 0
    AvgGrammerScore = 0

    itr = 1

    for i in range( number_of_questions ):
        
        #  get  similarity score
        SimilarityScore = EVAL.get_similarityScore( UserAnswer=UserAnswers[i] , ExpectedAnswer=ModelAnswers[i] )
        AvgCurrectnessScore += SimilarityScore
        

        # get perplexityscore
        PerplexityScore = EVAL.get_perplexityScore( UserAnswers[i] )
        AvgReadabilityScore += PerplexityScore

        # get get_keyPointsScore score
        keyPointsScore = EVAL.get_keyPointsScore( question= questions[i] , Answer=UserAnswers[i] )
        AvgkeyPointsCovered += keyPointsScore

        # get Grammer score
        GrammerScore = EVAL.get_grammerScore( UserAnswers[i] )
        AvgGrammerScore += GrammerScore

        CurrAnswerEVAl =  (SimilarityScore * Similarity_parameter) + (PerplexityScore * perplexity_parameter) + (keyPointsScore * keyPoint_parameter) + (GrammerScore * Grammer_parameter)


        TotalScore += CurrAnswerEVAl

        print(f"{itr} iteration completed")
        itr = itr+1

    print("2")

    AvgReadabilityScore /= number_of_questions
    AvgkeyPointsCovered /= number_of_questions
    AvgCurrectnessScore /= number_of_questions
    AvgGrammerScore /= number_of_questions

    print( "TotalScore - > " ,TotalScore  )
    print( 'Readability - >' , AvgReadabilityScore )
    print( 'Currectness - >' , AvgCurrectnessScore )
    print( 'keyPointsCovered - >', AvgkeyPointsCovered  )
    print( 'GrammerScore - >' , AvgGrammerScore  )

    eval = {
        'TotalScore' : round(TotalScore/5,2),
        'Readability' : round(AvgReadabilityScore*100,2),
        'Currectness' : round(AvgCurrectnessScore*100,2),
        'keyPointsCovered' : round(AvgkeyPointsCovered*100,2),
        'GrammerScore' : round(AvgGrammerScore*100,2)
    }

    return eval
