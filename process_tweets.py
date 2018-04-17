'''
Author: Tomas Phelan
License Employed: GNU General Public License v3.0
Brief: Takes tweets and formats them.
'''

import argparse, json
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from datetime import datetime
import format

def process_tweets_from_file(fin, fout):
    valid_count = 0
    invalid_count = 0
    sia = SIA()

    list_of_tweets = []
    with open(fin) as f:
        for line in f:
            j = json.loads(line)
            try:
                # validate date format
                created_at = datetime.strptime(j['created_at'], '%Y-%m-%dT%H:%M:%S')

                # text formatting
                formatted_text = format.format_full(j['text'])
                j['formatted_text'] = formatted_text

                # sentiment
                sent = sia.polarity_scores(formatted_text)
                j['sentiment'] = sent

                list_of_tweets.append(json.dumps(j))
                valid_count += 1
                if (valid_count % 25000 == 0):
                    print(valid_count)
            except ValueError:
                invalid_count += 1
                if (invalid_count % 100 == 0):
                    print('Invalid:' + str(created_at), j['created_at'])
                continue

    with open(fout, 'w') as f:
        for tweet in list_of_tweets:
            f.write(tweet+'\n')

def get_sentiment(formatted_text):
    CRYPTO_LEXICON = json.load(open("../SentimentTrader/Words/crypto_lexicon.json"))
    sia = SIA()
    sia.lexicon.update(CRYPTO_LEXICON)

    return sia.polarity_scores(formatted_text)

def process_tweets_from_main(tweets):
    spam_list = json.load(open("../SentimentTrader/Words/spam_phrases.json"))
    spam_list = format.generate_variations(spam_list)
    invalid_count = 0

    list_of_tweets = []

    for line in tweets:
        j = line.__dict__
        try:
            # text formatting
            formatted_text = format.remove_excess_whitespace(j['text'])

            #has spam words, do not add
            if any(word in formatted_text.lower() for word in spam_list):
                continue

            formatted_text = format.remove_url(formatted_text)
            j['formatted_text'] = formatted_text

            # validate date format
            created_at = datetime.strptime(j['created_at'], '%Y-%m-%dT%H:%M:%S')

            # sentiment
            sent = get_sentiment(formatted_text)
            j['sentiment'] = sent

            if j['sentiment']['compound'] == 0:
                continue

            list_of_tweets.append(j)
        except ValueError:
            invalid_count += 1
            if (invalid_count % 100 == 0):
                print('Invalid:' + str(created_at), j['created_at'])
            continue
    return list_of_tweets


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file", required=True)
    parser.add_argument("-o", "--output", help="output file", required=True)
    args = parser.parse_args()

    # Process tweets
    process_tweets_from_file(args.input, args.output)
