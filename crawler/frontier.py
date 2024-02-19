import os
import shelve
import json
from threading import Thread, RLock
from queue import Queue, Empty
from urllib.parse import urlparse, urljoin
from utils import get_logger, get_urlhash, normalize
from scraper import is_valid


def get_domain_and_path(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc + parsed_url.path



class Frontier(object):
    def __init__(self, config, restart):
        self.logger = get_logger("FRONTIER")
        self.config = config
        self.to_be_downloaded = list()
        self.corpus = dict()
        self.largest_page = ""
        self.largest_word_count = 0
        self.subdomains = dict()
        self.subdomain_thres = 150
        if not os.path.exists(self.config.save_file) and not restart:
            # Save file does not exist, but request to load save.
            self.logger.info(
                f"Did not find save file {self.config.save_file}, "
                f"starting from seed.")
        elif os.path.exists(self.config.save_file) and restart:
            # Save file does exists, but request to start from seed.
            self.logger.info(
                f"Found save file {self.config.save_file}, deleting it.")
            os.remove(self.config.save_file)
        # Load existing save file, or create one if it does not exist.
        self.save = shelve.open(self.config.save_file)
        if restart:
            for url in self.config.seed_urls:
                self.add_url(url)
        else:
            # Set the frontier state with contents of save file.
            self._parse_save_file()
            if not self.save:
                for url in self.config.seed_urls:
                    self.add_url(url)

    def _parse_save_file(self):
        ''' This function can be overridden for alternate saving techniques. '''
        total_count = len(self.save)
        tbd_count = 0
        for url, completed in self.save.values():
            if not completed and is_valid(url):
                self.to_be_downloaded.append(url)
                tbd_count += 1
        self.logger.info(
            f"Found {tbd_count} urls to be downloaded from {total_count} "
            f"total urls discovered.")

    def get_tbd_url(self):
        try:
            return self.to_be_downloaded.pop()
        except IndexError:
            return None

    def add_url(self, url):
        url = normalize(url)
        urlhash = get_urlhash(url)
        if urlhash not in self.save:
            if get_domain_and_path(url) in self.subdomains:
                self.subdomains[get_domain_and_path(url)] +=1
            else:
                self.subdomains[get_domain_and_path(url)] =1
            
        
            if get_domain_and_path(url) in self.subdomains and self.subdomains[get_domain_and_path(url)] > self.subdomain_thres:
                print("skip url reached depth of", self.subdomain_thres, "for url:",url,get_domain_and_path(url))
                return

            self.save[urlhash] = (url, False)
            self.save.sync()
            self.to_be_downloaded.append(url)
    
    def mark_url_complete(self, url):
        urlhash = get_urlhash(url)
        if urlhash not in self.save:
            # This should not happen.
            self.logger.error(
                f"Completed url {url}, but have not seen it before.")

        self.save[urlhash] = (url, True)
        self.save.sync()
        


        with open("subdomains.json",'w')as json_file:
            json.dump(self.subdomains,json_file)

    def save_words(self, words_list):
        # saves the corpus of crawler to a text file for later for report
        if words_list:
            for i in words_list:
                if i in self.corpus:
                    self.corpus[i] +=1
                else:
                    self.corpus[i] =1
            with open("corpus.json",'w')as json_file:
                json.dump(self.corpus,json_file)


        