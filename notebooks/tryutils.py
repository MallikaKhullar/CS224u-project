from collections import Counter 
from types import SimpleNamespace
import json 
import requests
import csv
import time
from collections import Counter
import pandas as pd
import datetime as dt #only if you want to analyze the date created feature
import json 
from types import SimpleNamespace
import sys
from nltk.tokenize import TreebankWordTokenizer
from textblob import TextBlob
from tabulate import tabulate
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords

class SetEncoder(json.JSONEncoder):
    '''Using SetEncoder to JSONify our individual result sets'''
    def default(self, obj):
        if isinstance(obj, set): return list(obj)
        return json.JSONEncoder.default(self, obj)

SUBS_MEN = ['ROCD', 'AvPD','selfharm', 'bipolar', 'CPTSD', 'BPD', 
'MentalHealthSupport','antidepressants','medical_advice',
'raisedbynarcissists','GeneticCounseling','ADHDAccountability',
'Dissociation', 'depression', 'SuicideWatch', 'OCD' , 'TrueOffMyChest', 
'mentalhealth', 'offmychest', 'emotionalsupport', 'therapy', 'ADHD',
'AskDocs', 'dpdr', 'emetophobia', 'Agoraphobia','Tokophobia','depressed']

SUBS_ANX = ['zoloft', 'Gad', 'Anxietyhelp', 'PanicAttack', 'Anxiety', 
'AnxietyDepression', 'socialanxiety', 'HealthAnxiety', 
'panicdisorder', 'PanicParty']

def get_fresh_counters(): 
   counter_men = Counter()
   counter_unr = Counter()
   counter_anx = Counter()
   posts_men = []
   posts_anx = []
   posts_unr = []

   categories = SimpleNamespace(**{
      
      'unr': SimpleNamespace(**{
         'type': 'unr',
         'counter': counter_unr,
         'result_list': posts_unr,
         'file_name': 'posts-unr.json'
      }),
      
      'men': SimpleNamespace(**{
         'type': 'men',
         'counter': counter_men,
         'result_list': posts_men,
         'file_name': 'posts-men.json'
      }),
      
      'anx': SimpleNamespace(**{
         'type': 'anx',
         'counter': counter_anx,
         'result_list': posts_anx,
         'file_name': 'posts-anx.json'
      })
   })

   return categories

def get_dict_from_submission(submission,  user):
    try:
        sub_dict = {'sub': submission.subreddit.display_name, \
                'title': submission.title, \
                'body' : submission.selftext, \
                'num_u' : submission.score, \
                'url' : submission.url, \
                'num_c' : submission.num_comments, \
                'time': submission.created, \
                'user': user
        }
    except:
        print("Error has occured here")
        
    return sub_dict


def process_user(user, user_count, n):
    print_progress(user_count, n)
    user_count += 1
    return user_count

def init_vars():
    return [],0,0

def print_progress(user_count, n):
    if user_count%4==0:  
      print("{}/{} users".format(user_count, n), end='\r', flush=True)

def dump_data(file_name, data):
    if isinstance(data, set): data = json.dumps(data, cls=SetEncoder) # if set, first encode
        
    with open(file_name, 'w') as fp:
        json.dump(data, fp)

def get_post_type(sub, categories):
    if sub in SUBS_ANX: return categories.anx.type
    elif sub in SUBS_MEN: return categories.men.type
    else: return categories.unr.type

def process_for_category(post, sub, categories):
   if sub in SUBS_ANX:
      categories.anx.counter[sub] += 1
      categories.anx.result_list.append(post)
         
   elif sub in SUBS_MEN:
      categories.men.counter[sub] += 1
      categories.men.result_list.append(post)

   else: 
      categories.unr.counter[sub] += 1
      categories.unr.result_list.append(post)
   return categories

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def bprint(string):
    print(color.BOLD + string + color.END)

def grey_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    return "hsl(0, 0%%, %d%%)" % 0

def show_cloud(words):
    d = {}
    for a, x in words:
        d[a] = x

    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    wordcloud = WordCloud()
    wordcloud.prefer_horizontal = 1
    wordcloud.width = 800
    wordcloud.height= 800
    wordcloud.background_color = 'white'
    wordcloud.generate_from_frequencies(frequencies=d)
    
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud.recolor(color_func=grey_color_func, random_state=3), interpolation="bilinear")
    plt.axis("off")
    plt.show()