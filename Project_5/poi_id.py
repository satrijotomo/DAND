#!/Users/macbook/anaconda/envs/py2/bin/python

import sys
import pickle
sys.path.append("../tools/")
import matplotlib.pyplot as plt
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
#from outlier_cleaner import outlierCleaner
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import tester
from time import time
from sklearn.cross_validation import train_test_split


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".


poi_feature = ['poi']
fin_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 
'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 
'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 
'director_fees']
email_features = ['to_messages', 'from_poi_to_this_person', 'from_messages', 
'from_this_person_to_poi', 'shared_receipt_with_poi']



### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
    
    
# Transform dictionary data into Panda Dataframe. Select orient = 'index' so that the 
# keys (Name) will be in rows. 
df = pd.DataFrame.from_dict(data_dict, orient = 'index')
df = df.replace('NaN', np.nan)


df.info()
print df.head()
print
poi_group = df.poi.value_counts()
poi_group.index = ['Non-POI  ','POI   ']
print '=== Count of POI and Non POI ==='
print poi_group
print

### Task 2: Remove outliers


## Replace NaN in Salary and Bonus with 0
df['salary'].replace(to_replace='NaN', value=0, inplace=True)
df['bonus'].replace(to_replace='NaN', value=0, inplace=True)
df.head()	

print ">> Remove Outliers"
print "Data Plot Before Removing Outlier"
print "================================="
df.plot.scatter('salary','bonus', s=30, c='red')
plt.show()

df['salary'].sort_values(ascending=False).head(6)
df['bonus'].sort_values(ascending=False).head(6)

# From the result above, remove the outliers. TOTAL is the obvious outlier. 
# SKILLING JEFFREY K, LAY KENNETH L, and BELDEN TIMOTHY N are also outliers, but since they 
# are identified as poi and there is only a small pool of poi persons compared to the non-poi, 
#we will keep them on the dataset. On the other hand, FREVERT MARK A, LAVORATO JOHN J, 
# PICKERING MARK R, and ALLEN PHILLIP K are not, so will remove them and plot the data again.

dropname = ['TOTAL','THE TRAVEL AGENCY IN THE PARK','FREVERT MARK A','LAVORATO JOHN J','ALLEN PHILLIP K','PICKERING MARK R']
df.drop(dropname, inplace=True)
print
print "Data Plot After Removing Outlier"
print "================================="
df.plot.scatter('salary','bonus', s=20, c='blue')
plt.show()
print


### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
# We will investigate the number of emails to and from POI for each person. However, since 
# there are big variance of values, we need to normalize the data. Two new features will be 
# created by using the following formula:
# 
# >norm_from_poi_to_this_person : from_poi_to_this_person / (from_messages + from_poi_to_this_person)
# >norm_from_this_person_to_poi : from_this_person_to_poi / (to_messages + from_this_person_to_poi)
 

print ">> Create 2 new features to normalized from/to poi email counts"
print('Creating norm_from_poi_to_this_person :')
df['norm_from_poi_to_this_person'] = df['from_poi_to_this_person']/(df['from_messages'] + 
df['from_poi_to_this_person'])
df[['from_messages','from_poi_to_this_person','norm_from_poi_to_this_person']].head()
print('Creating norm_from_this_person_to_poi :')
df['norm_from_this_person_to_poi'] = df['from_this_person_to_poi']/(df['to_messages'] + 
df['from_this_person_to_poi'])
df[['to_messages','from_this_person_to_poi','norm_from_this_person_to_poi']].head()
print
feature_list = ['poi',
 'salary',
 'deferral_payments',
 'total_payments',
 'bonus',
 'total_stock_value',
 'expenses',
 'exercised_stock_options',
 'long_term_incentive',
 'restricted_stock',
 'norm_from_poi_to_this_person',
 'norm_from_this_person_to_poi']

print "Included Features for Analysis are \n",  feature_list
print

scaled_features = ['salary',
 'deferral_payments',
 'total_payments',
 'bonus',
 'total_stock_value',
 'expenses',
 'exercised_stock_options',
 'long_term_incentive',
 'restricted_stock']
## Feature scaling
df = df.replace(np.nan, 0)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
## fit & transform
df[scaled_features] = scaler.fit_transform(df[scaled_features])
#print df[feature_list].head(5)


### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html


# We will try three classifiers to see which one of them has the highest accuracy. The 
# classifiers are:
# 1. Decision Tree
# 2. Random Forest
# 3. Adaboost
# 4. Naive Bayes


# Provided to give you a starting point. Try a variety of classifiers.


# Preparing dataset
my_dataset = df[feature_list].to_dict(orient = 'index')
data = featureFormat(my_dataset, feature_list, remove_all_zeroes=True, sort_keys = False)
labels, features = targetFeatureSplit(data)
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.25, random_state=42)


print ">> Try a varity of classifiers"
#4.1 Decision Tree

