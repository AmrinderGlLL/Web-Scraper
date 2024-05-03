# Import necessary modules
from flask import Flask, render_template
from bs4 import BeautifulSoup
import pandas as pd
import requests 
from collections import Counter
from nltk.corpus import stopwords

# Initialize Flask app
app = Flask(__name__)

# Function to scrape data from IMDb and generate review data
def get_data(url):
    data=[]
    # Make a GET request to the provided URL
    response = requests.get(url)
     
     # error handling
    if response.status_code == 200:
        # Parse the HTML content of the response using BeautifulSoup
        result = BeautifulSoup(response.content, "html.parser")
        # Find all review elements with the specified class
        reviews = result.find_all('div', class_='text show-more__control')

        # Iterate over each review element and extract review text
        for idx, revw in enumerate(reviews, 1):
            revNum = f"Review {idx}"  # Assign a review number
            review = revw.get_text(strip=True)  # Get review text
            data.append({"reviewNumber": revNum, "review": review})  # Append review data to list

    return data 

# Function to calculate word count statistics
def word_count_statistics(reviews):
    # Create a DataFrame from the review data
    df = pd.DataFrame(reviews)
    df['word_count'] = df['review'].apply(lambda x: len(x.split()))
    # Calculate average, maximum, and minimum word counts
    avg_word_count = df['word_count'].mean()
    max_word_count = df['word_count'].max()
    min_word_count = df['word_count'].min()
    return {
        'Average Word Count': avg_word_count,
        'Maximum Word Count': max_word_count,
        'Minimum Word Count': min_word_count
    }

# Function to find the most frequent words
def most_frequent_words(reviews, n=20):
    # Get English stopwords from NLTK
    stop_words = set(stopwords.words('english'))
    # Extract words from reviews, excluding stopwords
    words = [word.lower() for review_dict in reviews for word in review_dict['review'].split() if word.lower() not in stop_words]
    # Count occurrences of each word
    word_counts = Counter(words)
    # Get the top n most common words as a dictionary
    top_n_words = word_counts.most_common(n)
    return dict(top_n_words)

# Home page showing raw data
@app.route('/')
def show_raw_data():
    # Scrape raw data from IMDb and render the raw_data.html template
    raw_data = get_data("https://www.imdb.com/title/tt15239678/reviews/?ref_=tt_ql_2")
    return render_template('raw_data.html', raw_data=raw_data)

# Analysis page
@app.route('/analysis')
def show_analysis():
    raw_data = get_data("https://www.imdb.com/title/tt15239678/reviews/?ref_=tt_ql_2")
    # Calculate word count statistics
    word_count_stats = word_count_statistics(raw_data)
    # Find the most frequent words
    frequent_words = most_frequent_words(raw_data)
    # Render the analysis.html template with word count statistics and frequent words
    return render_template('analysis.html', word_count_stats=word_count_stats, frequent_words=frequent_words)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
