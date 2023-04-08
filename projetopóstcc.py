# -*- coding: utf-8 -*-
"""ProjetoPósTCC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VhstTju0U7dRB9lV8jqJmK0--UMkhbJ4
"""

import pandas as pd
pd.options.display.max_columns = 500
pd.options.display.max_rows = 500

# Commented out IPython magic to ensure Python compatibility.
# data analysis and wrangling
import pandas as pd
import numpy as np
import random as rnd

# visualization
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
#machine learning
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC

df = pd.read_csv('/content/drive/MyDrive/PÓS -DADOS/ProjetoTCC/application_data.csv')
df2 = pd.read_csv('/content/drive/MyDrive/PÓS -DADOS/ProjetoTCC/columns_description.csv',encoding='cp1252')

df.head(10)

df2.head(10)

df.shape

df.size

df.info()

df.describe()

df.dtypes

df.columns

len(list(df.columns))

"""## Missing Values"""

df.isnull().sum()

testando = list(df.isnull().sum())
print(testando)

print(list(df.columns))

import seaborn as sns

sns.displot(df.isnull(), x=df.isnull().sum())

"""## Fill Null values with Mean, median and Mode

"""

#fill null values with mean,median ,mode
for i in df.columns:
    if df[i].dtypes == 'object':
        df[i].fillna(df[i].mode()[0], inplace=True)
    else:
        df[i].fillna(df[i].median(), inplace=True)

df.head()

df.isnull().sum()

df['NAME_INCOME_TYPE'].value_counts()

# Import label encoder
from sklearn import preprocessing

# label_encoder object knows how to understand word labels.
label_encoder = preprocessing.LabelEncoder()

#fill null values with mean,median ,mode
for i in df.columns:
    if df[i].dtypes == 'object':
        # Encode labels in column 'species'.
        df[i]= label_encoder.fit_transform(df[i])
    else:
        pass

df['NAME_INCOME_TYPE'].value_counts()



for col in df.columns:
    if df[col].dtypes != object:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        IQR = q3 - q1
        llp = q1-1.5*IQR
        ulp = q3+1.5*IQR
        print('column name',col)
        print('mean:',df[col].mean())
        print('mode:',df[col].mode()[0])
        print('median:',df[col].median())
        print('skewness:',df[col].skew())
        print('kurtosis:',df[col].kurtosis())
        print('null_value count:',df[col].isnull().sum())
        print('\n')

#checking outliers
#Outlier Search: This helps you to get some insights about the outliers in the data.
df.plot(kind='box', layout=(15,15),subplots=1,figsize=(25,11))
plt.show()

"""## Correlation"""

cor = df.corr()
cor

"""## Heat Map"""

#sns.set(rc={'figure.figsize':(50,50)})
#ax = sns.heatmap(df.corr(), annot=True)
#plt.show()

"""## Transform"""

df = df[['CODE_GENDER','CNT_CHILDREN','NAME_INCOME_TYPE','NAME_EDUCATION_TYPE','NAME_HOUSING_TYPE','REGION_RATING_CLIENT','REGION_RATING_CLIENT_W_CITY'
,'REG_CITY_NOT_LIVE_CITY','REG_CITY_NOT_WORK_CITY','LIVINGAREA_MEDI','TARGET','AMT_CREDIT',
'AMT_ANNUITY','AMT_GOODS_PRICE','NAME_INCOME_TYPE','HOUR_APPR_PROCESS_START','ORGANIZATION_TYPE','NAME_CONTRACT_TYPE']]

cor = df.corr()
cor

sns.set(rc={'figure.figsize':(15,15)})
ax = sns.heatmap(df.corr(), annot=True)
plt.show()



X = df.drop("TARGET",axis=1)
y = df.TARGET

X.shape



"""## Train, Test and Split"""

from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler, Normalizer
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)

#sc = StandardScaler()

#sc.fit(X_train)
#X_train = sc.transform(X_train)
#X_test = sc.transform(X_test)

X_train.shape,X_test.shape

X_train

X_test

"""

## Random forest Classifier

Random forest is a type of Supervised Machine Learning Algorithm that is commonly used in classification and regression problems. It constructs decision trees from various samples and uses their majority vote for classification and average for regression.
"""

# Applying random forest Classifier
from sklearn.ensemble import RandomForestClassifier
rf_Classifier = RandomForestClassifier(n_estimators = 10, random_state = 0)
rf_Classifier.fit(X_train, y_train)

y_pred = rf_Classifier.predict(X_test)
y_pred

from sklearn.metrics import  confusion_matrix,accuracy_score
cm=confusion_matrix(y_test,y_pred)
print(cm)
accuracy_score(y_test,y_pred)

# Classification Report
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

X_test

"""## Naive Bayes Classifier"""

from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()

y_pred = gnb.fit(X_train, y_train).predict(X_test)

print("Number of mislabeled points out of a total %d points : %d"
...       % (X_test.shape[0], (y_test != y_pred).sum()))

from sklearn.metrics import  confusion_matrix,accuracy_score,classification_report
cm=confusion_matrix(y_test,y_pred)
print(cm)
accuracy_score(y_test,y_pred)
#F1 score e cobertura (ingles)

