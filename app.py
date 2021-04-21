import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__, template_folder='template')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method=='POST':
        input = request.form

        text =(input['text'])
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for token in doc]
    asd = punctuation + '\n' + '\n\n'

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in asd:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text]=1
                else:
                    word_frequencies[word.text]+=1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
                
    sentence_tokens = [sent for sent in doc.sents]

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    select_length = int(input['sentences'])
    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)
    result = summary.replace('\n','<br>')
    return render_template('result.html', data=input, pred=result)

if __name__ == '__main__':

    port = int(os.environ.get('PORT',5000))
    app.run(debug=True,host='0.0.0.0',port=port)