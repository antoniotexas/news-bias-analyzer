from newspaper import Article
import nltk
url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
article = Article(url)
article.download()
article.parse()
article.nlp()
print("keywrods", article.keywords)
print("text :: ", article.text)
