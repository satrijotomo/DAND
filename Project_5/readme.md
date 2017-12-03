## Predict Person of Interest (POI) in Enron Case

Enron was an American energy company based in Houston, Texas and formed in 1985 by Kenneth Lay after merging Houston Natural Gas and InterNorth. The Enron scandal, publicized in October 2001, eventually led to the bankruptcy of the Enron Corporation. It was the largest bankruptcy reorganization in American history at that time.

In this project we will identify Enron employees who may have committed fraud. The identification is based on machine learning algorithms applied into the public Enron financial and email dataset. The target label is 'poi' or person of interest. There are total 146 data points (rows) in the dataset and each has features (columns) represent financial and email data.

The python script is based on Python 2.7. Because it is desirable to persist the model for future use without having to retrain, I use pickle at the end of the script for this purpose.

