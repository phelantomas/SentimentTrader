import datetime
import os.path
import sys
import threading
import multiprocessing
#from twisted.internet import task
#from twisted.internet import reactor
import time
from PyQt4 import QtCore

import pandas as pd
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import collect_prices
import collect_tweets
import json
import predict
import process_tweets
import notify
import notify_config

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

class SentimentTraderWindow(QTabWidget):
    def __init__(self, parent=None):
        super(SentimentTraderWindow, self).__init__(parent)
        self.workerThread = WorkerThread()

        self.connect(self.workerThread, QtCore.SIGNAL("update_tweets_table"), self.update_tweets_table)

        self.loop = 0
        self.home = QWidget()
        self.bitcoin_home = QScrollArea()
        self.bitcoin_home.setWidgetResizable(True)
        self.litecoin_home = QWidget()
        self.etherium_home = QWidget()

        self.addTab(self.home, "Home")
        self.addTab(self.bitcoin_home, "Bitcoin")
        self.addTab(self.litecoin_home, "Litecoin")
        self.addTab(self.etherium_home, "Etherium")

        self.btc_predict_label = QLabel()
        self.ltc_predict_label = QLabel()
        self.eth_predict_label = QLabel()

        self.btc_sentiment_label = QLabel()
        self.btc_price_label = QLabel()

        self.btc_table = QTableWidget()

        #####
        self.list_actual_change = []
        self.list_predicted_change = []
        ####

        #plotting bitcoin
        self.btc_xlist = []
        self.btc_y_actual_list = []
        self.btc_y_predict_list = []
        self.btc_current_price = []
        self.btc_plot_time = []

        # plotting litecoin
        self.ltc_xlist = []
        self.ltc_y_actual_list = []
        self.ltc_y_predict_list = []
        self.ltc_current_price = []
        self.ltc_plot_time = []

        header = ['TimeStamp', 'Tweet', 'Sentiment']

        self.btc_table.setColumnCount(3)
        self.btc_table.setColumnWidth(0, 170)
        self.btc_table.setColumnWidth(1, 800)

        self.btc_table.setHorizontalHeaderLabels(header)
        self.btc_table.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)

        self.btcFigure = Figure()
        self.ltcFigure = Figure()
        self.ethFigure = Figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.btcCanvas = FigureCanvas(self.btcFigure)
        self.ltcCanvas = FigureCanvas(self.ltcFigure)
        self.ethCanvas = FigureCanvas(self.ethFigure)

        self.btc_ax = self.btcFigure.add_subplot(111)
        self.ltc_ax = self.btcFigure.add_subplot(111)
        self.eth_ax = self.btcFigure.add_subplot(111)

        #self.plot(1,1,1)
