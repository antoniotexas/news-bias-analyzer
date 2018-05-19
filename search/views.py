# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .forms import SearchForm
from django.http import HttpResponseRedirect

from newspaper import Article

from search.models import NewspaperArticle, Loader, Analyzer
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

#access db 
from search.models import NewspaperArticle

import re

def index(request):
    return search_new(request)
    
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
    '''
    loader = Loader("websites.txt")
    all_papers = loader.loadpapers() # load all the articles from each website in the file
    for paper in all_papers:
        line = '%-30s  %-15s' % (("URL: " + paper.domain), str("# of Articles: " + str(len(paper.articles))))
        print(line)
    
    # BUG TO MANNY CONCURRENT THREADS
    now = datetime.datetime.now()
    fname = "newspapers_scores" + str(now.month) + "-"+str(now.day) + "-" + str(now.hour) + "-" + str(now.minute) + ".txt"
    print(fname)
    # zero makes it unbuffered. i.e writes automatically
    f = open(fname,"w") 
    keywords = ['clinton']
    for paper in all_papers:
        # paper is all the articles for a specific news outlet
        print("=====Analyzing", paper.domain, "for keyword", keywords, "=====")
        get_bias(paper, keywords, paper.domain, f)
        print("=====DONE ANALYZING", paper.domain, "=========")
    f.close()
    
    print("done analyzing all docs")
    '''
    
    #---------------------------------------------------------------------------------------
    
    #---------------------------------------------------------------------------------
    #'''
    # use this function to save to heroku
    
    # save scores to db code
    print ("starting to save articles to db...")
    fname = "e.txt"
    keyword = 'democrat'
    with open(fname,'r') as f_in:
        lines = (line.rstrip() for line in f_in) # All lines including the blank ones
        #print(lines)
        lines = (line for line in lines if line) # Non-blank lines
        #print(lines)
        for line in lines:
            print(line.split())
            _domain, _url, compound_score = line.split()
            if NewspaperArticle.objects.filter(domain=_domain, url=_url, keywords=keyword).exists() == False:
                n1 = NewspaperArticle(domain=_domain, url=_url, keywords=keyword, article_text='', bias_score=compound_score) #publish_date=datetime.datetime.now(), retrieval_date=datetime.datetime.now())
                n1.save() 
            
            print(_domain, _url, compound_score)
            
    print ("done savings scores to db ...", keyword)
    # done saving scores to db
    
     #'''
    
    #---------------------------------------------------------------------------------------------
    
import threading

def search_new(request):
   
    # if this is a POST request we need to process the form data
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            
            #startDoingProject()
            returnData = 'inputed query = '
        
            return HttpResponse(returnData)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'search/index.html', {'form': form})
    
class HomeView(View):
    def get(self, request):
        return render(request, 'charts.html')

#sends data to the graph. 
class ChartData(APIView):
    
    def get(self, request, format=None):
        
        db_data = NewspaperArticle.objects.all()
        labels = []
        bias_scores = []
        matrix = {}
        
        # retrieve from db
     
        
        smallMatrix = {'NY Times': 0, 'Wall Street Journal': 0, 'USA Today': 0, 'CBS News': 0, 'Huffington Post': 0, 
                        'Reuters': 0, 'Washington Times': 0, 'CNN': 0, 'Fox News' : 0, 'NBC News': 0, 'ABC News': 0, 'MSN': 0}
        bigMatrix = {}
        
        smallCounter = {'NY Times': 0, 'Wall Street Journal': 0, 'USA Today': 0, 'CBS News': 0, 'Huffington Post': 0, 
                        'Reuters': 0, 'Washington Times': 0, 'CNN': 0, 'Fox News' : 0, 'NBC News': 0, 'ABC News': 0, 'MSN': 0}
        bigCounter = {}
        
        allKeywords = []
        # sum the bias scores of all the articles in the db
        for paper in db_data:
            p = re.compile('^(?:http://|https://)?(?:www.)?(.*).com(?:.*)$')
            filtered_name = p.search(paper.domain).group(1)
            
            label = 'NOT_FOUND'
            
            
            if filtered_name == 'nytimes':
                label = 'NY Times'
            elif filtered_name == 'wsj':
                label = 'Wall Street Journal'
            elif filtered_name == 'usatoday':
                label = 'USA Today'
            elif filtered_name == 'cbsnews':
                label = 'CBS News'
            elif filtered_name == 'huffingtonpost':
                label = 'Huffington Post'
            elif filtered_name == 'reuters':
                label = 'Reuters'
            elif filtered_name == 'washingtontimes':
                label = 'Washington Times'
            elif filtered_name == 'cnn':
                label = 'CNN'
            elif filtered_name == 'foxnews':
                label = 'Fox News'
            elif filtered_name == 'nbcnews':
                label = 'NBC News'
            elif filtered_name == 'abcnews.go':
                label = 'ABC News'
            elif filtered_name == 'msn':
                label = 'MSN'
            else:
                print("label not found: ", filtered_name)
                
            labels.append(label)
            keyword = paper.keywords.lower()
            allKeywords.append(keyword)
            bias_score = paper.bias_score

            # not polarized enough to acccurately make any conclusion.    
            if bias_score > 0.5:
                pass
            elif bias_score < -0.5:
                pass
            else:
                continue

            if keyword not in bigMatrix:
                bigMatrix[keyword] = {'NY Times': 0, 'Wall Street Journal': 0, 'USA Today': 0, 'CBS News': 0, 'Huffington Post': 0, 
                        'Reuters': 0, 'Washington Times': 0, 'CNN': 0, 'Fox News' : 0, 'NBC News': 0, 'ABC News': 0, 'MSN': 0}
                bigMatrix[keyword][label] += bias_score
                
                
                bigCounter[keyword] = {'NY Times': 0, 'Wall Street Journal': 0, 'USA Today': 0, 'CBS News': 0, 'Huffington Post': 0, 
                        'Reuters': 0, 'Washington Times': 0, 'CNN': 0, 'Fox News' : 0, 'NBC News': 0, 'ABC News': 0, 'MSN': 0}
                bigCounter[keyword][label] += 1
                
            else:
                bigMatrix[keyword][label] += bias_score
                bigCounter[keyword][label] += 1
        
        # x e.g. {trump: {CNN: 32.34, ABC: 53.3, ... }}
        # e.g. bigCounter[keyword] = {CNN: 3, ABC: 6}
        print("\n\n\n\n")
        for keyword in bigMatrix:
            
            for label in bigMatrix[keyword]:
                b_score = bigMatrix[keyword][label]
                if b_score == 0:
                    continue
                else:
                    bigMatrix[keyword][label] /= bigCounter[keyword][label]
            
        data = {'labels': list(set(labels)), 'keywords': list(set(allKeywords)), 'data': bigMatrix}
        return Response(data)
