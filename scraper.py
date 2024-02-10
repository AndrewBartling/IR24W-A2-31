import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup,SoupStrainer
import tokenizer
from simhash import Simhash, SimhashIndex
import httplib2

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
    try:

        if resp.status == 400:
            return resp.error

        elif resp.status == 300:
            #redirect
            pass
        elif resp.status == 200:
            #succcess token the webpage

            largefile = False
            content_length = resp.raw_response.headers.get('Content-Length')
            if content_length and int(content_length) > 10 * 1024 * 1024:  
                print("Skipping due to large content size:", resp.url)
                largefile = True            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
            
            # Extract text content and count words
            text = soup.get_text()
            

            tokens,total_words =tokenizer.tokenize(text)
            
            min_word_count = 20 
             
            links = set()
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.startswith(('http://', 'https://')):
                    links.add(href)
                elif href:
                    links.add(urljoin(url, href))

            if total_words < 20 and largefile:
                #if a page has less than 20 words you shouldn't save it 
                return list()
            with open("scrapered.txt","a")as file:
                file.write(url +"\n")

            return list(links)
        #include simhashing for simliarity


        return list(url)
        #check for redirect?
    except Exception as e:
        print("ERROR: ",e)
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
        
        print("is_valid,", url)
    except TypeError:
        print ("TypeError for ", url)
        raise