####rememember!!!self.collect_data()

        self.home_UI()
        self.bitcoin_home_UI()
        self.litecoin_home_UI()
        self.etherium_home_UI()
        self.setWindowTitle("Sentment Trader")
        self.resize(1450, 720)

        self.process_data()

    def home_UI(self):
        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())
        self.setTabText(0, "Home")
        self.home.setLayout(layout)

    def bitcoin_home_UI(self):
        layout = QFormLayout() #QFormLayout()
        self.btc_predict_label.setAlignment(Qt.AlignCenter)
        self.btc_sentiment_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.btc_sentiment_label)
        layout.addWidget(self.btc_predict_label)
        layout.addWidget(self.btc_price_label)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.btc_toolbar = NavigationToolbar(self.btcCanvas, self)

        layout.addWidget(self.btc_toolbar)
        layout.addWidget(self.btcCanvas)
        layout.addWidget(self.btc_table)


        self.setTabText(1, "Bitcoin")
        self.bitcoin_home.setLayout(layout)

    def litecoin_home_UI(self):
        layout = QFormLayout()

        self.ltc_toolbar = NavigationToolbar(self.ltcCanvas, self)

        layout.addWidget(self.ltc_toolbar)
        layout.addWidget(self.ltcCanvas)
        #layout.addWidget(self.btc_table)

        self.setTabText(2, "Litecoin")
        self.litecoin_home.setLayout(layout)

    def etherium_home_UI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        self.setTabText(3, "Etherium")
        self.etherium_home.setLayout(layout)

    def plot(self, predict_change, current_price, plot_time, y_predict_list, currency):
        ''' plot change'''
        if len(y_predict_list) is 0:#Init
            y_predict_list.append(current_price[-1])

        print("Current " + str(current_price[-1]))
        y_predict_list.append(float(current_price[-1]) + float(predict_change))

        if len(current_price) > 8:
            current_price_graph = current_price[-8:]
            y_predict_list_graph = y_predict_list[-9:]
            predict_xList = plot_time[-8:]
        else:
            current_price_graph = current_price
            y_predict_list_graph = y_predict_list
            predict_xList = plot_time[:]
        predict_xList.append("Predicted Change")

        y_predict_list_graph = [round(float(i)) for i in y_predict_list_graph]
        current_price_graph = [round(float(i)) for i in current_price_graph]

        if currency == "Bitcoin":
            ax = self.btcFigure.add_subplot(111)
            ax.clear()
            ax.cla()
            ax.remove()
            ax = self.btcFigure.add_subplot(111)
            ax.set_title('Bitcoin Price Previous Hours')
            ax.set_ylabel('Price ($)')
            ax.set_xlabel('Time (h)')
            ax.grid()
            ax.set_ylim((min(y_predict_list_graph) - 50), (max(y_predict_list_graph) + 50))
        elif currency == "Litecoin":
            ax = self.ltcFigure.add_subplot(111)
            ax.clear()
            ax.cla()
            ax.remove()
            ax = self.ltcFigure.add_subplot(111)
            ax.set_title('Litecoin Price Previous Hours')
            ax.set_ylabel('Price ($)')
            ax.set_xlabel('Time (h)')
            ax.grid()
            ax.set_ylim((min(y_predict_list_graph) - 1), (max(y_predict_list_graph) + 1))

        print(current_price_graph)
        print(predict_xList)
        print(y_predict_list_graph)

        ax.plot(predict_xList[:-1], current_price_graph, label='Actual Price')
        ax.plot(predict_xList, y_predict_list_graph, label='Linear Prediction')
        ax.legend(loc='upper left')
        if currency == "Bitcoin":
            self.btcCanvas.draw_idle()
        elif currency == "Litecoin":
            self.ltcCanvas.draw_idle()

    def process_data(self):
        self.workerThread.start()

    def update_tweets_table(self, tweets):
        row = 0
        # do at end
        for tweet in tweets:
            rowPosition = self.btc_table.rowCount()
            self.btc_table.insertRow(rowPosition)
            self.btc_table.setItem(rowPosition, 0, QTableWidgetItem(str(tweet['created_at'])))
            self.btc_table.setItem(rowPosition, 1, QTableWidgetItem(
                str(tweet['formatted_text'].encode('utf8'))))  # tweet['formatted_text']
            self.btc_table.setItem(rowPosition, 2, QTableWidgetItem(str(tweet['sentiment']['compound'])))
            row = row + 1

