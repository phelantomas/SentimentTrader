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
import datetime

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

from Tkinter import *
import Tkinter as tk
import ttk

import pandas as pd

import threading


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)

formatted_btc_tweets = []
formatted_ltc_tweets = []
formatted_eth_tweets = []
predict_change = 0

twitter_logger = lc.setup_logger('first_logger', 'twitter_logfile.log')

sched = BlockingScheduler()
num_of_passes = 0

def animateBtcPrice(file, Num):
    pullData = pd.read_csv(file, error_bad_lines=False)

    pullData = pullData.tail(n=Num)
    xList = []
    yList = []
    index1 = 0
    for index, row in pullData.iterrows():
        xList.append(int(index1))
        yList.append(int(row['Price']))
        index1 = index1 + 1

    a.clear()
    a.plot(xList, yList)

def analyse_data(formatted_tweets, filename, exchange, coin):
    global predict_change

    btcTweetsInHour = []
    #remove duplicated tweets
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
                  'Change': [change], 'Price' : [price], 'NoOfTweets' : [len(btcTweetsInHour)]}

    pd.DataFrame.from_dict(data=cryptoFeature, orient='columns').to_csv(filename, mode='a',
                                                                     header=not file_exists)
    # Make
    predict_change = predict.generate_linear_prediction_model(cryptoFeature, filename)

    if(predict_change):
        print("The sentiment of the last 60 minutes for " + coin + " is : " + str(
        cryptoFeature['Sentiment'][0]) + " - The predicted change in price is : " + predict_change)


#@sched.scheduled_job('interval', minutes=1)
def timed_job():
    threading.Timer(60.0, timed_job).start()  # called every minute

    global formatted_btc_tweets
    global formatted_ltc_tweets
    global formatted_eth_tweets
    global num_of_passes

    num_of_passes = num_of_passes + 1

    print('Pass number : ' + str(num_of_passes))

    #bitcoin
    btcTweets = collect_tweets.collect_tweets('bitcoin')
    btcTweets = process_tweets.process_tweets_from_main(btcTweets)

    formatted_btc_tweets.extend(btcTweets)

    #litecoin
    ltcTweets = collect_tweets.collect_tweets('litecoin')
    ltcTweets = process_tweets.process_tweets_from_main(ltcTweets)

    formatted_ltc_tweets.extend(ltcTweets)

    #etherium
    ethTweets = collect_tweets.collect_tweets('etherium')
    ethTweets = process_tweets.process_tweets_from_main(ethTweets)

    formatted_eth_tweets.extend(ethTweets)

    if(num_of_passes is 60):
        num_of_passes = 0

        analyse_data(formatted_btc_tweets, "btcFeature.csv", "btc-usd", "Bitcoin")
        formatted_btc_tweets = []
        analyse_data(formatted_ltc_tweets, "ltcFeature.csv", "ltc-usd", "Litecoin")
        formatted_ltc_tweets = []
        analyse_data(formatted_eth_tweets, "ethFeature.csv", "eth-usd", "Etherium")
        formatted_eth_tweets = []

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, ) #default="clienticon.ico"
        tk.Tk.wm_title(self, "Sea of BTC client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageBtcTweets): #, MultiListbox
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("""Bitcoin trading application use at your own risk. There is no promise of warranty."""),
                         font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Bitcoin",
                            command=lambda: controller.show_frame(PageOne))
        button.pack(pady=10, padx=10, anchor='c')

        button2 = ttk.Button(self, text="Litecoin",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack(pady=10, padx=10, anchor='c')

        button3 = ttk.Button(self, text="Graph Page",
                             command=lambda: controller.show_frame(PageThree))
        button3.pack(pady=10, padx=10, anchor='c')


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        global predict_change

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Bitcoin", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label2 = tk.Label(self, text="Predicted change in price is " + str(predict_change), font=LARGE_FONT)
        label2.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10, padx=10)

        button2 = ttk.Button(self, text="Tweets",
                             command=lambda: controller.show_frame(PageBtcTweets))
        button2.pack(pady=10, padx=10)
        button3 = ttk.Button(self, text="Bitcoin Price",
                             command=lambda: controller.show_frame(PageThree))
        button3.pack(pady=10, padx=10)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Litecoin", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class PageBtcTweets(tk.Frame):

    def __init__(self, parent, controller):
        global formatted_btc_tweets
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="BTC Tweets", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Bitcoin Home",
                             command=lambda: controller.show_frame(PageOne))
        button1.pack()

        tree = ttk.Treeview(self, selectmode='browse')
        tree.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')

        tree.configure(yscrollcommand=vsb.set)

        tree["columns"] = ("1", "2", "3")
        tree['show'] = 'headings'
        tree.column("1", width=150, anchor='c', stretch=False)
        tree.column("2", width=900, anchor='w')
        tree.column("3", width=100, anchor='c', stretch=False)
        tree.heading("1", text="TimeStamp")
        tree.heading("2", text="Tweet")
        tree.heading("3", text="Sentiment")

        for tweet in formatted_btc_tweets:
            print(str(tweet['formatted_text']))
            tree.insert("", 'end', text="L1", values=(str(tweet['created_at']), str(tweet['formatted_text']), str(tweet['sentiment']['compound'])))


if __name__ == '__main__':
    timed_job()
    #sched.start()
    app = SeaofBTCapp()
    app.geometry("1280x720")
    ani = animation.FuncAnimation(f, animateBtcPrice("btcFeature.csv", 15), interval=1000)
    app.mainloop()
