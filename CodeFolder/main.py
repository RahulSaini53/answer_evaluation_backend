from CodeFolder.similarity_module import NLP_Predict_Score
from CodeFolder.ML_module import ML_Predict_Score
from CodeFolder.adjust_score import Adjust_Score
from CodeFolder.OCR import image_to_text # take file path as input 


def Get_score(solution,answer):

    maximum_marks = 10
    Cosine_sililarty_lower = 0.2
    Cosine_sililarty_upper = 0.7 # Th values

    # '''Teacher Solution'''
    # solution = "I am a student of MNIT" 

    # '''Student Answer'''
    # answer = "I am MNITian Student"

    # ml_score = ML_Predict_Score(solution , answer)
    ml_score=7
    nlp_score = NLP_Predict_Score(solution, answer, maximum_marks, Cosine_sililarty_lower, Cosine_sililarty_upper)
    # nlp_score=5
  
    
    score = Adjust_Score(ml_score , nlp_score*10) # becase 0<=nlp_score<=10 , but 0<=ml_score<=100)
    score = score/10 # setting score range between 0 to 10 
    
    floor_v = int(score)
    fr = score - floor_v
    if fr>=0.75:
        fr = 1
    elif fr>=0.25:
        fr = 0.5
    else:
        fr = 0

    final_score = floor_v + fr

    print(final_score)
    return final_score


