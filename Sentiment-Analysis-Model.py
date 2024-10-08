# -*- coding: utf-8 -*-
"""NLP Final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EW7fv2bRwNOvZqDbIZdmloVRlR7tW7mQ

Q.1 About The Company & How Can This Help The Our Company?

Ans. IMDb (Internet Movie Database) well defined by it's name most renouned website for movie ratings; as their newly appointed data scientist i've built a pipeline which helps to understand customer sentiments and by utlizing this we can introduce a Movie Recommendation System which could enhance the user experience and benefit industry stakeholders, including filmmakers, studios, distributors, and advertisers.

Understanding customer sentiment could be crucial for a company like IMDb. By analyzing these reviews, the company can understand audience reactions, improve marketing strategies, and enhance user experience. Solving this problem will help in monitoring the brand reputation, improving suggestions for existing users, and increasing customer satisfaction. Further can come up as promoters and do promotion campaigns for Film/ Entertainment industry with the help of this data.

The main components of this NLP system are:
1. Data Collection: Gathering IMDb data (reviews).
2. Data Preprocessing: Cleaning and preparing the text data for analysis.
3. Feature Extraction: Converting text data into numerical representations using TF-IDF vectorization.
4. Model Training: Training machine learning models to classify sentiments with Linear Regession (Traditional) & Neural Networks.
5. Evaluation: Assessing the performance of both models using appropriate metrics.
6. Deployment: Using the trained model to predict sentiments of new given reviews.

##Library

Importing all the required libraries including nltk for this NLP System and downloading packages.
"""

import pandas as pd
import numpy as np
import re
import string
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from sklearn.model_selection import train_test_split
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import seaborn as sns
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import scipy

nltk.download('punkt')
nltk.download('stopwords')

"""##Dataset Loading

Loading the IMDb dataset. from kaggle https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews
"""

df = pd.read_csv("/content/IMDB Dataset.csv")
df

"""##Data Exploration

In this part i'm basically exploring data by using some functions such as

shape to check no. of rows and columns.

info for data information (data types, missing values).

value count to analyzes sentiment distribution (positive vs. negative reviews).

bar chart to visualize sentiment distribution.

looking for any missing values and duplicate rows.
"""

df.shape

df.info()

df['sentiment'].value_counts()

from matplotlib import pyplot as plt
import seaborn as sns
df.groupby('sentiment').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
plt.gca().spines[['top', 'right',]].set_visible(False)

missing_values = df.isnull().sum()
print(missing_values)

duplicate_rows = df.duplicated().sum()
print("Number of duplicate rows:", duplicate_rows)

"""##Data Pre-Processing

cleaning up the data by removing the duplicates.
"""

df.drop_duplicates(inplace=True)

duplicate_rows = df.duplicated().sum()
print("Number of duplicate rows:", duplicate_rows)

"""##Spliting Dataset

here i split my data into training and testing sets for model evaluation (80% training, 20% testing) of the whole.
"""

X_train_raw, X_test_raw, y_train, y_test = train_test_split(df['review'], df['sentiment'].apply(lambda x: 1 if x == 'positive' else 0), test_size=0.2, random_state=42)

"""##Text Pre-Processing

Created a function clean_text to perform multiple tasks to clean the text in my data.

Removed HTML tags using BeautifulSoup.

Converted text to lowercase.

Removed special characters and numbers using regular expressions.

Tokenized text into words using nltk.

Removed stop words (common words like "the","in") using nltk.

Joined tokens back into a cleaned text string.

Applied the clean_text function to both training and testing sets.
"""

def clean_text(text):

    text = BeautifulSoup(text, 'html.parser').get_text()
    text = text.lower()
    text = re.sub(f'[{string.punctuation}]', '', text)
    text = re.sub('\d+', '', text)
    tokenized_text = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokenized_text = [word for word in tokenized_text if word not in stop_words]
    return ' '.join(tokenized_text)

df['processed_text'] = df['review'].apply(clean_text)
print("Shape after processing:", df.shape)
df.head()

"""lets take look at how long the reviews are in general and create a graph histogram that shows how many reviews fall into different ranges of lengths."""

df['review_length'] = df['review'].apply(len)
sns.histplot(df['review_length'], bins=50, kde=True)
plt.title('Review Length Distribution')
plt.xlabel('Review Length')
plt.ylabel('Frequency')
plt.show()

"""combines processed text from a DataFrame column into a single string and divides the merged string into individual tokens, or words. then creates a dictionary where each word is a key and its count is its value by counting the frequency of each term"""

all_words = ' '.join(df['processed_text']).split()
word_freq = Counter(all_words)

common_words = word_freq.most_common(20)
common_df = pd.DataFrame(common_words, columns=['Word', 'Frequency'])
sns.barplot(x='Frequency', y='Word', data=common_df)
plt.title('Most Common Words')
plt.show()

"""##Feature Extraction

This tool TfidfVectorizer to convert text to numbers features,
next training data to acquire crucial vocabulary (fit) and converts textual data for testing (X_test) and training (X_train) into numerical features according to word significance.
"""

tfidf = TfidfVectorizer(max_features=5000)
X_train = tfidf.fit_transform(X_train_raw).toarray()
X_test = tfidf.transform(X_test_raw).toarray()

