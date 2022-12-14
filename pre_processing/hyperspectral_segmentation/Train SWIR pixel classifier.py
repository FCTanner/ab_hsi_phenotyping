#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm
import pickle

class Segmentation:
    Foreground = 1
    Background = 0

# 1.1 Load data
foreground = pd.read_csv("training_data/SWIR/pixel_values/swir_foreground_pixels.csv")
print("Foreground shape =", foreground.shape)
background_original = pd.read_csv("training_data/SWIR/pixel_values/swir_background_pixels.csv")
print("Background original shape =", background_original.shape)

n_foreground_pixels = foreground.shape[0]
background = background_original.sample(n_foreground_pixels, random_state=99)
print("Background sampled shape =", background.shape)

print("Background shape study_08 = ", background.shape)
print("Foreground shape study_08 = ", foreground.shape)


# 1.2 Label data
foreground['Segmentation'] = Segmentation.Foreground
background['Segmentation'] = Segmentation.Background
data = foreground.append(background)

print(data.head())
print(data.shape)

# 2. Test/train split
train, test = train_test_split(data, test_size= 0.3, random_state=33)
print(train.shape)
print(train.head())
train_x = train.drop('Segmentation', axis = 1).to_numpy()
train_y = train['Segmentation'].to_numpy()
test_x = test.drop('Segmentation', axis = 1).to_numpy()
test_y = test['Segmentation'].to_numpy()

# 2.2 Check split
print(train.groupby(['Segmentation']).count())
print(test.groupby(['Segmentation']).count())

print(train_x.shape)
print(train_y.shape)
print(test_x.shape)
print(test_y.shape)

# 3. Train
# 3.1 clf_svm
clf_svm = svm.SVC(kernel='rbf')
clf_svm.fit(train_x, train_y)

# 4. Predict
print(test_x[1:2,:].shape)
print(clf_svm.predict(test_x[1:100,:]))

# 5. Evaluation
# 5.1 Prediction accuracy
print("clf_svm prediction accuracy = ", clf_svm.score(test_x, test_y))

# 5.2 Parameter tuning
parameters = {'kernel': ('linear', 'rbf'), 'C': (1,4,8,16,32)}

svc = svm.SVC()
clf_tuned = GridSearchCV(svc, parameters, cv = 5)
clf_tuned.fit(train_x, train_y)
print("clf_tuned prediction accuracy = ", clf_tuned.score(test_x, test_y))

# 6. Save model
with open("training_data/SWIR/classifier/study_08_SWIR_SVM_pixel_classifier.pkl", "wb") as f:
    pickle.dump(clf_tuned, f)

