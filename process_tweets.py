'''
Author: Tomas Phelan
License Employed: GNU General Public License v3.0
Brief:
'''

import argparse, json
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from datetime import datetime
import format

def process_tweets_from_file(fin, fout):
    valid_count = 0
    invalid_count = 0
    sia = SIA()
    sia.lexicon.update({u'hodle': 3})
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

def process_tweets_from_main(tweets):
    invalid_count = 0
    sia = SIA()

    #Dict of kewords used by cryptocurrency enthuasists
    crypto_slang = {u'bullish': -1.4, u'ath': 3.0, u'ico': 1.0, u'shilling': -2.0, u'fomo': -3.0, u'fudster': -3.2,
                    u'bagholder': -1.3, u'sharding': 1.1,
                    u'dapp': 1.5, u'wei': 1.0, u'hodl': 3.5, u'lambo': 4.0, u'mooning': 2.6, u'satoshi': 2.5}
    sia.lexicon.update(crypto_slang)

    list_of_tweets = []
    list_of_spam = [' prize ', 'prize ', ' prize.',
                    ' contest ', 'contest ', ' contest.',
                    ' giveaway ', 'giveaway ', ' giveaway.',
                    ' giving away ','giving away ',' giving away.',
                    ' free ', 'free ', ' free.',
                    ' limited time only ', 'limited time only ',' limited time only.',
                    ' discount ', 'discount ', ' discount.',
                    ' click here ', 'click here ', ' click here.',
                    ' 4u ', '4u ', ' 4u.']

    for line in tweets:
        j = line.__dict__
        try:
            # text formatting
            formatted_text = format.remove_excess_whitespace(j['text'])

            #has spam words, do not add
            if any(word in formatted_text.lower() for word in list_of_spam):
                continue

            formatted_text = format.remove_url(formatted_text)
            j['formatted_text'] = formatted_text

            # validate date format
            created_at = datetime.strptime(j['created_at'], '%Y-%m-%dT%H:%M:%S')

            # sentiment
            sent = sia.polarity_scores(formatted_text)
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
