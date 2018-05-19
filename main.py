from multiprocessing.dummy import Pool
import sys
import os
import json
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
import threading

class Analyzer:
    
    def __init__(self, articles, keyword, domain, f):
        self.articles = articles
        self.keyword = keyword
        self.domain = domain
        self.write_file = f
        
    # Determine if an article's relevance score for a given keyword
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
            article.download()
            article.parse()
            
            path = article.get_resource_path()
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
        
        # just save the info to a text
        data = self.domain + " " + article.url +  " " + str(ss['compound']) + "\n"
        self.write_file.write(data)
        self.write_file.flush()
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
        

        return average
       

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
        
def analyze_keywords(articles, keywords, domain, f):
    scores = {}
    for keyword in keywords:
        print("Determining Sentiment Average for keyword: ", keyword)
        analyzer = Analyzer(articles, keyword, domain, f)
        scores[keyword] = analyzer.analyze()
        print("Sentiment Average for ", keyword, ": ", scores[keyword])
    return scores
    
def get_bias(source, keywords, domain, f):
    articles = source.articles
    analyze_keywords(articles, keywords, domain, f)
    
import datetime


def analyzeArticlesOfTheDay():
    #-----------------------------------------------------------------------
  #  '''
    loader = Loader("websites.txt")
    all_papers = loader.loadpapers() # load all the articles from each website in the file
    for paper in all_papers:
        line = '%-30s  %-15s' % (("URL: " + paper.domain), str("# of Articles: " + str(len(paper.articles))))
        print(line)
    
    now = datetime.datetime.now()
    fname = "newspapers_scores" + str(now.month) + "-"+str(now.day) + "-" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second) + ".txt"
    print(fname)
    # zero makes it unbuffered. i.e writes automatically
    f = open(fname,"w") 
    # Donald Trump, Barack Obama, Hillary Clinton, Marco Rubio, Ted Cruz, Bernie Sanders, Betsy DeVos, Rick Perry
    keywords = ['trump']
    for paper in all_papers:
        # paper is all the articles for a specific news outlet
        print("=====Analyzing", paper.domain, "for keyword", keywords, "=====")
        get_bias(paper, keywords, paper.domain, f)
        print("=====DONE ANALYZING", paper.domain, "=========")
    f.close()
    
    print("done analyzing all docs")
        
def main():
    print("starting...")
    analyzeArticlesOfTheDay()
    print ("done...")
    
main()
