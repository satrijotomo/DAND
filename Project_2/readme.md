## Project 2: Investigate a Dataset: Titanic survival data

Based on data of 91 of the 2224 passengers and crew on board the Titanic, I examined various variables in the dataset to find if there are correlations between them and the survivability of the passengers. The training dataset was retrieved from Kaggle.

Please note that the analysis does not utilize machine learning, and the correlation between variables are calculated by using Pearson R score.

https://www.kaggle.com/c/titanic/data

## Conclusion
By looking at the Pearson coefficient, the two strongest dependent variables are Sex and Pclass. From the data we can see that in general, female passengers had better chance to survive. This is perhaps due to the facts that women and children were prioritised to be evacuated to lifeboats. The second variable is the Pclass or ticket class. For the passengers in the first class, they were twice more likely to survive. On the contrary, only around 24% passengers in third clas survived.

The analysis was made by observing the charts and Pearson coefficient. Statistical tests need to be performed on the data to examine the significance of the dependent variables to the independent variable (Survived). Hence the result here is tentative.

One can use machine learning to build a model to predict the survivability of the passengers based on the various variables to predict the survivability
