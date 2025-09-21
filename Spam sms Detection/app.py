from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import re
import string

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages

# Load and train the model
data = pd.read_csv('spam.csv', encoding='latin-1')
data.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace=True)
data.columns = ['label', 'message']
data['label'] = data['label'].map({'spam': 1, 'ham': 0})

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(data['message'])
y = data['label']
classifier = MultinomialNB()
classifier.fit(X, y)

spam_keywords_list = [
    "free", "free money", "earn cash", "winner", "prize", "free gift", "claim your prize", "urgent",
    "limited time offer", "buy now", "risk-free", "congratulations", "free access", "act now", 
    "exclusive deal", "click here", "offer expires", "100% free", "get paid", "guaranteed", 
    "free consultation", "discount", "cash prize", "free trial", "exclusive offer", "limited offer",
    "fast cash", "cash grant", "special offer", "winner notification", "restricted access", "easy money", 
    "confirm your win", "final notice", "last chance", "unsecured loan", "emergency funds", "get rich quick",
    "earn money from home", "invest now", "earn big", "make money fast", "prize money", "free rewards",
    "free holiday", "free course", "get instant cash", "free entry", "exclusive access", "fast loan",
    "best offer", "exclusive discount", "fast loan approval", "guaranteed cash"
]


def check_explicit_spam_words(message):
    return any(keyword in message.lower() for keyword in spam_keywords_list)

suspicious_links_list = [
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "shorturl.at", "rebrand.ly", "shorte.st", 
    "snip.ly", "adf.ly", "is.gd", "cutt.ly", "zurl.co", "linktr.ee", "clicky.me", "click2sell.eu", 
    "bit.do", "q.gs", "clck.ru", "shortlink.com", "t.ly", "linkr.in", "ht.ly", "zippyshare.com", 
    "sharinglinks.net", "linkinghub.com", "track.click", "shrinkme.io", "freeclick.com", "claimreward.com",
    "sharecash.org", "clicktospam.com", "rewardscenter.com", "cashreward.link", "getmoneyclicks.com", 
    "quickclicks.net", "special-offers.com", "hurryclick.com", "prize-clicks.com", "getpaidfast.com", 
    "easyearnclicks.com", "quickcashnow.com", "reward4you.com", "earn-from-links.com", "money4click.com",
    "clicktospam.net", "getclickpay.com", "fastmoneylink.com", "instantcash4you.com"
]


def check_suspicious_links(message):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    return any(domain in url for domain in suspicious_links_list for url in urls)

def check_unusual_characters(message):
    return any(char not in string.printable for char in message)

personal_info_requests_list = [
    "social security number", "credit card number", "bank account number", "password", "PIN", 
    "security code", "account number", "tax ID", "driver's license number", "routing number", 
    "personal identification number", "SSN", "date of birth", "mother's maiden name", "address", 
    "telephone number", "email address", "security question", "medical records", "biometric data", 
    "paypal", "bank details", "credit card", "online banking", "personal ID", "account details", 
    "ATM number", "personal question", "password reset", "verify account", "login details", "recovery key",
    "account security", "card verification", "account verification", "unlock code", "account recovery", 
    "identity verification", "bank pin", "secure payment", "email verification", "identity theft", 
    "payment information", "bank login", "credit score", "mobile number", "personal email", "contact information",
    "bank security", "account recovery code", "security check", "access code"
]


def check_personal_info_request(message):
    return any(keyword in message.lower() for keyword in personal_info_requests_list)

urgency_keywords_list = [
    "urgent","urgent action required", "immediate response needed", "act now", "limited time", "last chance", 
    "deadline approaching", "response required", "time-sensitive", "urgent request", "immediate attention", 
    "act fast", "instant", "quickly", "now or never", "important information", "limited offer", "final notice", 
    "expires soon", "don't miss out", "hurry up", "final call", "immediate response", "urgent update", 
    "urgent deadline", "take action now", "time is running out", "limited availability", "final opportunity",
    "secure your spot", "don't wait", "only a few left", "urgent offer", "last minute", "immediate reply", 
    "act quickly", "quick response", "last chance to claim", "urgent notification", "hurry before it’s too late", 
    "almost gone", "urgent notification", "fast action required", "quick decision needed", "immediate attention required",
    "don’t miss out", "act immediately", "response needed now", "flash sale", "limited stock"
]


def check_urgency(message):
    return any(keyword in message.lower() for keyword in urgency_keywords_list)

def check_spam_heuristics(message):
    score = 0
    factors = []
    if check_explicit_spam_words(message):
        score += 1
        factors.append("Spam-related keywords detected.")
    if check_suspicious_links(message):
        score += 2
        factors.append("Suspicious links detected.")
    if check_unusual_characters(message):
        score += 2
        factors.append("Unusual characters found.")
    if check_personal_info_request(message):
        score += 3
        factors.append("Personal information request detected.")
    if check_urgency(message):
        score += 2
        factors.append("Urgency detected in the message.")
    return score, factors

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/check')
def check():
    return render_template('check.html')

@app.route('/process')
def process():
    return render_template('process.html')

@app.route('/predict', methods=['POST'])
def predict():
    message = request.form['message']
    message_vec = vectorizer.transform([message])
    nb_prediction = classifier.predict(message_vec)[0]
    
    # Heuristic spam check
    score, factors = check_spam_heuristics(message)
    is_spam = (nb_prediction == 1 or score >= 4)

    if is_spam:
        return redirect(url_for('why', message=message, spam=is_spam, nb_prediction=nb_prediction, factors=";".join(factors)))
    else:
        flash('This message is classified as NOT SPAM. You can check another message.', 'success')
        return redirect(url_for('check'))

@app.route('/why')
def why():
    message = request.args.get('message', '')
    spam = request.args.get('spam') == 'True'
    nb_prediction = request.args.get('nb_prediction')
    factors = request.args.get('factors', '').split(';')
    
    return render_template('why.html', factors=factors, message=message, spam=spam, nb_prediction=nb_prediction)

if __name__ == '__main__':
    app.run(debug=True)
