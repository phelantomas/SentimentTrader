from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


def get_sentiment_for_tweets():
    output = []
    
    # Open the tweet dataset
    with open('tweets_formatted.txt', 'r') as f:
        tweets = f.readlines()
    
    # Get the sentiment for each tweet
    sia = SIA()
    
    for i in range(len(tweets)):
        tweet = tweets[i].split('||')[1]
        res = sia.polarity_scores(tweet)
        output.append(tweets[i].rstrip("\n")+'||'+str(res['compound']))
        if i % 100 == 0:
            print(i)
    
    with open('tweets_with_sentiment.txt', 'w+') as f:
        for line in output:
            f.write(line+"\n")


def calculate_sentiment(text):
    sia = SIA()
    return sia.polarity_scores(text)


if __name__ == '__main__':
    get_sentiment_for_tweets()