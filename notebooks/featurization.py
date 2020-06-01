import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import WordPunctTokenizer
from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from bs4 import BeautifulSoup
import re

def init_char_tokenizer(df):
    char_tokenizer=Tokenizer(char_level=True)
    char_tokenizer.fit_on_texts(str(df["text"]))
    return char_tokenizer

def get_char_tokens(string, char_tokenizer):
    return char_tokenizer.texts_to_sequences([str(string)])[0]

def get_bigrams(string):
    try:
        tokenizer = WordPunctTokenizer()
        tokens = tokenizer.tokenize(string)
        stemmer = PorterStemmer()
        bigram_finder = BigramCollocationFinder.from_words(tokens)
        bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 500)

        for bigram_tuple in bigrams:
            x = "%s %s" % bigram_tuple
            tokens.append(x)

        result = [' '.join([stemmer.stem(w).lower() for w in x.split()]) for x in tokens if x.lower() not in stopwords.words('english') and len(x) > 8]
        return result
    except:
        return None

def init_perma_age_gender():
    age_lexi=pd.read_csv("emnlp14age.csv")
    gender_lexi=pd.read_csv("emnlp14gender.csv")
    perma_lexi = pd.read_csv("permaV3_dd.csv")

    age_dict={}
    for i in range (int(age_lexi.size/2)):
        word=age_lexi.iloc[i]['term']
        weight=age_lexi.iloc[i]['weight']
        age_dict[word]=weight

    gender_dict={}
    for i in range (int(gender_lexi.size/2)):
        word=gender_lexi.iloc[i]['term']
        weight=gender_lexi.iloc[i]['weight']
        gender_dict[word]=weight

    category_dict={}
    perma_dict={} 
    for i in range (int(perma_lexi.size/3)):
        word=perma_lexi.iloc[i]['term']
        category=perma_lexi.iloc[i]['category']
        if(category not in category_dict):
            category_dict[category]=1
        weight=perma_lexi.iloc[i]['weight']
        if(word not in perma_dict):
            perma_dict.setdefault(word,{})[category]=weight
        else:
            perma_dict[word][category]=weight


    return age_dict, gender_dict, category_dict, perma_dict



def get_age(string, age_dict):
    try:
        text=string.lower()
        text=text.split()
        help_dict={}
        total_word=0

        for word in text:
            if word in age_dict:
                total_word+=1
                if word not in help_dict: help_dict[word]=1
                else: help_dict[word]+=1
        
        age=age_dict['_intercept']

        for word in help_dict: age+=age_dict[word]*help_dict[word]/total_word
            
        return int(age)
    except:
        return None



def get_gender(string, gender_dict):

    try:
        text=string.lower()
        text=text.split()
        help_dict={}
        total_word=0
        for word in text:
            if word in gender_dict:
                total_word+=1
                if word not in help_dict:
                    help_dict[word]=1
                else:
                    help_dict[word]+=1
        gender=gender_dict['_intercept']
        for word in help_dict:
            gender+=gender_dict[word]*help_dict[word]/total_word
        if gender>0:
            gender=1
        else:
            gender=-1
            
        return gender
    except:
        return None
    
    

        
def get_perma(string,category, perma_dict):
    try:
        text=string.lower()
        text=text.split()
        score=0
        for word in text:
            if word in perma_dict:
                if category in perma_dict[word]:
                    score+=perma_dict[word][category]
            
        return score
    except:
        return None
    

def clean_text(raw_review):
    # Remove HTML
    review_text = BeautifulSoup(raw_review, 'lxml').get_text() 
    # Remove non-letters        
    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
    # Convert to lower case, split into individual words
    words = letters_only.lower().split()   
    # Remove stop words (use of sets makes this faster)
    stops = set(stopwords.words("english"))                  
    meaningful_words = [w for w in words if not w in stops and len(w) > 4]                             
    return ( " ".join( meaningful_words )) 

def apply_cleaning_function_to_series(X):
    print('Cleaning data')
    cleaned_X = []
    for element in X:
        cleaned_X.append(clean_text(element))
    print ('Cleaning finished')
    return cleaned_X
