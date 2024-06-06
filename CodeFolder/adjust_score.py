def Round(x):
    m = int(x)
    f = x-m
    ex = 0
    if f>0.7:
        ex = 1
    elif f>0.3:
        ex = 0.5
    return m + ex         

def Adjust_Score(ml_score , nlp_score):
    if ml_score==nlp_score:
        return ml_score
    if nlp_score > ml_score:
        return Round(max(0,nlp_score-0.1*ml_score))
    if ml_score > nlp_score:
        return Round(min(100,nlp_score+0.1*ml_score))