"""##Model Training

training the Logistic Regression model majorly for the comparission with my neural network model also had to increase the amount of iters from 100 (Default) to 500
"""

lr_model = LogisticRegression(max_iter=500)
lr_model.fit(X_train, y_train)

"""Training neural networkk model"""

nn_model = Sequential()
nn_model.add(Dense(512, activation='relu', input_dim=5000))
nn_model.add(Dropout(0.5))
nn_model.add(Dense(256, activation='relu'))
nn_model.add(Dropout(0.5))
nn_model.add(Dense(1, activation='sigmoid'))
nn_model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
nn_model.fit(X_train, y_train, epochs=50, batch_size=75, validation_data=(X_test, y_test))

"""Predicting and evaluating for both my models Logistic Regression model and Neural Networks model using appropriate metrics."""

y_pred_lr = lr_model.predict(X_test)
accuracy_lr = accuracy_score(y_test, y_pred_lr)
precision_lr = precision_score(y_test, y_pred_lr)
recall_lr = recall_score(y_test, y_pred_lr)
f1_lr = f1_score(y_test, y_pred_lr)

y_pred_nn = (nn_model.predict(X_test) > 0.5).astype("int32")
accuracy_nn = accuracy_score(y_test, y_pred_nn)
precision_nn = precision_score(y_test, y_pred_nn)
recall_nn = recall_score(y_test, y_pred_nn)
f1_nn = f1_score(y_test, y_pred_nn)

print(f'Logistic Regression - Accuracy: {accuracy_lr}, Precision: {precision_lr}, Recall: {recall_lr}, F1 Score: {f1_lr}')
print(f'Neural Network - Accuracy: {accuracy_nn}, Precision: {precision_nn}, Recall: {recall_nn}, F1 Score: {f1_nn}')

"""form before results have improved but still there is not much of difference

Visualization creates a comparision of performance metrics of two models Logistic Regression and Neural Network and as we can see there is not much difference.
"""

metrics = pd.DataFrame({
    'Metric': ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
    'Logistic Regression': [accuracy_lr, precision_lr, recall_lr, f1_lr],
    'Neural Network': [accuracy_nn, precision_nn, recall_nn, f1_nn]
})

modelM = metrics.melt(id_vars='Metric', var_name='Model', value_name='Score')

sns.barplot(x='Score', y='Metric', hue='Model', data=modelM)
plt.title('Model Performance Metrics')
plt.show()

"""Deploying the model and testing by 2 of my reviews"""

reviews = ["john's role was a disaster and the location for this movie is just not suitable", "Rick And Morty are the best"]

for review in reviews:
  processed_review = clean_text(review)
  vectorized_review = tfidf.transform([processed_review])
  vectorized_review.sort_indices()
  predicted_score = nn_model.predict(vectorized_review)
  predicted_sentiment = "positive" if predicted_score > 0.5 else "negative"
  print(f"review: {review}")
  print(f"Predicted Sentiment: {predicted_sentiment}")

"""##Discission

>Strengths and Limitations

Strengths:-
1. This NLP system is accurately processing and classifying given reviews.
2. The combination of logistic regression and neural network models provides a strong and steady performance.

Limitations:-
1. The neural network model requires more computational resources compared to traditional models, it is usually time taking and long procedures for improvements you need lot of experimenting.

2. The systm may need re-training with new and large data to maintain its accuracy over time.

>Implications for the Business Problem

By implementing this NLP pipeline system, IMDb can gain valuable insights into customers emotions, enhancing their ability to tailor marketing strategies and improve user-experience. This sentiment analysis can drive better movie recommendations and targeted advertising campaigns, ultimately benefiting filmmakers, studios, distributors, and advertisers.

>Data-Driven Recommendations

1. Continuous Monitoring and Improvement: Regularly update the model with new reviews to maintain accuracy and relevance.
2. Expand Features: Incorporate more advanced NLP techniques like word embeddings or transformer-based models for potentially better performance.
3. User Feedback: Implement a feedback mechanism to gather user responses and further refine the recommendation system based on sentiment analysis.

This comprehensive pipeline not only addresses the business problem but also lays the foundation for continuous improvement and adaptation in the dynamic field of sentiment analysis.

##Conclusion

This NLP sentiment analysis model of IMDb movie reviews is a vital task for enhancing user-experience and providing valuable analytics for industry stakeholders. Here are the key takeaways :

1.Comprehensive Data Collection: IMDb already should have a pile of data

2.Robust Preprocessing: Using traditional method and neural networks this pipeline is providing quite accurate results.

3.Improved User Experience: By understanding customer emotions, IMDb can refine its recommendation system, offering more personalized and satisfying experiences for users.

4.Enhanced Marketing Strategies: Insights from sentiment analysis can inform marketing campaigns, helping target the right audience.

5.Brand Reputation Management: Monitoring sentiments trend allows IMDb to proactively manage its brand reputation, addressing negative sentiments promptly.

overall this pipeline provides a strongg framework and base for leveraging IMDb movie reviews to gain value business insights. By combining traditional machine learning techniques with advanced neural networks, we have accuracy and efficiency within this model. Continuous improvements will ensure that the system remains relevant and effective in meeting business objectives.

Refrences: https://www.tensorflow.org/tutorials/quickstart/beginner,
https://www.kaggle.com/,https://www.imdb.com/,https://en.wikipedia.org/wiki/IMDb.
"""