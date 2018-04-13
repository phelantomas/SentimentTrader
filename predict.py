'''
Author: Tomas Phelan
License Employed: GNU General Public License v3.0
Brief:
'''

from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm

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

            return predicted_change
      except:
            print("Not enough values yet.")
            return None

def generate_multi_linear_prediction_model(feature, file):
      try:
            df = pd.read_csv(file, error_bad_lines=False)

            shift = -1
            df.Change = df.Change.shift(shift)
            df = df.dropna()

            targets = pd.DataFrame(df, columns=["Change"])

            X = df[["NoOfTweets", "Sentiment", "Volume"]]
            y = targets["Change"]

            model = sm.OLS(y, X).fit()

            sentiment = feature['Sentiment'][0]
            volume = float(feature['Volume'][0])
            noOfTweets = feature['NoOfTweets'][0]

            regFeature = {"NoOfTweets": noOfTweets,'Sentiment': [sentiment], 'Volume': [volume]}

            dfFeature = pd.DataFrame(regFeature)

            predicted_change = str(model.predict(dfFeature).values[0])

            return predicted_change
      except:
            print("Not enough values yet.")
            return None

def generate_forest_prediction_model(feature, file):
      try:
            rf = RandomForestRegressor()
            df = pd.read_csv(file, error_bad_lines=False)
            shift = -1
            df.Change = df.Change.shift(shift)
            df = df.dropna()

            X = df[["NoOfTweets", "Sentiment", "Volume"]]
            Y = df['Change']

            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=5)

            rf.fit(X, Y.ravel())

            sentiment = feature['Sentiment'][0]
            volume = float(feature['Volume'][0])
            noOfTweets = feature['NoOfTweets'][0]

            regFeature = {"NoOfTweets": noOfTweets, 'Sentiment': [sentiment], 'Volume': [volume]}

            dfFeature = pd.DataFrame(regFeature)

            predicted_change = str(rf.predict(dfFeature)[0])

            return predicted_change
      except Exception as e:
            print("Not enough values yet. " + str(e))
            return None

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


