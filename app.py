from flask import Flask, request, jsonify, render_template
from difflib import SequenceMatcher
from transformers import pipeline
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt')

app = Flask(__name__)

# Load paraphrasing model
paraphraser = pipeline("text2text-generation", model="t5-small")

# Load text database from a file
with open('text_database.txt', 'r') as f:
    text_database = f.read().splitlines()

# Function to calculate similarity
def calculate_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

# Function to check plagiarism
def check_sentence_plagiarism(sentence):
    max_similarity = 0
    for db_sentence in text_database:
        similarity = calculate_similarity(sentence, db_sentence)
        max_similarity = max(max_similarity, similarity)
    return max_similarity

# Function to rewrite sentences
def rewrite_sentence(sentence):
    response = paraphraser(sentence, max_length=200, num_return_sequences=1)
    return response[0]['generated_text']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism():
    input_text = request.form['text']
    sentences = sent_tokenize(input_text)

    plagiarized_sentences = []
    unique_sentences = []
    plagiarism_score = 0
    total_sentences = len(sentences)

    for sentence in sentences:
        similarity = check_sentence_plagiarism(sentence)
        if similarity > 0.3:  # Define plagiarism threshold
            plagiarized_sentences.append((sentence, similarity))
        else:
            unique_sentences.append(sentence)
        plagiarism_score += similarity

    plagiarism_percentage = (plagiarism_score / total_sentences) * 100
    unique_percentage = 100 - plagiarism_percentage

    return jsonify({
        'plagiarism_percentage': plagiarism_percentage,
        'unique_percentage': unique_percentage,
        'plagiarized_sentences': plagiarized_sentences,
        'unique_sentences': unique_sentences
    })

@app.route('/remove_plagiarism', methods=['POST'])
def remove_plagiarism():
    input_text = request.form['text']
    sentences = sent_tokenize(input_text)

    rewritten_paragraph = []
    for sentence in sentences:
        similarity = check_sentence_plagiarism(sentence)
        if similarity > 0.3:  # Rewrite only plagiarized sentences
            rewritten_sentence = rewrite_sentence(sentence)
            rewritten_paragraph.append(rewritten_sentence)
        else:
            rewritten_paragraph.append(sentence)

    return jsonify({
        'rewritten_text': " ".join(rewritten_paragraph)
    })

if __name__ == '__main__':
    app.run(debug=True)