print "== Decision Tree =="
from sklearn import tree
print "Fitting the classifier to the training set"
t0 = time()
clf = tree.DecisionTreeClassifier(random_state=0)
clf.fit(features_train, labels_train)
pred = clf.predict(features_train)
print "Accuracy :%0.3f" % clf.score(features_test, labels_test)
print "Done in: %0.3fs" % (time() - t0)
print

#4.2 Random Forest

print "== Random Forest =="
from sklearn.ensemble import RandomForestClassifier
print "Fitting the classifier to the training set"
t0 = time()
clf = RandomForestClassifier(max_depth=1, random_state=0)
clf.fit(features_train, labels_train)

print "Accuracy :%0.3f" % clf.score(features_test, labels_test)
print "Done in: %0.3fs" % (time() - t0)
print

#4.3 Adaboost

print "== Adaboost =="
from sklearn.ensemble import AdaBoostClassifier
print "Fitting the classifier to the training set"
t0 = time()
clf = AdaBoostClassifier(n_estimators=25,random_state=0)
clf.fit(features_train, labels_train)

print "Accuracy :%0.3f" % clf.score(features_test, labels_test)
print "Done in: %0.3fs" % (time() - t0)
print

#4.3 Gaussian Naive Bayes

print "== Gaussian NB =="
from sklearn.naive_bayes import GaussianNB
print "Fitting the classifier to the training set"
t0 = time()
clf = GaussianNB()
clf.fit(features_train, labels_train)

print "Accuracy :%0.3f" % clf.score(features_test, labels_test)
print "Done in: %0.3fs" % (time() - t0)
print

#The accuracy, precision, recall and F1 values of each classifier are summarized in below table.
# Note the time taken to run each algorithm can vary

print "== Summary =="
print pd.DataFrame([[0.771, 0.002],
              [0.886, 0.082],
              [0.829, 0.066],
              [0.800, 0.001]],
             columns = ['Accuracy','Time (sec)'], 
             index = ['1. Decision Tree Classifier', '2. Random Forest', '3. Adaboost',
                      '4. Gaussian Naive Bayes'])
print "Note: Time is for indication purpose only. Result may vary depending on evironment"
print

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
# Example starting point. Try investigating other evaluation techniques!


print ">> Tune Classifier"
print "Random Forest is selected algorithm to tune. Here we use cross validation to compare"
print "the performance before and after the tuning."
print

print "== Random Forest Before Tuning (Baseline) =="
from sklearn.ensemble import RandomForestClassifier
print "Fitting the classifier to the training set"
t0 = time()
clf = RandomForestClassifier(max_depth=1, random_state=0)
dataset_dict = df[feature_list].to_dict(orient = 'index')
tester.dump_classifier_and_data(clf, dataset_dict, feature_list)
tester.main()
print "Done in %0.3fs" % (time() - t0)
print

from sklearn.model_selection import GridSearchCV
print "== Finding best parameter combination for Random Forest =="
parameters = {'n_estimators':[5,10,20], 'max_features':[0.1, 0.2, 0.5]}
svc = RandomForestClassifier(max_depth=1)
t0 = time()
clf = GridSearchCV(svc, parameters)
clf.fit(features_train, labels_train)

#print "== Parameters to use : ==\n",clf.best_estimator_
print "Done in: %0.3fs" % (time() - t0)
print

print "== Random Forest After Tuning =="
from sklearn.ensemble import RandomForestClassifier
print "Fitting the classifier to the training set"
t0 = time()
clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=1, max_features=0.2, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            n_estimators=20, n_jobs=1, oob_score=False, random_state=0,
            verbose=0, warm_start=False)
dataset_dict = df[feature_list].to_dict(orient = 'index')
tester.dump_classifier_and_data(clf, dataset_dict, feature_list)
tester.main()
print "Done in %0.3fs" % (time() - t0)
print

print "== Tuning Summary  =="
print pd.DataFrame([[0.86764, 0.89730, 0.08300, 0.15195,34.923],
              [0.86336, 1.0000, 0.04350, 0.08337,94.093]],
             columns = ['Accuracy','Precision', 'Recall', 'F1','Time (sec)'], 
             index = ['1. RF - Before Tuning', '2. RF - After Tuning'])
print "Note: Time is for indication purpose only. Result may vary depending on evironment"
print
clf.fit(features_train, labels_train)
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
print("== Random Forest Feature ranking:")
for f in xrange(11):
    print "%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]])
print

## End note performance evaluation comparison with Decision Tree
print "For comparison with other algorithm, we evaluate Decision Tree by using tester.py"
print
print "== Decision Tree, default parameters  =="
print "Fitting the classifier to the training set"
t0 = time()
clf = tree.DecisionTreeClassifier(random_state=0)
dataset_dict = df[feature_list].to_dict(orient = 'index')
tester.dump_classifier_and_data(clf, dataset_dict, feature_list)
tester.main()
print "done in %0.3fs" % (time() - t0)
print



### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

#dump_classifier_and_data(clf, my_dataset, features_list)
print ">> Dump Classifier and Data"
dump_classifier_and_data(clf, dataset_dict, feature_list)
print "Dump is finished"
print
