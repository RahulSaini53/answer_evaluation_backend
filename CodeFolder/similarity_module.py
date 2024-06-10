import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import Word

# Ensure the necessary nltk data packages are downloaded
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

stop_word = set(stopwords.words('english'))

ps = PorterStemmer()

def stemming(w):
    return ps.stem(w)

def correct_spelling(word):
    w = Word(word)
    corrected_word = w.correct()
    return corrected_word

def calculate_cosine_similarity(sentence1, sentence2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([sentence1, sentence2])
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return cosine_sim

def split_paragraph_into_sentences(paragraph):
    sentences = nltk.sent_tokenize(paragraph)
    return sentences

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

def find_Comp_Score(Ssen, Answer, Csim_upper, Csim_lower):
    T_Ssen = word_tokenize(Ssen)
    T_Ssen = [w for w in T_Ssen if w.lower() not in stop_word]
    
    CS_current = 0
    KP = 1  # keyword penalty
    
    Ssen_Synm_group = []
    for w in T_Ssen:
        w_s = Synonyms(w)
        w_s.add(w)
        Ssen_Synm_group.append(w_s)
    
    for Asen in Answer:
        T_Asen = word_tokenize(Asen)
        T_Asen = [w for w in T_Asen if w.lower() not in stop_word]
        
        Asen_Synm = set()
        for word in T_Asen:
            Asen_Synm.add(word)
            Asen_Synm |= Synonyms(word)
        
        intersection = sum(1 for w_s in Ssen_Synm_group if any(each in Asen_Synm for each in w_s))
        Kw = intersection / len(T_Ssen) if T_Ssen else 0
        
        Sd = calculate_cosine_similarity(Ssen, Asen)
        Sw = Sd
        
        Ccs = 0
        if Sd >= Csim_upper:
            Sw = Sd
            Ccs = min(1, Sw + Kw)
        elif Sd >= Csim_lower:
            if Kw > 0.3:
                Ccs = min(1, Sw + Kw)
            else:
                Ccs = 0
        
        if Ccs > CS_current:
            CS_current = Ccs
            KP = 1 - Kw
    
    return CS_current, KP

def NLP_Predict_Score(Solution, Answer, maximum_marks, Cosine_sililarty_lower, Cosine_sililarty_upper):
    Solution = split_paragraph_into_sentences(Solution)
    Answer = split_paragraph_into_sentences(Answer)
    
    grammarly_wrong = 0
    Os = 0
    Mkp = 0
    count = 0
    length = sum(len(s) for s in Answer)
    
    for Ssen in Solution:
        Comparision_Score, KP = find_Comp_Score(Ssen, Answer, Cosine_sililarty_upper, Cosine_sililarty_lower)
        Mkp += KP
        if Comparision_Score != 0:
            count += 1
            Os += Comparision_Score
    
    Mkp = Mkp / len(Solution) if Solution else 0
    if count:
        Os = Os / count
    
    Os = max(0, Os - (Mkp / 1.6))
    Os = max(0, Os - (grammarly_wrong / length))
    
    final = Os * maximum_marks
    f = final - int(final)
    extra = 1 if f >= 0.75 else 0.5 if f >= 0.25 else 0
    
    return int(final) + extra
