import re
from urllib.parse import urlparse,urldefrag,urljoin
from bs4 import BeautifulSoup
import tokenizer
from simhash import Simhash, SimhashIndex
import requests

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    url = set()

    

    if resp.status == 400:
        return resp.status
    
    elif resp.status == 300:
        #redirect
        pass
    elif resp.start == 200:
        
        #succcess token the webpagS
        #save all words tokenized to get top 50 words 
        #longest page in term of number of words 
        soup = BeautifulSoup(resp.raw_response.content,'html.parser')
        print("links",soup)
    #include simhashing for simliarity



    #check for redirect?

    return list()

def domains_match(url):

    domains = [
        r".*\.ics\.uci\.edu.*",
        r".*\.cs\.uci\.edu.*",
        r".*\.informatics.uci.edu.*",
        r".*\.stat.uci.edu.*"
    ]

    for domain in domains:
        if re.match(domain,url):
            return True
    return False

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if False ==domains_match(parsed.netloc):
            print(url)
            return False


        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
    except TypeError:
        print ("TypeError for ", parsed)
        raise
