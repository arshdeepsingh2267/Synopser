from flask import Flask,url_for,render_template,request
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


stopwords=list(STOP_WORDS)
nlp=spacy.load('en_core_web_md')
punctuation = punctuation + '\n'


app = Flask(__name__)
@app.route('/',methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/Summarize',methods=["GET","POST"])
def Summarize():
    if request.method == "POST":
        rawtext=request.form["rawtext"]
        doc=nlp(rawtext)
        #tokens = [token.text for token in doc]
        word_frequencies = {}
        for word in doc:
            if word.text.lower() not in stopwords:
                if word.text.lower() not in punctuation:
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] += 1
        
        max_freq = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word]/max_freq
        sentence_tokens = [sent for sent in doc.sents]
        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]
        select_length = int(len(sentence_tokens)*0.3)  #reduced to 30% of original text.
        summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
        final_summary= ''.join([word.text for word in summary])

        return render_template("index.html",summary=final_summary)
    else:
        return render_template("index.html")






if __name__ =="__main__":
    app.run(debug=True)