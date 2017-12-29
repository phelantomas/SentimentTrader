import argparse, json, format
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from datetime import datetime
import logCreater as lc

twitter_logger = lc.setup_logger('first_logger', 'twitter_logfile.log')

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
                # datetime.strptime('2016-10-27 22:58:14', '%Y-%m-%d %H:%M:%S')

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
    
    #print("Successfully processed", len(list_of_tweets), "tweets")
    twitter_info = "Successfully processed " + str(len(list_of_tweets)) + " tweets"
    twitter_logger.info(twitter_info)


def process_tweets_from_main(tweets):
    valid_count = 0
    invalid_count = 0
    sia = SIA()
    list_of_tweets = []

    for line in tweets:
        j = line.__dict__
        try:
            # validate date format
            created_at = datetime.strptime(j['created_at'], '%Y-%m-%dT%H:%M:%S')
            # datetime.strptime('2016-10-27 22:58:14', '%Y-%m-%d %H:%M:%S')

            # text formatting
            formatted_text = format.format_full(j['text'])
            j['formatted_text'] = formatted_text

            # sentiment
            sent = sia.polarity_scores(formatted_text)
            j['sentiment'] = sent

            list_of_tweets.append(j)
            valid_count += 1
            if (valid_count % 25000 == 0):
                print(valid_count)
        except ValueError:
            invalid_count += 1
            if (invalid_count % 100 == 0):
                print('Invalid:' + str(created_at), j['created_at'])
            continue
    #print("Successfully processed", len(list_of_tweets), "tweets")
    twitter_info = "Successfully processed " + str(len(list_of_tweets)) + " tweets"
    twitter_logger.info(twitter_info)
    return list_of_tweets


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file", required=True)
    parser.add_argument("-o", "--output", help="output file", required=True)
    args = parser.parse_args()

    # Process tweets
    process_tweets_from_file(args.input, args.output)
