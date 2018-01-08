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

twitter_logger = lc.setup_logger('first_logger', 'twitter_logfile.log')

sched = BlockingScheduler()
formatted_btc_tweets = []
formatted_ltc_tweets = []
formatted_eth_tweets = []

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    #print('This job is run every minute')
    global formatted_btc_tweets
    global formatted_ltc_tweets
    global formatted_eth_tweets

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

@sched.scheduled_job('interval', minutes=15)
def scheduled_job():
    #print('This job is run every 15 minutes')
    global formatted_btc_tweets
    global formatted_ltc_tweets
    global formatted_eth_tweets

    #remove duplicates
    formatted_btc_tweets = [i for n, i in enumerate(formatted_btc_tweets) if i not in formatted_btc_tweets[n + 1:]]
    formatted_ltc_tweets = [i for n, i in enumerate(formatted_ltc_tweets) if i not in formatted_ltc_tweets[n + 1:]]
    formatted_eth_tweets = [i for n, i in enumerate(formatted_eth_tweets) if i not in formatted_eth_tweets[n + 1:]]

    #print('Actual btc ', len(formatted_btc_tweets))
    #print('Actual ltc ',len(formatted_ltc_tweets))
    #print('Actual eth ',len(formatted_eth_tweets))

    log_info = "Current number of btc tweets without duplicates : " + str(len(formatted_btc_tweets))
    twitter_logger.info(log_info)
    log_info = "Current number of ltc tweets without duplicates : ", str(len(formatted_ltc_tweets))
    twitter_logger.info(log_info)
    log_info = "Current number of eth tweets without duplicates : ", str(len(formatted_eth_tweets))
    twitter_logger.info(log_info)

    btc_file_exists = os.path.isfile('btcFeature.csv')
    ltc_file_exists = os.path.isfile('ltcFeature.csv')
    eth_file_exists = os.path.isfile('ethFeature.csv')

    btc_price_info = collect_prices.get_price_info('btc-usd')
    ltc_price_info = collect_prices.get_price_info('ltc-usd')
    eth_price_info = collect_prices.get_price_info('eth-usd')

    #bitcoin
    j_btc_info = json.loads(btc_price_info)
    btc_change = j_btc_info['ticker']['change']
    btc_volume = j_btc_info['ticker']['volume']
    btc_timestamp = j_btc_info['timestamp']
    #average compound
    btc_average_compound = float(sum(d['sentiment']['compound'] for d in formatted_btc_tweets)) / len(formatted_btc_tweets)

    btcFeature = {'TimeStamp' : [btc_timestamp], 'Sentiment': [btc_average_compound], 'Volume': [btc_volume], 'Change': [btc_change]}


    #Make
    btc_predict_change = predict.generate_linear_prediction_model(btcFeature, "/home/tomas/PycharmProjects/CollegeProject/btcFeature.csv")

    print( "The sentiment of the last 15 minutes for btc is : " + str(btcFeature['Sentiment'][0]) + " - The predicted change in price is :" + btc_predict_change)
    pd.DataFrame.from_dict(data=btcFeature, orient='columns').to_csv('btcFeature.csv', mode='a', header=not btc_file_exists)

    formatted_btc_tweets = []

    # litecoin
    j_ltc_info = json.loads(ltc_price_info)
    ltc_change = j_ltc_info['ticker']['change']
    ltc_volume = j_ltc_info['ticker']['volume']
    ltc_timestamp = j_ltc_info['timestamp']
    # average compound
    ltc_average_compound = float(sum(d['sentiment']['compound'] for d in formatted_ltc_tweets)) / len(
        formatted_ltc_tweets)

    ltcFeature = {'TimeStamp': [ltc_timestamp], 'Sentiment': [ltc_average_compound], 'Volume': [ltc_volume],
                  'Change': [ltc_change]}

    ltc_predict_change = predict.generate_linear_prediction_model(ltcFeature, "/home/tomas/PycharmProjects/CollegeProject/ltcFeature.csv")

    print( "The sentiment of the last 15 minutes for ltc is : " + str(ltcFeature['Sentiment'][0]) + " - The predicted change in price is :" + ltc_predict_change)

    pd.DataFrame.from_dict(data=ltcFeature, orient='columns').to_csv('ltcFeature.csv', mode='a',
                                                                     header=not ltc_file_exists)

    formatted_ltc_tweets = []

    # etherium
    j_eth_info = json.loads(eth_price_info)
    eth_change = j_eth_info['ticker']['change']
    eth_volume = j_eth_info['ticker']['volume']
    eth_timestamp = j_eth_info['timestamp']
    # average compound
    eth_average_compound = float(sum(d['sentiment']['compound'] for d in formatted_eth_tweets)) / len(
        formatted_eth_tweets)

    ethFeature = {'TimeStamp': [eth_timestamp], 'Sentiment': [eth_average_compound], 'Volume': [eth_volume],
                  'Change': [eth_change]}

    eth_predict_change = predict.generate_linear_prediction_model(ethFeature, "/home/tomas/PycharmProjects/CollegeProject/ethFeature.csv")

    print( "The sentiment of the last 15 minutes for eth is : " + str(ethFeature['Sentiment'][0]) + " - The predicted change in price is :" + eth_predict_change)

    pd.DataFrame.from_dict(data=ethFeature, orient='columns').to_csv('ethFeature.csv', mode='a',
                                                                     header=not eth_file_exists)

    formatted_eth_tweets = []

sched.start()