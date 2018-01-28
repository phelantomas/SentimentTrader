import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import datetime
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import collect_tweets, collect_prices, process_tweets, json

import pandas as pd
import os.path
import predict
import datetime
import matplotlib

import random

formatted_btc_tweets = []
formatted_ltc_tweets = []
formatted_eth_tweets = []
btc_predict_change = 0
ltc_predict_change = 0
eth_predict_change = 0
btc_predict_change_model = None
ltc_predict_change_model = None
eth_predict_change_model = None
num_of_passes = 0

class SentimentTrader(QTabWidget):
    def __init__(self, parent=None):
        super(SentimentTrader, self).__init__(parent)
        self.home = QWidget()
        self.bitcoin_home = QWidget()
        self.litecoin_home = QWidget()
        self.etherium_home = QWidget()




        self.addTab(self.home, "Home")
        self.addTab(self.bitcoin_home, "Bitcoin")
        self.addTab(self.litecoin_home, "Litecoin")
        self.addTab(self.etherium_home, "Etherium")

        self.btc_predict_label = QLabel()
        self.ltc_predict_label = QLabel()
        self.eth_predict_label = QLabel()

        #header = ['TimeStamp', 'Tweet', 'Sentiment']

        self.btc_table = QTableWidget()

        header = ['TimeStamp', 'Tweet', 'Sentiment']

        self.btc_table.setColumnCount(3)
        self.btc_table.setColumnWidth(0, 170)
        #self.btc_table.setColumnWidth(1, 800)
        self.btc_table.setColumnWidth(2, 80)


        #self.btc_table.setSizeAdjustPolicy(self.bitcoin_home.QAbstractScrollArea.AdjustToContents)
       


        self.btc_table.setHorizontalHeaderLabels(header)

        #self.btc_table.setHorizontalHeaderLabels(header)  # a figure instance to plot on
        self.figure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        self.collect_data()

        self.home_UI()
        self.bitcoin_home_UI()
        self.litecoin_home_UI()
        self.etherium_home_UI()
        self.setWindowTitle("Sentment Trader")
        self.resize(1450, 720)

    def home_UI(self):
        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())
        self.setTabText(0, "Home")
        self.home.setLayout(layout)

    def bitcoin_home_UI(self):
        layout = QFormLayout()
        self.btc_predict_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.btc_predict_label)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.btc_table)


        self.setTabText(1, "Bitcoin")
        #layout.addWidget(scroll)
        self.bitcoin_home.setLayout(layout)

    def litecoin_home_UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        self.setTabText(2, "Litecoin")
        self.litecoin_home.setLayout(layout)

    def etherium_home_UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        self.setTabText(3, "Etherium")
        self.etherium_home.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()

    def analyse_data(self, formatted_tweets, filename, exchange, coin):
        global predict_change

        btcTweetsInHour = []
        # remove duplicated tweets
        formatted_tweets = [i for n, i in enumerate(formatted_tweets) if i not in formatted_tweets[n + 1:]]

        print("Number of unique tweets in an hour for " + coin + " is " + str(len(formatted_tweets)))

        tweets_from_one_hour = datetime.datetime.now() - datetime.timedelta(hours=1)

        for tweet in formatted_tweets:
            created_at = datetime.datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S')
            if created_at > tweets_from_one_hour:
                btcTweetsInHour.append(tweet)

        print("Number of unique tweets in an hour for " + coin + " is " + str(len(btcTweetsInHour)))

        file_exists = os.path.isfile(filename)

        price_info = collect_prices.get_price_info(exchange)

        j_info = json.loads(price_info)
        change = j_info['ticker']['change']
        volume = j_info['ticker']['volume']
        price = j_info['ticker']['price']
        timestamp = j_info['timestamp']

        # average compound
        average_compound = float(sum(d['sentiment']['compound'] for d in btcTweetsInHour)) / len(
            btcTweetsInHour)

        cryptoFeature = {'TimeStamp': [timestamp], 'Sentiment': [average_compound], 'Volume': [volume],
                         'Change': [change], 'Price': [price], 'NoOfTweets': [len(btcTweetsInHour)]}

        pd.DataFrame.from_dict(data=cryptoFeature, orient='columns').to_csv(filename, mode='a',
                                                                            header=not file_exists)
        # Make
        predict_change = predict.generate_linear_prediction_model(cryptoFeature, filename)

        if (predict_change):
            print("The sentiment of the last 60 minutes for " + coin + " is : " + str(
                cryptoFeature['Sentiment'][0]) + " - The predicted change in price is : " + predict_change)

    def collect_data(self):
        #threading.Timer(60.0, collect_data).start()  # called every minute
        self.plot()

        global formatted_btc_tweets
        global formatted_ltc_tweets
        global formatted_eth_tweets
        global num_of_passes
        global btc_predict_change
        global btc_predict_change_model
        global btc_var_pred_text
        global btcTree

        num_of_passes = num_of_passes + 1

        print('Pass number : ' + str(num_of_passes))

        # bitcoin
        btcTweets = collect_tweets.collect_tweets('bitcoin')
        btcTweets = process_tweets.process_tweets_from_main(btcTweets)


        formatted_btc_tweets.extend(btcTweets)

        #clear table
        self.btc_table.setRowCount(0)
        row = 0
        numOfRows = len(formatted_btc_tweets)
        self.btc_table.setRowCount(numOfRows)

        for tweet in formatted_btc_tweets:
            print(str(tweet['formatted_text'].encode('utf8')))
            self.btc_table.setItem(row,0, QTableWidgetItem(str(tweet['created_at'])))
            self.btc_table.setItem(row,1, QTableWidgetItem(str(tweet['formatted_text'].encode('utf8'))))    #tweet['formatted_text']
            self.btc_table.setItem(row,2, QTableWidgetItem(str(tweet['sentiment']['compound'])))
            self.btc_table.resizeColumnsToContents()
            row = row + 1

        if btc_predict_change_model is None:
            btc_predict_change_model = predict.generate_linear_prediction_model_init("btcFeature.csv")

        # Generate new prediction every minute

        # average compound
        average_compound = float(sum(d['sentiment']['compound'] for d in formatted_btc_tweets)) / len(
            formatted_btc_tweets)

        regFeature = {'Sentiment': [average_compound]}

        dfFeature = pd.DataFrame(regFeature)

        btc_predict_change = str(btc_predict_change_model.predict(dfFeature))

        self.btc_predict_label.setText("Predicted change in price is " + str(btc_predict_change))
        #if btc_var_pred_text:
        #    btc_var_pred_text.set("Predicted change in price is " + str(btc_predict_change))

        # litecoin
        ltcTweets = collect_tweets.collect_tweets('litecoin')
        ltcTweets = process_tweets.process_tweets_from_main(ltcTweets)

        formatted_ltc_tweets.extend(ltcTweets)

        # etherium
        ethTweets = collect_tweets.collect_tweets('etherium')
        ethTweets = process_tweets.process_tweets_from_main(ethTweets)

        formatted_eth_tweets.extend(ethTweets)

        if (num_of_passes is 60):
            num_of_passes = 0

            self.analyse_data(formatted_btc_tweets, "btcFeature.csv", "btc-usd", "Bitcoin")
            formatted_btc_tweets = []
            self.analyse_data(formatted_ltc_tweets, "ltcFeature.csv", "ltc-usd", "Litecoin")
            formatted_ltc_tweets = []
            self.analyse_data(formatted_eth_tweets, "ethFeature.csv", "eth-usd", "Etherium")
            formatted_eth_tweets = []


def main():
    app = QApplication(sys.argv)


    window = SentimentTrader()
    timer = QTimer()
    timer.timeout.connect(window.collect_data)
    timer.start(60000)  #
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()