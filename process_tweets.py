import argparse, json, format
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from datetime import datetime


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
    
    print("Successfully processed", len(list_of_tweets), "tweets")


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file", required=True)
    parser.add_argument("-o", "--output", help="output file", required=True)
    args = parser.parse_args()

    # Process tweets
    process_tweets_from_file(args.input, args.output)
