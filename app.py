from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)

def load_words_from_csv(file_path):
    words = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            words.append(row['word'])
    return words

def search_words(pattern, word_list):
    matching_words = []
    for word in word_list:
        if len(word) == len(pattern):
            match = True
            for i in range(len(pattern)):
                if pattern[i] != '_' and pattern[i].lower() != word[i].lower():
                    match = False
                    break
            if match:
                matching_words.append(word)
    return matching_words

# Load the word list from CSV file
word_list = load_words_from_csv('example_dataset.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_pattern = request.form['search_pattern']
        results = search_words(search_pattern, word_list)
        return render_template('search_results.html', results=results)
    last_updated = get_last_updated()
    return render_template('search.html', last_updated=last_updated)

def get_last_updated():
    # Replace this with the actual logic to fetch the last updated timestamp from the GitHub repository
    # For demonstration purposes, we'll use the current timestamp
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/search', methods=['POST'])
def search():
    search_pattern = request.form['search_pattern']
    results = search_words(search_pattern, word_list)
    return render_template('search_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)