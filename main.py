'''
Author: Tomas Phelan
License Employed: GNU General Public License v3.0
Brief:
'''
from apscheduler.schedulers.blocking import BlockingScheduler
import collect_tweets, collect_prices, process_tweets, json
import pandas as pd
import os.path
import predict
import log_creater as lc

formatted_btc_tweets = []
formatted_ltc_tweets = []
formatted_eth_tweets = []

twitter_logger = lc.setup_logger('first_logger', 'twitter_logfile.log')

sched = BlockingScheduler()
num_of_passes = 0

def analyse_data(formatted_tweets, filename, exchange, coin):
    #remove duplicated tweets
    formatted_tweets = [i for n, i in enumerate(formatted_tweets) if i not in formatted_tweets[n + 1:]]

    print("Number of unique tweets in an hour for " + coin + " is " + str(len(formatted_tweets)))

    file_exists = os.path.isfile(filename)

    price_info = collect_prices.get_price_info(exchange)

    j_info = json.loads(price_info)
    change = j_info['ticker']['change']
    volume = j_info['ticker']['volume']
    timestamp = j_info['timestamp']

    # average compound
    average_compound = float(sum(d['sentiment']['compound'] for d in formatted_tweets)) / len(
        formatted_tweets)


    cryptoFeature = {'TimeStamp': [timestamp], 'Sentiment': [average_compound], 'Volume': [volume],
                  'Change': [change]}

    pd.DataFrame.from_dict(data=cryptoFeature, orient='columns').to_csv(filename, mode='a',
                                                                     header=not file_exists)
    # Make
    predict_change = predict.generate_linear_prediction_model(cryptoFeature, filename)

    print("The sentiment of the last 15 minutes for " + coin + " is : " + str(
        cryptoFeature['Sentiment'][0]) + " - The predicted change in price is : " + predict_change)


@sched.scheduled_job('interval', minutes=1)
def timed_job():
    global formatted_btc_tweets
    global formatted_ltc_tweets
    global formatted_eth_tweets
    global num_of_passes

    num_of_passes = num_of_passes + 1

    print('Pass number : ' + str(num_of_passes))

    #bitcoin
    btcTweets = collect_tweets.collect_tweets('bitcoin')
    btcTweets = process_tweets.process_tweets_from_main(btcTweets)
    log_info = "Number of btc tweets just recieved : " + str(len(btcTweets))
    twitter_logger.info(log_info)
    #print("Number of btcTweets just retrieved", len(btcTweets))

    formatted_btc_tweets.extend(btcTweets)
    #print(len(formatted_btc_tweets))
    log_info = "Current number of btc tweets : " + str(len(btcTweets))
    twitter_logger.info(log_info)

    #litecoin
    ltcTweets = collect_tweets.collect_tweets('litecoin')
    ltcTweets = process_tweets.process_tweets_from_main(ltcTweets)
    #print("Number of ltcTweets", len(ltcTweets))
    log_info = "Number of ltc tweets just recieved : " + str(len(ltcTweets))
    twitter_logger.info(log_info)

    formatted_ltc_tweets.extend(ltcTweets)
    #print(len(formatted_ltc_tweets))
    log_info = "Current number of ltc tweets : " + str(len(ltcTweets))
    twitter_logger.info(log_info)

    #etherium
    ethTweets = collect_tweets.collect_tweets('etherium')
    ethTweets = process_tweets.process_tweets_from_main(ethTweets)
    #print("Number of ethTweets", len(ethTweets))
    log_info = "Number of eth tweets just recieved : " + str(len(ethTweets))
    twitter_logger.info(log_info)

    formatted_eth_tweets.extend(ethTweets)
    #print(len(formatted_eth_tweets))
    log_info = "Current number of eth tweets : " + str(len(ethTweets))
    twitter_logger.info(log_info)

    if(num_of_passes is 60):
        num_of_passes = 0

        analyse_data(formatted_btc_tweets, "btcFeature.csv", "btc-usd", "Bitcoin")
        formatted_btc_tweets = []
        analyse_data(formatted_ltc_tweets, "ltcFeature.csv", "ltc-usd", "Litecoin")
        formatted_ltc_tweets = []
        analyse_data(formatted_eth_tweets, "ethFeature.csv", "eth-usd", "Etherium")
        formatted_eth_tweets = []

sched.start()