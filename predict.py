import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
#import matplotlib.pyplot as plt
import logCreater as lc

# file logger
sentiment_logger = lc.setup_logger('second_logger', 'sentiment_logfile.log')

def generate_linear_prediction_model(feature):
      lm = LinearRegression()
      df = pd.read_csv('/home/tomas/PycharmProjects/CollegeProject/features.csv')
      X = df['sentiment']
      Y = df['change']

      X = X.values.reshape(len(X), 1)
      Y = Y.values.reshape(len(Y), 1)

      lm.fit(X, Y)

      sentiment = feature['Sentiment'][0]

      regFeature = {'sentiment': [sentiment]}

      dfFeature = pd.DataFrame(regFeature)
      log_info = "The sentiment of the last 15 minutes is : " + str(sentiment) + " - The predicted change in price is :" + str(lm.predict(dfFeature))
      print(log_info)
      sentiment_logger.info(log_info)

def generate_prediction_model(feature):
      df = pd.read_csv('/home/tomas/PycharmProjects/CollegeProject/features.csv')

      df.change = df.change.round()
      df = df.drop("date", 1)

      X = df.iloc[:, :-1]
      y = df.iloc[:, -1:].values.ravel()

      X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=5)


      # Create linear regression object
      regr = linear_model.LogisticRegression()

      # Train the model using the training sets
      regr.fit(X_train, y_train)

      sentiment = feature['Sentiment'][0]
      volume = feature['Volume'][0]

      regFeature = {'sentiment': [sentiment], 'volume': [volume]}

      dfFeature = pd.DataFrame(regFeature)
      print("The predicted change in price is :", regr.predict(dfFeature))

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


