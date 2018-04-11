import json, time, argparse
from datetime import datetime

SENTIMENT_VECTOR_SIZE = 10


def load_data(fname):
    print('Loading data from ' + fname)
    output = []
    with open(fname) as f:
        for line in f:
            j = json.loads(line)
            output.append(j)
    return output


def add_sentiments(sentiments, price_change, output):
    sentiments.sort(reverse=True)
    sentiments = sentiments[:SENTIMENT_VECTOR_SIZE]
    if len(sentiments) == SENTIMENT_VECTOR_SIZE and sentiments[0] != 0.0:
        change = 1 if price_change > 0 else 0
        output.append((sentiments, change))


def build_features(ftweets, fprices):
    print('Building features')

    tweets = load_data(ftweets)
    prices = load_data(fprices)

    price_dic = dict()
    for price in prices:
        price_time = datetime.utcfromtimestamp(price['timestamp']).strftime('%Y-%m-%dT%H')
        change = float(price['ticker']['change'])
        change = 0 if change < 0 else 1
        price_dic[price_time] = (change, [])

    for i, tweet in enumerate(tweets):
        tweet_time = datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H')
        
        if tweet_time in price_dic:
            price_dic[tweet_time][1].append(float(tweet['sentiment']['compound']))

    features = []
    for k, v in price_dic.items():
        change = v[0]
        sentiments = v[1][:SENTIMENT_VECTOR_SIZE]
        sentiments.sort(reverse=True)

        if len(sentiments) == SENTIMENT_VECTOR_SIZE:
            features.append((sentiments, change))
    
    print(features[-5:])
    
    return features


def write_features_to_csv(features, fname):
    print('Writing features')
    with open(fname, 'w') as f:
        column_headers = ','.join(['S'+str(i) for i in range(SENTIMENT_VECTOR_SIZE)]) + ',CHANGE\n'
        f.write(column_headers)
        for feature_vector in features:
            x = [str(v) for v in feature_vector[0]]
            y = str(feature_vector[1])
            f.write(','.join(x))
            f.write(',' + y + '\n')
                

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tweets", help="Tweets file", required=True)
    parser.add_argument("-p", "--prices", help="Prices file", required=True)
    parser.add_argument("-o", "--output", help="Output file", required=True)
    parser.add_argument("-s", "--svs", help="Sentiment vector size", required=True)

    args = parser.parse_args()
    SENTIMENT_VECTOR_SIZE = int(args.svs)

    # Build features
    f = build_features(args.tweets, args.prices)
    write_features_to_csv(f, args.output)
