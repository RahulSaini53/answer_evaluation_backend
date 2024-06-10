import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
from nltk.stem import PorterStemmer


from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from textblob import Word
# from language_tool_python import LanguageTool
from typing import List

'''~~~~~~~~~~~~~~~~~~~~~~~Stemming of word~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

ps = PorterStemmer()
def stemming(w):
    return ps.stem(w)

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~Grammar Error detection Part~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ '''
# def correct_grammar(sentences :List[str]):
#     tool = LanguageTool('en-US')

#     # Check grammar and get corrections
#     wrong = 0
#     for i in range(len(sentences)):
#         matches = tool.check(sentences[i])
#         if len(matches) <= 1: # may be one word is wrong just ignore it
#             continue
#         # Apply corrections
#         sentences[i] = tool.correct(sentences[i])
#         wrong += 1

#     return wrong


'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~Spelling Correction Part~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

def correct_spelling(word):
    w = Word(word)
    # Correct the spelling
    corrected_word = w.correct()
    return corrected_word

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Calculate Cosine Similarity~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

def calculate_cosine_similarity(sentence1, sentence2):
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the sentences into TF-IDF vectors
    tfidf_matrix = vectorizer.fit_transform([sentence1, sentence2])

    # Calculate cosine similarity between the vectors
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    return cosine_sim

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~Tokenize Paragraph in Sentences~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

def split_paragraph_into_sentences(paragraph):
    sentences = nltk.sent_tokenize(paragraph)
    return sentences


'''~~~~~~~~~~~~~~~~~~~~~~~~~~~Find all Synonyms of a Word~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

def Synonyms(word):
    synm = get_synonyms(word)

    s1 = set()
    for w in synm:
        s1 = s1 | get_synonyms(w)

    return s1

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Stop Word ~~~~~~~~~~~~'''    

str1='''weren't on just such each mustn't for no being shan't needn't at don wasn't having by because into been are do hasn't now between any than aren't did doing isn't same should or mightn't were does if from in so some other off should've here out down doesn't while shouldn't won't an only not there all a will mightn up as has few through with can don't was is had how didn and hadn't until then more when why couldn't of but too wouldn't didn't have haven't be where nor am to the about most 
 '''
stop_word = set(str1.split(" "))

'''~~~~~~~~~~~~~~~~~Calculate Maximum comparision Score of a Solution Sentence~~~~~~~~~~~~~~ '''

def find_Comp_Score(Ssen , Answer, Csim_upper , Csim_lower):# one solution sentence and all answer sentences for finding Maximum Comparision Score
    Ssen_Synm =  set()
    T_Ssen = word_tokenize(Ssen)
    #Removing Stop word in Solution sentence
    T_Ssen  = [w for w in T_Ssen if w not in stop_word]

    CS_current = 0
    KP = 1 # keyword penality

    Ssen_Synm_group = []
    for w in T_Ssen:
        w_s  = Synonyms(w)
        w_s.add(w)
        Ssen_Synm_group.append(w_s)

    for Asen in Answer:
        
        T_Asen = word_tokenize(Asen)

        # removing stop word
        T_Ssen = [w  for w in T_Ssen if w not in stop_word]

        # find  synonyms for all tokens of Answer
        Asen_Synm = set()
        for word in T_Asen:
            Asen_Synm.add(word)
            Asen_Synm |= Synonyms(word)

        # Count how many word of solution present in Answer
        intersection = 0
        for w_s in Ssen_Synm_group:
            for each in w_s:
                if each in Asen_Synm:
                    intersection += 1
                    break


        Kw = intersection/len(T_Ssen)  # Jaccard Similarity

        Sd = calculate_cosine_similarity(Ssen , Asen)  # recheck it
        Sw = Sd  # recheck it
     
        Ccs = 0
        if Sd >= Csim_upper:
            Sw = Sd
            Ccs = min(1,Sw + Kw)

        elif Sd >= Csim_lower:
            if Kw > 0.3 : # more than 30% match
                Ccs = min(1,Sw + Kw)
            else:
                Ccs = 0

        if Ccs > CS_current:
            CS_current = Ccs
            KP = (1-Kw)

    return CS_current , KP

'''~~~~~~~~~~~Predict the Marks of Answer according to similarity with Solution~~~~~~~~~~~~~~'''
def NLP_Predict_Score(Solution , Answer , maximum_marks , Cosine_sililarty_lower , Cosine_sililarty_upper):


    Solution = split_paragraph_into_sentences(Solution) # list of answers sentences
    Answer = split_paragraph_into_sentences(Answer) # list of answers sentences
    grammarly_wrong=0
    # Grammarly Correct the Answer of Student and also count how many sentences are wrong
    # grammarly_wrong = correct_grammar(Answer)

    Os = 0
    Mkp = 0
    count = 0
    length=0


    for s in Answer:
       length+=len(s)

    return 10

    for Ssen in Solution:
        Comparision_Score , KP = find_Comp_Score(Ssen,Answer,Cosine_sililarty_upper, Cosine_sililarty_lower)
        Mkp += KP
        if Comparision_Score != 0:
            count += 1
            Os += Comparision_Score
     
           

    Mkp = Mkp/len(Solution)
    if count:
        Os = Os/count
    
    # Subtract marks according to missing keyword in student solution ~
    Os =max(0, Os - (Mkp/1.6))
    # Subtract marks according to grammarly wrong sentence in student solution 
    Os=max(0,Os-(grammarly_wrong/length))
    final = Os*maximum_marks

    f = final - int(final)
    extra = 0
    if f>=0.75:
        extra = 1
    elif f>=0.25:
        extra = 0.5
    else:
        extra  = 0

    return int(final) + extra            
