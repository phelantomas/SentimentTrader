'''
Author: Tomas Phelan
License Employed: GNU General Public License v3.0
Brief:
'''

import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import log_creater as lc
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing
from sklearn import utils
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.model_selection import cross_val_score
import os

# file logger
sentiment_logger = lc.setup_logger('second_logger', 'sentiment_logfile.log')

def generate_linear_prediction_model_init(file):
      try:
            lm = LinearRegression()
            df = pd.read_csv(file, error_bad_lines=False)
            X = df['Sentiment']
            Y = df['Change']

            X = X.values.reshape(len(X), 1)
            Y = Y.values.reshape(len(Y), 1)

            lm.fit(X, Y)

            return lm
      except:
            print("Not enough values yet.")

def generate_linear_prediction_model(feature, file):
      try:
            lm = LinearRegression()
            df = pd.read_csv(file, error_bad_lines=False)

            shift = -1
            df.Change = df.Change.shift(shift)
            df = df.dropna()
            X = df['Sentiment']
            Y = df['Change']

            X = X.values.reshape(len(X), 1)
            Y = Y.values.reshape(len(Y), 1)

            lm.fit(X, Y)

            sentiment = feature['Sentiment'][0]

            regFeature = {'Sentiment': [sentiment]}

            dfFeature = pd.DataFrame(regFeature)

            predicted_change = str(lm.predict(dfFeature)[0][0])
            log_info = "The sentiment of the last 60 minutes is : " + str(sentiment) + " - The predicted change in price is :" + predicted_change

            return predicted_change
      except:
            print("Not enough values yet.")


def generate_forest_prediction_model(feature, file):
      try:
            rf = RandomForestRegressor()
            df = pd.read_csv(file, error_bad_lines=False)
            shift = -1
            df.Change = df.Change.shift(shift)
            df = df.dropna()

            X = df['Sentiment']
            Y = df['Change']

            X = X.values.reshape(len(X), 1)
            Y = Y.values.reshape(len(Y), 1)

            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=5)

            rf.fit(X, Y)

            sentiment = feature['Sentiment'][0]

            regFeature = {'Sentiment': [sentiment]}

            dfFeature = pd.DataFrame(regFeature)

            predicted_change = str(rf.predict(dfFeature)[0])

            return predicted_change
      except Exception as e:
            print("Not enough values yet. " + str(e))

def test_accuracy(regr, X_test, y_test):
      # Make predictions using the testing set
      y_pred = regr.predict(X_test)

      # The coefficients
      print('Coefficients: \n', regr.coef_)
      # The mean squared error
      print("Mean squared error: %.2f"
            % mean_squared_error(y_test, y_pred))
      # Explained variance score: 1 is perfect prediction
      print('Variance score: %.2f' % r2_score(y_test, y_pred))

      error = np.mean(y_pred != y_test)
      print(y_pred)
      print(y_test)
      print(error)

      return regr


