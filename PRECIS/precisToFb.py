import bs4 as BeautifulSoup
import urllib.request
from urllib.error import HTTPError
import Precis


def Process_url(url):
    try:
        # Fetching the content from the URL
        fetched_data = urllib.request.urlopen(url)

        article_read = fetched_data.read()
        # Parsing the URL content and storing in a variable
        article_parsed = BeautifulSoup.BeautifulSoup(article_read,'html.parser')
        # Returning <p> tags
        paragraphs = article_parsed.find_all('p')

    except HTTPError as e:
        return str(e) + ". Try another URL"

    except:
        return "Invalid URL"
    
    article_content = ''
    for p in paragraphs:  
        article_content += p.text

    summary = Precis._run_article_summary(article_content)
    #print(summary)
    return summary

    
   