cr = classification_report(y_test,y_pred)
print(cr)

TP = cm[0,0]
TN = cm[1,1]
FN = cm[1,0]
FP = cm[0,1]

acuracy = (TP+TN)/(TP+TN+FN+FP)
acuracy

recall = TP/(TP+FN)
recall

precision = TP/(TP+FP)
precision

f_score = 2*((precision*recall)/(precision+recall))
f_score

from sklearn.model_selection import cross_val_score, GridSearchCV

parametros = {"var_smoothing":[0.0000000001,0.00000000001,0.00000000001,0.000000000001,0.0000000000001,0.000000000000001]}
busca = GridSearchCV(estimator=GaussianNB(),param_grid=parametros,scoring = 'accuracy')
busca.fit(X,y)
best_params = busca.best_params_
print(best_params)
melhor_modelo = busca.best_estimator_
score = busca.best_score_
print(score.round(5))

#lr_pred = melhor_modelo.predict(X_test)
#

y_pred

gnb2 = GaussianNB(var_smoothing= 1e-10)

y_pred2 = gnb2.fit(X_train, y_train).predict(X_test)

from sklearn.metrics import  confusion_matrix,accuracy_score,classification_report
cm2=confusion_matrix(y_test,y_pred2)
print(cm2)
print("a Acurácia é de: ",(accuracy_score(y_test,y_pred))*100," %")
#accuracy_score(y_test,y_pred2)
#F1 score e cobertura (ingles)

cr2 = classification_report(y_test,y_pred2)
print(cr2)

TP = cm2[0,0]
TN = cm2[1,1]
FN = cm2[1,0]
FP = cm2[0,1]

acuracy2 = (TP+TN)/(TP+TN+FN+FP)
acuracy2

"""# Naive Bayes With Pre Processing StandardScaler"""

'''
Todos os códigos desse Turing Talks foram feitos em cima de um Data Set de qualidade
de vinhos. O mesmo da imagem de dados desbalanceados no início do texto.
Link: https://www.kaggle.com/uciml/red-wine-quality-cortez-et-al-2009
'''

import numpy as np
import pandas as pd
from imblearn.under_sampling import RandomUnderSampler, NearMiss, OneSidedSelection

# Random Undersampler
rus = RandomUnderSampler(random_state = 32)
X_rus_res, y_rus_res = rus.fit_resample(X, y)

# NearMiss
#nm = NearMiss(version=1)
#X_nm_res, y_nm_res = nm.fit_resample(X, y)

# OneSidedSelection (Algoritmo tipo KNN)
#oss = OneSidedSelection(random_state = 32)
#X_oss_res, y_oss_res = oss.fit_resample(X, y)

from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler, Normalizer
X_train,X_test,y_train,y_test=train_test_split(X_rus_res,y_rus_res,test_size=0.3,random_state=42)

sc = StandardScaler()

#sc.fit(X_train)
#X_train = sc.transform(X_train)
#X_test = sc.transform(X_test)

X_train.shape,X_test.shape



from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()

y_pred = gnb.fit(X_train, y_train).predict(X_test)

print("Number of mislabeled points out of a total %d points : %d"
...       % (X_test.shape[0], (y_test != y_pred).sum()))

from sklearn.metrics import  confusion_matrix,accuracy_score,classification_report
cm=confusion_matrix(y_test,y_pred)
print(cm)
print("a Acurácia é de: ",(accuracy_score(y_test,y_pred))*100," %")
#accuracy_score(y_test,y_pred)
#F1 score e cobertura (ingles)

cr = classification_report(y_test,y_pred)
print(cr)

TP = cm[0,0]
TN = cm[1,1]
FN = cm[1,0]
FP = cm[0,1]

acuracy = (TP+TN)/(TP+TN+FN+FP)
acuracy

recall = TP/(TP+FN)
recall

precision = TP/(TP+FP)
precision

f_score = 2*((precision*recall)/(precision+recall))
f_score

from sklearn.model_selection import cross_val_score, GridSearchCV

parametros = {"var_smoothing":[0.0000000001,0.00000000001,0.00000000001,0.000000000001,0.0000000000001,0.000000000000001]}
busca = GridSearchCV(estimator=GaussianNB(),param_grid=parametros,scoring = 'accuracy')
busca.fit(X_rus_res,y_rus_res)
best_params = busca.best_params_
print(best_params)
melhor_modelo = busca.best_estimator_
score = busca.best_score_
print(score.round(5))

#lr_pred = melhor_modelo.predict(X_test)
#

y_pred

gnb2 = GaussianNB(var_smoothing= 1e-10)

y_pred2 = gnb2.fit(X_train, y_train).predict(X_test)

from sklearn.metrics import  confusion_matrix,accuracy_score,classification_report
cm2=confusion_matrix(y_test,y_pred2)
print(cm2)
accuracy_score(y_test,y_pred2)
#F1 score e cobertura (ingles)

cr2 = classification_report(y_test,y_pred2)
print(cr2)

TP = cm2[0,0]
TN = cm2[1,1]
FN = cm2[1,0]
FP = cm2[0,1]

acuracy2 = (TP+TN)/(TP+TN+FN+FP)
acuracy2