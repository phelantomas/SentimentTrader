def plot(self, ax, predicted_change, actual_change, current_price):
    ''' plot change'''
    # last_hour = actual_change
    # self.list_actual_change.append(actual_change)
    self.btc_current_price.append(current_price)
    self.btc_y_actual_list.append(actual_change)
    self.plot_time.append(datetime.datetime.now().strftime("%H:%M:%S"))

    if len(self.btc_y_predict_list) is 0:  # Init
        self.btc_y_predict_list.append(current_price)
        self.loop = 1
    self.btc_y_predict_list.append(float(current_price) + float(predicted_change))

    i = 0
    xList = []
    yList = self.btc_current_price
    for x in yList:
        xList.append(i)
        i = i + 1

    if len(self.btc_current_price) > 8:
        btc_current_price_graph = self.btc_current_price[-8:]
        btc_y_predict_list_graph = self.btc_y_predict_list[-9:]
        xList = xList[-8:]
        xList[:] = [x - self.loop for x in xList]
        self.loop = self.loop + 1
        predict_xList = self.plot_time[-8:]
    else:
        btc_current_price_graph = self.btc_current_price
        btc_y_predict_list_graph = self.btc_y_predict_list
        predict_xList = self.plot_time[:]
    predict_xList.append("Predicted Change")

    btc_y_predict_list_graph = [round(float(i)) for i in btc_y_predict_list_graph]
    btc_current_price_graph = [round(float(i)) for i in btc_current_price_graph]

    ax = self.btcFigure.add_subplot(111)
    ax.clear()
    ax.cla()
    ax.remove()
    ax = self.btcFigure.add_subplot(111)
    ax.set_title('Bitcoin Price Previous Hours')
    ax.set_ylabel('Price ($)')
    ax.set_xlabel('Time (h)')
    ax.grid()

    print(xList)
    print(btc_current_price_graph)
    print(predict_xList)
    print(btc_y_predict_list_graph)

    ax.set_ylim((min(btc_y_predict_list_graph) - 10), (max(btc_y_predict_list_graph) + 10))
    ax.plot(predict_xList[:-1], btc_current_price_graph, label='Actual Price')
    ax.plot(predict_xList, btc_y_predict_list_graph, label='Linear Prediction')
    ax.legend(loc='upper left')
    self.btcCanvas.draw_idle()