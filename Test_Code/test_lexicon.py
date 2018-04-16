from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

sia = SIA()

max_value = max(sia.lexicon, key=sia.lexicon.get)
min_value = min(sia.lexicon, key=sia.lexicon.get)
print(max_value, sia.lexicon[max_value])
print(min_value, sia.lexicon[min_value])

crypto_slang = {u'bullish':-1.4, u'ath': 3.0,u'ico':1.0,u'shilling':-2.0,u'fomo':-3.0,u'fudster':-3.2,u'bagholder':-1.3,u'sharding':1.1,
                u'dapp':1.5,u'wei':1.0,u'hodl':3.5, u'lambo': 4.0,u'mooning':2.6,u'satoshi':2.5}

#Check if they exist
print(sia.polarity_scores('lets hodle'))
print(sia.polarity_scores('bullish'))
print(sia.polarity_scores('ath'))
print(sia.polarity_scores('ico'))
print(sia.polarity_scores('shilling'))
print(sia.polarity_scores('fomo'))
print(sia.polarity_scores('fud'))
print(sia.polarity_scores('fudster'))
print(sia.polarity_scores('bagholder'))
print(sia.polarity_scores('sharding'))
print(sia.polarity_scores('dapp'))
print(sia.polarity_scores('wei'))
print(sia.polarity_scores('hodl'))
print(sia.polarity_scores('lambo'))
print(sia.polarity_scores('mooning'))
print(sia.polarity_scores('satoshi'))

#Add to lexicon
sia.lexicon.update(crypto_slang)

print(sia.polarity_scores('lets hodle'))
print("bullish", sia.polarity_scores('bullish'))
print('ath',sia.polarity_scores('ath'))
print('ico', sia.polarity_scores('ico'))
print('shilling', sia.polarity_scores('shilling'))
print('fomo', sia.polarity_scores('fomo'))
print('fudster', sia.polarity_scores('fudster'))
print('bagholder',sia.polarity_scores('bagholder'))
print('sharding', sia.polarity_scores('sharding'))
print('dapp', sia.polarity_scores('dapp'))
print('wei', sia.polarity_scores('wei'))
print('hodl', sia.polarity_scores('hodl'))
print('lambo',sia.polarity_scores('lambo'))
print('mooning', sia.polarity_scores('mooning'))
print('satoshi', sia.polarity_scores('satoshi'))
