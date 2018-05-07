from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier 
from sklearn.model_selection import cross_val_score

import numpy as np

classicaldata = open('data_label=0.csv', 'r').read().split('NEXTSONG')
crowdata = [row.split('\n') for row in classicaldata] 
crowdata.remove([''])
for i, row in enumerate(crowdata):
    row.remove('')
    if len(row) > 0:
        for j, entry in enumerate(row):
            crowdata[i][j] = entry.split(',')

jazzdata = open('data_label=1.csv', 'r').read().split('NEXTSONG')
jrowdata = [row.split('\n') for row in jazzdata]
jrowdata.remove([''])
for i, row in enumerate(jrowdata):
    row.remove('')
    if len(row) > 0:
        for j, entry in enumerate(row):
            jrowdata[i][j] = entry.split(',')

trainingdata = np.vstack((np.array(crowdata), np.array(jrowdata)))
#num_features = np.shape(trainingdata)[1] - 1
#print(num_features)
features = trainingdata[:,:5,:20]
labels = trainingdata[:,0,20]
#print(len(labels))
#print(labels)
#quit()
#fixedlabels = np.zeros(np.shape(features)[0])
#for i, labelset in enumerate((labels)):
#    fixedlabels[i] = labelset[len(labelset) - 1]
#labels = fixedlabels

fixedfeatures = np.zeros((len(features), len(features[0].flatten())), dtype='int32')
for i, feature in enumerate(features):
    fixedfeatures[i] = feature.flatten()[0:len(feature.flatten())] 
features = fixedfeatures


print("Testing KNN, 10-Fold CV")
Ks = [1, 3, 5, 7, 9, 13, 21, 49, 101]
for K in Ks:
    classifier = KNeighborsClassifier(K)
    scores = cross_val_score(classifier, features, labels, cv=10)
    print("Error: %0.3f (+/- %0.3f) for k=%d" % (1 - scores.mean(), scores.std() * 2, K))
print()

print("Testing Decision Tree")
depths = [i + 1 for i in range((100))]
for depth in depths:
    classifier = tree.DecisionTreeClassifier(max_depth=depth)
    scores = cross_val_score(classifier, features, labels, cv=10)
    print("Error: %0.3f (+/- %0.3f) for depth=%d" % (1 - scores.mean(), scores.std() * 2, depth))
print()

print("Adaboosting")
numEstimators = [i for i in range(2, 16)]
for num in numEstimators:
    classifier = AdaBoostClassifier(n_estimators=num) 
    scores = cross_val_score(classifier, features, labels, cv=10)
    print("Error: %0.3f (+/- %0.3f) for num_estimators=%d" % (1 - scores.mean(), scores.std() * 2, num))
print()

print("Gradient Boosting")
numEstimators = [i for i in range(25, 39, 1)]
for num in numEstimators:
    classifier = GradientBoostingClassifier(n_estimators=num) 
    scores = cross_val_score(classifier, features, labels, cv=10)
    print("Error: %0.3f (+/- %0.3f) for num_estimators=%d" % (1 - scores.mean(), scores.std() * 2, num))
print()
