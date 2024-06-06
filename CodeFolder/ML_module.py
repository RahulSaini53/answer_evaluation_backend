import pandas as pd
import numpy as np
from math import ceil
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from CodeFolder.similarity_module import NLP_Predict_Score # import from similarity module
from CodeFolder.adjust_score import Adjust_Score

# Load data (solution, answer, and grade)
data = pd.read_csv(r'C:\Users\rksck\Desktop\major project2\backend\project_backend\CodeFolder\data1.csv')

# Split data into features (solution and answer) and label (grade)
X = data[['solution', 'answer']]

y = data['grade'] # range = 0-100
               

# Define TF-IDF vectorizer for text features
tfidf_vectorizer = TfidfVectorizer()

# Define a pipeline for preprocessing and modeling
pipeline = Pipeline([
    ('transformer', ColumnTransformer([
        ('tfidf_solution', tfidf_vectorizer, 'solution'),
        ('tfidf_answer', tfidf_vectorizer, 'answer')
    ], remainder='passthrough')),
    ('model', LinearRegression())
])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=32)

# minimum on random_state = 32 , test_size = 0.1

# Train the model
pipeline.fit(X_train, y_train)

# Make predictions on test data
def ML_Predict_Score(S , A):
    d = {
        'solution':[S], 
        'answer':[A]
    }

    score = (pipeline.predict(pd.DataFrame(d))[0])
    score = ceil(score*100)/100

    return score
    
    

'''
y_pred = pipeline.predict(X_test)

ml_error = ceil(mean_absolute_error(y_test, y_pred)*100)/100

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~Similarity module error calcualtion ~~~~~~~~~~~~~~~~~~~~~

error1 = 0
X_test = X_test.to_numpy()
y_test = y_test.to_numpy()

maximum_marks = 10
Cosine_sililarty_lower = 0.2
Cosine_sililarty_upper = 0.7 # Th values


y_pred_nlp = []
for i in range(len(y_test)):
    s,a = np.array(X_test[i])
    pred_1 = NLP_Predict_Score(s , a , maximum_marks ,Cosine_sililarty_lower, Cosine_sililarty_upper )
    y_pred_nlp.append(pred_1*10)

y_final = []
for i in range(len(y_pred)):
    y_final.append(Adjust_Score(y_pred[i] , y_pred_nlp[i]))
total =  mean_absolute_error(y_test, y_pred_nlp) 

nlp_error = ceil(mean_absolute_error(y_test, y_pred_nlp)*100)/100


'''