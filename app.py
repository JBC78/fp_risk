from flask import Flask, render_template, request
import joblib
import pandas as pd
import nltk
#  put back when deploying Heroku the nltk punkt, stopwords and wordnet
nltk.download('punkt') 
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
# Multinomial Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB

# Import Tf-idf Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Import the Label Encoder
from sklearn.preprocessing import LabelEncoder

# create an server (app) using the Flask libabry
app = Flask(__name__)

# creat routes(end points) for the server
@app.route("/") # in our app, create a new route, called / 

#what will this route do
def home_page():
    print("Server received request for 'index page'...")
    return render_template("index.html")

# # about end point
# @app.route("/about")
# def about():
#     print("Server received request for 'About' page...")
#     return "Welcome to my 'About' page!"

@app.route("/visuals")
def visuals():
    return render_template("visuals.html")
# Define a function to returns only alphanumeric tokens
def alpha(tokens):
    """This function removes all non-alphanumeric characters"""
    alpha = []
    for token in tokens:
        if str.isalpha(token) or token in ['n\'t','won\'t']:
            if token=='n\'t':
                alpha.append('not')
                continue
            elif token == 'won\'t':
                alpha.append('wont')
                continue
            alpha.append(token)
    return alpha

# Define a function to remove stop words
def remove_stop_words(tokens):
    """This function removes all stop words in terms of nltk stopwords"""
    no_stop = []
    for token in tokens:
        if token not in stopwords.words('english'):
            no_stop.append(token)
    return no_stop

# Define a function to lemmatization
def lemmatize(tokens):
    """This function lemmatize the messages"""
    # Initialize the WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    # Create the lemmatized list
    lemmatized = []
    for token in tokens:
            # Lemmatize and append
            lemmatized.append(lemmatizer.lemmatize(token))
    return " ".join(lemmatized)

def clean_data(raw_text):
    tokenized_message = word_tokenize(raw_text.lower())
    tokenized_message = alpha(tokenized_message)
    tokenized_message = remove_stop_words(tokenized_message)
    tokenized_message = lemmatize(tokenized_message)
    vectorizer = joblib.load("vectorizer.pkl")
    clean_message = vectorizer.transform([tokenized_message])
    return clean_message

@app.route("/api/predict", methods =["POST"])
def risk_predicter():
    user_scope_input = request.get_json()
    print(user_scope_input["risk_scope"])
    model = joblib.load("naive_bayes.pkl")
    cleaned_message = clean_data(user_scope_input["risk_scope"])
    print(cleaned_message)
    prediction_class = model.predict(cleaned_message)
    print(prediction_class)
    if prediction_class[0]==0 :
        prediction = "High"
    elif prediction_class[0]==1 :
        prediction = "Low"
    elif prediction_class[0]==2 :
        prediction = "Medium"
    else :
        prediction = "Prediction Unknown"
    print(prediction)
    return {"prediction": prediction}

@app.route("/risk_classifier")
def risk_classifier():
    return render_template("risk_classifier.html")

# start the server
if __name__ == "__main__":
    app.run(debug=True)