#TYPE can be "STOCK" or "CRYPTO"
#CRYPTOCURRENCY is the name, it will be used in the query so make sure it is correct.
#EXCHANGE is stock symbol or cyrpto symbol i.e GOOGL for stock and btc-usd for bitcoin
#FEATURE_FILE is where the features get saved
#PAST_PREDICTIONS_FILE is where past predictions are stored
#NUMBER_OF_MINUTES how long before doing predictions, default is 60
#GRAPH_SCALE scale of plotly graph
TYPE = "CRYPTO"
NAME = "Bitcoin"
EXCHANGE = "btc-usd"
FEATURE_FILE = "btcFeature.csv"
PAST_PREDICTIONS_FILE = "btcPastPredictions.csv"
NUMBER_OF_MINUTES = 5
GRAPH_SCALE = 3
THRESHOLD_ACCURACY = .1