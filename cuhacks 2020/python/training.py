import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn import tree, metrics
from sklearn.preprocessing import Imputer




train_data = pd.read_csv('bots_data.csv', encoding='latin1')
test_data = pd.read_csv('test.csv', encoding='latin1')

train_attr = train_data[
      ['followers_count', 'friends_count', 'listedcount', 'favourites_count', 'statuses_count', 'verified']]
train_label = train_data[['bot']]

test_attr = test_data[
  ['followers_count', 'friends_count', 'listed_count', 'favourites_count', 'statuses_count', 'verified']]
test_label = test_data[['bot']]


clf = tree.DecisionTreeClassifier()

X = train_attr.values
Y = train_label.values
clf = clf.fit(X, Y)
actual = np.array(test_label)
predicted = clf.predict(test_attr)
pred = np.array(predicted)



accuracy = accuracy_score(actual, pred) * 100
precision = precision_score(actual, pred) * 100
recall = recall_score(actual, pred) * 100
f1 = f1_score(actual, pred)
auc = roc_auc_score(actual, pred)
print('Accuracy is ', accuracy, 'Precision is', precision, 'Recall is ', recall, 'F1 Score is', f1, 'Area Under Curve is',  auc)

actual = np.array(test_label)
predicted = clf.predict(test_attr)
pred = np.array(predicted)

filename = 'finalized_model.sav'
pickle.dump(clf, open(filename, 'wb'))

#print(result)


