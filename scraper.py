import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup,SoupStrainer
import tokenizer
import httplib2

def remove_fragment_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url._replace(fragment='').geturl()


def scraper(url, resp):
    links,tokens_dic,total = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)],tokens_dic,total



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

        elif 300 <= resp.status <400:
            #redirect
            print("was redirect")
            pass
        elif resp.status == 200:
            #succcess token the webpage
            largefile = False

            #check to see if the file's size and if it's too large reject it
            content_length = resp.raw_response.headers.get('Content-Length')
            if content_length and int(content_length) > 8 * 1024 * 1024:  
                print("Skipping due to large content size:", resp.url)
                with open("error.txt","a" ) as file:
                    file.write(url+": "+str(resp.status)+"too large file,skipped"+"\n")
                return list(),[],int()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
            
            # Extract text content and count words
            text = soup.get_text()
            tokens,total_words =tokenizer.tokenize(text)

            links = set()

            #find all the links in the text and add them to a set to prevent duplicates
            for link in soup.find_all('a'):
                href = link.get('href')
                href = remove_fragment_from_url(href)

                if href and href.startswith(('http://', 'https://')):
                    links.add(href)
                elif href:
                    links.add(urljoin(href,url))
            
            links = list(links)


 
            if total_words < 30:
                #if a page has less than 30 words you shouldn't save it
                with open("error.txt","a" ) as file:
                    file.write(url+": "+str(resp.status)+"too little words skip"+"\n")

                return links,dict({}),int(0)

            #saved that the current url was scrapped successfuly
            with open("scrapered.txt","a")as file:
                file.write(url +"\n")        

            #return list of links, list of token, and int of total words to the crawler
            return links,tokens,total_words

        # if the resp status isn't succesful save the url and it's error code 
        with open("error.txt","a" ) as file:
            file.write(url+": " +str(resp.status) +"\n")

        return list([]),dict({}),int(0)
    except Exception as e:
        print("ERROR in scapering url: ",e)
        return list([]),dict({}),int(0)


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

            return False

        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico|odc|"
            + r"|png|tiff?|mid|mp2|mp3|mp4|img|ima"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|mpg"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1|ps|ppsx"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|apk)$", parsed.path.lower())


    except TypeError:
        print ("TypeError for ", url)
        raise