class WorkerThread(QThread):
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        #window = SentimentTraderWindow()

    def analyse_data(self, formatted_tweets, filename, exchange, coin, current_price, plot_time, y_predict_list):
        global predict_change

        while self.btc_table.rowCount() > 0:
            self.btc_table.removeRow(0)
        self.btc_table.setRowCount(0)

        tweetsInHour = []
        # remove duplicated tweets
        formatted_tweets = [i for n, i in enumerate(formatted_tweets) if i not in formatted_tweets[n + 1:]]

        print("Number of unique tweets in an hour for " + coin + " is " + str(len(formatted_tweets)))

        tweets_from_one_hour = datetime.datetime.now() - datetime.timedelta(hours=2)#2 hours now due to time saving

        for tweet in formatted_tweets:
            created_at = datetime.datetime.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S')
            if created_at > tweets_from_one_hour:
                tweetsInHour.append(tweet)
        formatted_tweets = []

        print("Number of unique tweets in an hour for " + coin + " is " + str(len(tweetsInHour)))

        file_exists = os.path.isfile(filename)

        timeout = 1
        str_error = "No price yet"
        while str_error:
            try:
                price_info = collect_prices.get_price_info(exchange)
                j_info = json.loads(price_info)
                str_error = None
            except Exception as str_error:
                print(str_error)
                time.sleep(timeout)
                #timeout *= 1

        change = j_info['ticker']['change']
        volume = j_info['ticker']['volume']
        price = j_info['ticker']['price']
        timestamp = j_info['timestamp']

        # average compound
        average_compound = float(sum(d['sentiment']['compound'] for d in tweetsInHour)) / len(
            tweetsInHour)

        cryptoFeature = {'TimeStamp': [timestamp], 'Sentiment': [average_compound], 'Volume': [volume],
                         'Change': [change], 'Price': [price], 'NoOfTweets': [len(tweetsInHour)]}

        pd.DataFrame.from_dict(data=cryptoFeature, orient='columns').to_csv(filename, mode='a',
                                                                            header=not file_exists)
        # Make
        predict_change = predict.generate_linear_prediction_model(cryptoFeature, filename)

        if (float(predict_change) >= notify_config.BITCOIN_PRICE_ABOVE or float(predict_change)
                <= notify_config.BITCOIN_PRICE_BELOW):
            notify.push_notification(predict_change, "Bitcoin")

        #Plotting
        current_price.append(price)
        plot_time.append(datetime.datetime.now().strftime("%H:%M:%S"))
        print(predict_change)

        self.plot(predict_change, current_price, plot_time, y_predict_list, coin)

        self.btc_sentiment_label.setText("The current sentiment is " + str(average_compound))
        self.btc_predict_label.setText("Predicted change in price is " + str(btc_predict_change))
        self.btc_price_label.setText("Actual change in price is " + str(change))

        if (predict_change):
            print("The sentiment of the last 60 minutes for " + coin + " is : " + str(
                cryptoFeature['Sentiment'][0]) + " - The predicted change in price is : " + predict_change)

    def run(self):
        global formatted_btc_tweets
        global formatted_ltc_tweets
        global formatted_eth_tweets
        global num_of_passes
        global btc_predict_change
        global btc_predict_change_model
        global ltc_predict_change_model
        global btc_var_pred_text
        global btcTree

        num_of_passes = num_of_passes + 1

        print('Pass number : ' + str(num_of_passes))

        # bitcoin
        btcTweets = collect_tweets.collect_tweets('bitcoin')
        btcTweets = process_tweets.process_tweets_from_main(btcTweets)

        formatted_btc_tweets.extend(btcTweets)

        formatted_btc_tweets = [i for n, i in enumerate(formatted_btc_tweets) if i not in formatted_btc_tweets[n + 1:]]


        if(float(btc_predict_change) >= notify_config.BITCOIN_PRICE_ABOVE or float(btc_predict_change) <= notify_config.BITCOIN_PRICE_BELOW):
            notify.push_notification(btc_predict_change, "Bitcoin")

        # litecoin
        ltcTweets = collect_tweets.collect_tweets('litecoin')
        ltcTweets = process_tweets.process_tweets_from_main(ltcTweets)

        formatted_ltc_tweets.extend(ltcTweets)

        # etherium
        ethTweets = collect_tweets.collect_tweets('etherium')
        ethTweets = process_tweets.process_tweets_from_main(ethTweets)

        formatted_eth_tweets.extend(ethTweets)

        self.emit(SIGNAL("update_tweets_table"), formatted_btc_tweets)

        if (num_of_passes is 3):
            num_of_passes = 0
            self.analyse_data(formatted_btc_tweets, "btcFeature.csv", "btc-usd", "Bitcoin", self.btc_current_price, self.btc_plot_time, self.btc_y_predict_list,)
            self.analyse_data(formatted_ltc_tweets, "ltcFeature.csv", "ltc-usd", "Litecoin", self.ltc_current_price, self.ltc_plot_time, self.ltc_y_predict_list)

           # self.analyse_data(formatted_eth_tweets, "ethFeature.csv", "eth-usd", "Etherium")
            #formatted_eth_tweets = []


def main():
    app = QApplication(sys.argv)
    window = SentimentTraderWindow()
    timer = QTimer()
    timer.timeout.connect(window.process_data)
    timer.start(60000)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()