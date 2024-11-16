# -*- coding: utf-8 -*-
"""NLP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w9Wcb6SdN3Ll7ZNvZo9fZp2WikEm6fjL
"""

import numpy as np
import pandas as pd

df = pd.read_csv("/content/drive/MyDrive/Data Science/project/spam-vs-ham-dataset.csv")

df.head()

df.tail()

df.shape

df.columns

df['Label'].value_counts()

df.info()

df.isnull().sum()

df.duplicated().sum()

df.drop_duplicates(inplace=True)

df.shape

import seaborn as sns
import matplotlib.pyplot as plt

# Visualizing the distribution of labels
sns.countplot(x='Label', data=df, hue='Label', palette='viridis', edgecolor='black', legend=False)
plt.title('Distribution of Spam and Ham Labels', fontsize=16, fontweight='bold')
plt.xlabel('Label', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()

# text preprocessing
text = df['Text']

type(text)

text1=[]

# leaning and preprocessing the text data
import re

for txt in df['Text']:
    # Convert to lowercase anf remove spcl characters
    txt = txt.lower()
    txt = re.sub(r'<br\s*/?>', ' ', txt)
    txt = re.sub(r'\W', ' ', txt)
    txt = re.sub(r'\d', ' ', txt)
    txt = re.sub(r'\s+', ' ', txt).strip()
    # Append cleaned text to text1
    text1.append(txt)

text1

text=pd.Series(text1)

import nltk
nltk.download('punkt_tab')

from nltk.tokenize import word_tokenize
text = text.apply(lambda x:' '.join([w for w in word_tokenize(x) if len(w)>=3]))

text

# lowecase conversion and normalization(convert in to root form or cut the tail part)
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('english')
text = text.apply(lambda x:[stemmer.stem(i.lower()) for i in word_tokenize(x)]).apply(lambda x:' '.join(x))

text

nltk.download('stopwords')

from nltk.corpus import stopwords
stop = stopwords.words('english')
text = text.apply(lambda x:[i for i in word_tokenize(x) if i not in stop]).apply(lambda x:' '.join(x))

text

# feature extraction usig TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
vec = TfidfVectorizer()
train_data_vec = vec.fit_transform(text)

print(train_data_vec)

train_data_vec.shape

y = df['Label'].values

print(y)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(train_data_vec,y,test_size=0.2,random_state=0)

# Logistic Regression

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(x_train,y_train)

y_pred = model.predict(x_test)
y_pred

# evaluating logistic regression

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
print("Accuracy:", accuracy_score(y_test, y_pred))

print("*"*60)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("*"*60)

print("Classification Report for Logistic Regression:")
print(classification_report(y_test, y_pred))

# Naive Bayes Model

from sklearn.naive_bayes import MultinomialNB
model1 = MultinomialNB()
model1.fit(x_train,y_train)

y_pred1 = model1.predict(x_test)
y_pred1

# evaluating logistic regression

print("Accuracy:", accuracy_score(y_test, y_pred1))

print("*"*60)

print("Confusion Matrix:")
cm=confusion_matrix(y_test, y_pred1)
print(cm)

print("*"*60)

print("Classification Report for Naive Bayes:")
print(classification_report(y_test, y_pred1))

# Plot the confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Spectral')
plt.xlabel('Predicted Spam/Ham', fontsize=14)
plt.ylabel('True Spam/Ham', fontsize=14)
plt.title('Confusion Matrix for Naive Bayes Model', fontsize=16, fontweight='bold')
plt.xticks([0.5, 1.5], ['Ham', 'Spam'], fontsize=12)
plt.yticks([0.5, 1.5], ['Ham', 'Spam'], fontsize=12, rotation=0)
plt.show()

# New prediction
sample = "Congratulations! You've won a free ticket to Bahamas. Call now!"

print("The result of sample message :  " ,model1.predict(vec.transform([sample])))