import re
from nltk.corpus import stopwords

ntlk.download('stopwords')


stop_words = set(stopwords.words('english'))


'''
Runtime complexity for tokenize:
n = size of the file being read line by line

re.findall checks the one line at a time and matches the pattern over it 

m = size of the line being tokenized

initialize and appending to a list is O(1)

Runtime = O(n + m)
        = O(n)


credit to https://regex101.com for testing regular expression     

'''    
def tokenize(text:str) -> list:

    tokens=[]
    expression = "\b[a-z0-9]+\b"



    tokens +=(re.findall(expression,line.lower()))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

'''
Runtime complexity for computeWordFrequencies:

n = number of tokens in the list

using average case from https://wiki.python.org/moin/TimeComplexity for dict

initialize dict, if token is in dict, add/set item to dict, is O(1)

Runtime = O(n)

'''    
def computeWordFrequencies(tokens:list)-> dict:

    frequencies ={}
    for i in tokens:
        if i not in frequencies:
            frequencies[i] = 1
        else:
            frequencies[i] +=1
    return frequencies
'''
Runtime complexity for print_frequencies:

n = size of the frequencies dict

sorted uses Timsort, it is O(n log n ) for Worst-case and Average performance

sorting the dict is O(n log n) 

iterating over the whole dict is O(n)

runtime = O(n + n log n)
        = O(n log n)

'''
def print_frequencies(frequencies:dict)->None:

    frequencies = sorted(frequencies.items(),key=lambda x: (-x[1],x[0]))
    for key,values in frequencies:
        print(key,"=",values)
    

'''
Total run time for running PartA.py is :
runtime = O(n log n)
as it's the largest growing time complexity 
'''


if __name__ == "__main__":
    tokens = tokenize(sys.argv[1])
    freqs = computeWordFrequencies(tokens)
    print_frequencies(freqs)
