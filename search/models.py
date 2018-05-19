# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import newspaper
import json

from django.db import models

# Create your models here.
class NewspaperArticle(models.Model):
    #domain = models.URLField()
    #article_text = models.TextField()
    #bias_score = models.DecimalField(max_digits=6, decimal_places=4)
    #publish_date = models.DateTimeField()
    #retrieval_date = models.DateField()
    
    
    domain = models.URLField()
    article_text = models.TextField()
    bias_score = models.DecimalField(max_digits=6, decimal_places=4)
    #publish_date = models.DateTimeField()
    #retrieval_date = models.DateField()
    keywords = models.TextField()
    url = models.TextField()


import newspaper
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
from nltk.stem.porter import *
import datetime
from multiprocessing.dummy import Pool


import sys
import os

class Analyzer:
    
    def __init__(self, articles, keyword, domain, f):
        self.articles = articles
        self.keyword = keyword
        self.domain = domain
        self.write_file = f
        
    # Determine if an article's relevance score for a given keyword
    # TODO: Improve by determining article's cosine score relevancy to the keyword
    def is_relevant(self, tokens):
        ps = PorterStemmer()
        keyword = ps.stem(self.keyword)
        for word in tokens:
            stemmed = ps.stem(word)
            if keyword.lower() == stemmed.lower():
                return True
        return False
    
    # Uses NLTK sentiment analysis to return the compound score for an article
    def score(self, article):
        path =""
        try:
            path = article.get_resource_path()
            article.download()
            article.parse()
            path = article.get_resource_path()
            print (article.get_resource_path())
            
            #article.clean_dom
            
            #article.clean_top_node
        except:
            return 0
            
        # Use NLTK word_tokenize module to tokenize the article
        tokens = word_tokenize(article.text)
        # If the article is not relevant, do not proceed to score it
        if not self.is_relevant(tokens):
            return 0.0
        # Perform sentiment analysis if the article is relevant
        print("Relevant Article: " + article.title)
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(article.text)
        print("Article Score: ", end=": ")
        for k in sorted(ss):
            print('{0}: {1}'.format(k, ss[k]), end=', ')
        print('\n')
        
        # just save the info to a text filefile = open(“testfile.txt”,”w”) 
        
        data = self.domain + " " + article.url +  " " + str(ss['compound']) + "\n"
        self.write_file.write(data)
        self.write_file.flush()
       
         # if check to see if newspaper is already in the db with that keyword
        #if NewspaperArticle.objects.filter(url=article.url, keywords=self.keyword).exists() == False:
         #   n1 = NewspaperArticle(domain = self.domain, url=article.url, keywords=self.keyword, article_text='', bias_score = ss['compound'])
            #publish_date=article.publish_date, retrieval_date=datetime.datetime.now())
            #n1.save()  
        
        # Return the article's compound sentiment score
        return ss['compound']
        
    # Finds the average sentiment score for a list of articles given a keyword
    def analyze(self):
        # https://stackoverflow.com/questions/2846653/how-to-use-threading-in-python
        # https://stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
        # 5 threads seems to work well -- should keep testing for optimal #
        #pool = Pool(5)
        #results = pool.map(self.score, self.articles)
        results = []
        for article in self.articles:
            result = self.score(article)
            results.append(result)
        #results = self.score(self.articles)
        average = 0.0
        count = 0
        for result in results:
            if result != 0:
                average += result
                count += 1
        average /= float(count)
        
        # close the pool and wait for the work to finish 
        #pool.close() 
        #pool.join() 

        return average
        
        
    # TODO: Calculates the term frequency of a term in an article    
    #def tf(self, term, article):
        
    # TODO: Determines the IDF score of a term in a list of articles
    #def idf(self, term, articles):

# Loads articles from a text file of URLs
class Loader:
    
    def __init__(self, filename):
        self.filename = filename
        self.websites = []

    # Load all of the website names from the text file
    def loadsites(self):
        with open(self.filename, 'r') as file:
            for website in file:
                self.websites.append(website)
    
    # Build each newspaper source using the Newspaper module
    def loadpapers(self):
        papers = []
        self.loadsites()
        for website in self.websites:
            current_paper = newspaper.build(website, memoize_articles=False, fetch_images=False, verbose=True)
            papers.append(current_paper)
        return papers
