import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

# Function to install packages if not already installed
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])

# Ensure the required packages are installed
try:
    import requests
except ImportError:
    install_package("requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    install_package("beautifulsoup4")

try:
    import pandas as pd
except ImportError:
    install_package("pandas")

try:
    import openpyxl
except ImportError:
    install_package("openpyxl")

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define your functions for data extraction and analysis here

# Example function to extract article text
def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Adjust the selectors as per the website's structure
    title = soup.find('h1').get_text()
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    
    return title, text

# Example function to read URLs from an Excel file
def read_urls_from_excel(file_path):
    df = pd.read_excel(file_path)
    urls = df['URL'].tolist()
    return urls

if __name__ == "__main__":
    # Path to your input Excel file
    input_excel = 'c:/Users/pavan/Downloads/20211030 Test Assignment-20240724T054231Z-001/Assignment/Input.xlsx'
    urls = read_urls_from_excel(input_excel)
    
    for url in urls:
        title, text = extract_article_text(url)
        # Save the extracted text to a file named with URL_ID
        url_id = url.split('/')[-1]  # Example: extracting the last part of the URL as ID
        with open(f'{url_id}.txt', 'w', encoding='utf-8') as f:
            f.write(f"{title}\n\n{text}")
    
    # Add your text analysis code here
import subprocess
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from textblob import TextBlob

# Ensure nltk packages are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Function to install packages if not already installed
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])

# Ensure the required packages are installed
try:
    import requests
except ImportError:
    install_package("requests")

try:
    from bs4 import BeautifulSoup
except ImportError:
    install_package("beautifulsoup4")

try:
    import pandas as pd
except ImportError:
    install_package("pandas")

try:
    import openpyxl
except ImportError:
    install_package("openpyxl")

try:
    import textblob
except ImportError:
    install_package("textblob")

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define your functions for data extraction and analysis here

# Example function to extract article text
def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Adjust the selectors as per the website's structure
    title = soup.find('h1').get_text()
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    
    return title, text

# Example function to read URLs from an Excel file
def read_urls_from_excel(file_path):
    df = pd.read_excel(file_path)
    urls = df['URL'].tolist()
    url_ids = df['URL_ID'].tolist()  # Assuming there's a column named 'URL_ID'
    return urls, url_ids

# Text analysis functions
def get_positive_score(text, positive_words):
    words = word_tokenize(text)
    positive_score = sum(1 for word in words if word in positive_words)
    return positive_score

def get_negative_score(text, negative_words):
    words = word_tokenize(text)
    negative_score = sum(1 for word in words if word in negative_words)
    return negative_score

def get_polarity_score(positive_score, negative_score):
    return (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

def get_subjectivity_score(text):
    return TextBlob(text).sentiment.subjectivity

def get_avg_sentence_length(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return len(words) / len(sentences)

def get_percentage_of_complex_words(text):
    words = word_tokenize(text)
    complex_words = [word for word in words if get_syllable_count(word) > 2]
    return len(complex_words) / len(words)

def get_fog_index(avg_sentence_length, percentage_of_complex_words):
    return 0.4 * (avg_sentence_length + percentage_of_complex_words)

def get_avg_number_of_words_per_sentence(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return len(words) / len(sentences)

def get_complex_word_count(text):
    words = word_tokenize(text)
    complex_words = [word for word in words if get_syllable_count(word) > 2]
    return len(complex_words)

def get_word_count(text):
    words = word_tokenize(text)
    return len(words)

def get_syllable_count(word):
    word = word.lower()
    syllables = re.findall(r'[aeiouy]+', word)
    return len(syllables)

def get_personal_pronouns(text):
    words = word_tokenize(text.lower())
    personal_pronouns = [word for word in words if word in ['i', 'we', 'my', 'ours', 'us']]
    return len(personal_pronouns)

def get_avg_word_length(text):
    words = word_tokenize(text)
    total_length = sum(len(word) for word in words)
    return total_length / len(words)

if __name__ == "__main__":
    # Path to your input Excel file
    input_excel = 'c:/Users/pavan/Downloads/20211030 Test Assignment-20240724T054231Z-001/Assignment/Input.xlsx'
    urls, url_ids = read_urls_from_excel(input_excel)
    
    # Read positive and negative words
    with open('c:/Users/pavan/Downloads/20211030 Test Assignment-20240724T054231Z-001/Assignment/MasterDictionary/positive-words.txt', 'r') as f:
        positive_words = set(f.read().split())
        
    with open('c:/Users/pavan/Downloads/20211030 Test Assignment-20240724T054231Z-001/Assignment/MasterDictionary/negative-words.txt', 'r') as f:
        negative_words = set(f.read().split())
    
    # DataFrame to store the results
    results = []

    for url, url_id in zip(urls, url_ids):
        title, text = extract_article_text(url)
        
        # Perform text analysis
        positive_score = get_positive_score(text, positive_words)
        negative_score = get_negative_score(text, negative_words)
        polarity_score = get_polarity_score(positive_score, negative_score)
        subjectivity_score = get_subjectivity_score(text)
        avg_sentence_length = get_avg_sentence_length(text)
        percentage_of_complex_words = get_percentage_of_complex_words(text)
        fog_index = get_fog_index(avg_sentence_length, percentage_of_complex_words)
        avg_number_of_words_per_sentence = get_avg_number_of_words_per_sentence(text)
        complex_word_count = get_complex_word_count(text)
        word_count = get_word_count(text)
        syllable_per_word = get_syllable_count(text) / word_count
        personal_pronouns = get_personal_pronouns(text)
        avg_word_length = get_avg_word_length(text)
        
        # Save results
        result = {
            'URL_ID': url_id,
            'URL': url,
            'POSITIVE SCORE': positive_score,
            'NEGATIVE SCORE': negative_score,
            'POLARITY SCORE': polarity_score,
            'SUBJECTIVITY SCORE': subjectivity_score,
            'AVG SENTENCE LENGTH': avg_sentence_length,
            'PERCENTAGE OF COMPLEX WORDS': percentage_of_complex_words,
            'FOG INDEX': fog_index,
            'AVG NUMBER OF WORDS PER SENTENCE': avg_number_of_words_per_sentence,
            'COMPLEX WORD COUNT': complex_word_count,
            'WORD COUNT': word_count,
            'SYLLABLE PER WORD': syllable_per_word,
            'PERSONAL PRONOUNS': personal_pronouns,
            'AVG WORD LENGTH': avg_word_length
        }
        results.append(result)
    
    # Convert results to DataFrame and save to Excel
    results_df = pd.DataFrame(results)
    results_df.to_excel('Output Data Structure.xlsx', index=False)
