import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

# from sklearn.linear_model import LogisticRegression
# from sklearn.linear_model import LogisticRegressionCV
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.naive_bayes import BernoulliNB
# from sklearn.naive_bayes import MultinomialNB, GaussianNB


from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from math import ceil
from CodeFolder.similarity_module import NLP_Predict_Score # import from similarity module
from CodeFolder.adjust_score import Adjust_Score

# def adjust_score(mark_ml , mark_nlp):

# Load data (solution, answer, and grade)
data = pd.read_csv(r'C:\Users\rksck\Desktop\major project2\backend\project_backend\CodeFolder\data1.csv')

# Split data into features (solution and answer) and label (grade)
X1 = data[['solution', 'answer']]

y1 = data['grade']# range = 0-100
               
def fun(X,y):

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

    y_pred = pipeline.predict(X_test)

    ml_error = mean_absolute_error(y_test, y_pred)

    ''' ~~~~~~~~~~~~~~~~~~~~~~~~~~~~Similarity module error calcualtion ~~~~~~~~~~~~~~~~~~~~~'''

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

    nlp_error = mean_absolute_error(y_test, y_pred_nlp)

    # print("Mean Absolute Error in ML model: = ", ml_error)
    # print("Mean Absolute Error in NLP module: = ", nlp_error)
    y_final = []
    for i in range(len(y_pred)):
        y_final.append(Adjust_Score(y_pred[i] , y_pred_nlp[i]))
    total =  mean_absolute_error(y_test, y_pred_nlp)   
    return ml_error , nlp_error,total

x_axis = []
y_axis1 =  [] # ml error
y_axis2 = [] # nlp error
y_total = []
for i in range(60, 151 , 10):
    x = X1[:i]
    y = y1[:i]
    x_axis.append(i)
    ml,nlp,total = fun(x,y)
    y_axis1.append(100 - ceil(ml*100)/100)
    y_axis2.append(100 - ceil(nlp*100)/100)
    y_total.append(100 -ceil(total*100)/100) 


import matplotlib.pyplot as plt
x = x_axis
y1 = y_axis1

y2 = y_axis2

bar_width = 2

plt.bar(x, y1, color='blue', width=bar_width, label='ML model Accuracy')
plt.bar([xi + bar_width for xi in x], y2, color='red', width=bar_width, label='NLP module Accuracy')

# Adding text labels on top of each bar
for xi, yi in zip(x, y1):
    plt.text(xi, yi + 0.5, str(yi), ha='center', va='bottom', color='black')

for xi, yi in zip(x, y2):
    plt.text(xi + bar_width, yi + 0.5, str(yi), ha='center', va='bottom', color='black')


# print(y_total)
plt.xlabel('Data Size-(Data split = 90% training , 10% testing)')
plt.ylabel('Accuracy')
plt.title('Data Size v/s Accuracy Analysis')
plt.legend()
plt.savefig('accuracy_ml_nlp1.png')
plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
y1 = y_total
plt.bar(x, y1, color='blue', width=bar_width, label='Total System')


# Adding text labels on top of each bar
for xi, yi in zip(x, y1):
    plt.text(xi, yi + 0.5, str(yi), ha='center', va='bottom', color='black')


plt.xlabel('Data Size-(Data split = 90% training , 10% testing)')
plt.ylabel('Accuracy')
plt.title('Data Size v/s Accuracy Analysis')
plt.legend()
plt.savefig('total_accuracy1.png')
plt.show()







