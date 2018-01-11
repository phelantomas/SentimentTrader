'''
Author: Tomas Phelan
License Employed: GNU General Public License v3.0
Brief: Includes methods for processing raw tweet data
'''

from string import ascii_lowercase
from nltk.corpus import words as english_words, stopwords
import Porter

porter_stemming = Porter.PorterStemmer()

english = set(w.lower() for w in english_words.words())
stop = set(w.lower() for w in stopwords.words())


def remove_excess_whitespace(text):
    return ' '.join(text.split())
    
    
def convert_to_lowercase(text):
    return text.lower()
    
    
def remove_non_alpha_chars(text):
    T = list(text)
    i = 0
    while i < len(T):
        if T[i] not in ascii_lowercase and T[i] != ' ':
            del T[i]
        else:
            i += 1
    return ''.join(T)
    

def remove_non_english_words(text, english):
    T = text.split(' ') # ["hello", "world"]
    i = 0
    while i < len(T):
        if T[i] not in english:
            del T[i]
        else:
            i += 1    
    return ' '.join(T)


def remove_stopwords(text, stop):
    T = text.split(' ')
    i = 0
    while i < len(T):
        if T[i] in stop or len(T[i]) == 1:
            del T[i]
        else:
            i += 1
    return ' '.join(T)


def format_syntax(text):
    a = convert_to_lowercase(text)
    b = remove_non_alpha_chars(a)
    c = remove_excess_whitespace(b)
    return c


def format_semantic(text):
    a = remove_non_english_words(text, english)
    #Checkcking to see what difference is made
    #b = remove_stopwords(a, stop)
    return a

def format_porter(text):
    return porter_stemming.stem(text, 0,len(text)-1)
    

def format_full(text):
    return (format_semantic(format_syntax(text)))
    #return #format_porter(formatted_text)


def format_test():
    print(format_full("# ILoveNY bcuz    $ $  money"))
    print(format_full("Hello to the world"))


if __name__ == '__main__':
    # Format raw tweets
    seen = set()
    
    infile = open('tweets_raw.txt', 'r')
    outfile = open('tweets_formatted.txt', 'w+')
    i = 0
    for line in infile:
        i += 1
        if (i % 1000) == 0:
            i = 0
            print(time.time())
        tw = line.split("||")
        fmt = format_tweets.format_full(tw[1])
        try:
            tweet_time = datetime.datetime.strptime(tw[2], "%Y-%m-%dT%H:%M:%S")
            tweet_hash= str(tweet_time.year) + str(tweet_time.month) + str(tweet_time.day) + str(tweet_time.hour)+"||"+fmt
            if fmt:
                if tweet_hash not in seen:
                    outfile.write(tw[2] + "||" + fmt + "\n")
                    seen.add(tweet_hash)
        except ValueError as e:
            continue
