# Spam-Sms-Detection
Flask Spam Message Detector
A simple yet effective web application built with Flask to classify messages as Spam or Not Spam (Ham). This project uses a hybrid approach, combining a pre-trained machine learning model with a set of heuristic rules to enhance detection accuracy and provide clear, explainable results.

Features 
Hybrid Detection Model: Combines a Multinomial Naive Bayes classifier with a rule-based scoring system for robust analysis.

Heuristic Analysis: Scans messages for multiple common spam indicators:

Spammy keywords (e.g., 'free', 'prize', 'winner').

Suspicious links and URL shorteners (e.g., 'bit.ly').

Requests for sensitive personal information (e.g., 'password', 'credit card').

Urgency-inducing language (e.g., 'act now', 'limited time').

Unusual or non-printable characters.

Explainable Results: When a message is flagged as spam, the application details why by listing the specific rules that were triggered.

Simple Web Interface: Built with Flask and HTML for easy and intuitive interaction.

How It Works ⚙️
Every message submitted is analyzed by two main components running in the background:

Naive Bayes Classifier: A machine learning model, pre-trained on the spam.csv dataset, provides a probabilistic classification of the message.

Heuristic Engine: A custom scoring system checks the message against several lists of spam indicators. Each triggered rule adds to a total 'spam score'.

A message is ultimately flagged as SPAM if the Naive Bayes model predicts it as spam, OR if its heuristic score meets a predefined threshold (a score of 4 or higher). This dual approach helps catch a wider variety of spam that might be missed by a machine learning model alone.

Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
You need to have Python and pip installed on your system.

Installation
Clone the repository:


Bash

pip install Flask pandas scikit-learn
Ensure you have the dataset and HTML files:

Place the spam.csv dataset in the root directory of the project.

Make sure you have a templates folder containing the necessary HTML files (home.html, check.html, process.html, why.html).

Usage 
Run the Flask application from your terminal:

Bash

python app.py
(Replace app.py with the name of your Python script if it's different.)

Open your web browser and navigate to:

http://127.0.0.1:5000
Click through to the "Check Message" page, enter the text you want to analyze, and see the results!

File Structure 
.
├── app.py  
# Main Flask application logic
├── spam.csv 
# Dataset used for training the ML model
└── templates/
    
    ├── home.html      # Landing page
    
    ├── check.html     # Page with the input form for message checking
    
    ├── process.html   # (Optional) A page describing the process
    
    └── why.html       # Results page that explains why a message is spam
