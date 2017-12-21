import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('features.csv')

df.change = df.change.round()
df = df.drop("date", 1)

X = df.iloc[:, :-1]
y = df.iloc[:, -1:].values.ravel()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=5)


# Create linear regression object
regr = linear_model.LogisticRegression()

# Train the model using the training sets
regr.fit(X_train, y_train)

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


