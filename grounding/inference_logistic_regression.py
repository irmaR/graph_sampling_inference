from sklearn.linear_model import LogisticRegression
import pandas as pd
import pylab as pl
from sklearn.metrics import roc_auc_score
import os

def train_logistic_regression(train_data_csv):
    dataset = pd.read_csv(train_data_csv)
    X = dataset[dataset.columns[2:]]
    y=dataset['target']
    logistic = LogisticRegression()
    logistic.fit(X, y)
    train_roc = roc_auc_score(y, logistic.predict_proba(X)[:, 1])
    print "Train roc: ",train_roc
    return logistic


def predict_logistic_regression(test_data,model,output_file):
    dataset = pd.read_csv(test_data)
    X = dataset[dataset.columns[2:]]
    y = dataset['target']
    prediction=model.predict_proba(X)
    print model.classes_
    print model.coef_
    #counter=2
    #for p in prediction:
    #    print counter, p
    #    counter+=1

    roc = roc_auc_score(y, model.predict_proba(X)[:, 1])
    accuracy_score = model.score(X, y)
    print "ROC: ",roc
    with open(os.path.join(output_file,'roc.res'),'w') as f:
        f.write(str(roc))

if __name__ == '__main__':
    #train_logistic_regression('/home/irma/work/DATA/DATA/yeast/exact_train.csv')
    train_data='/home/irma/work/DATA/DATA/WEBKB/experiments_inference/page_class/RESULTS/exact/train.csv'
    test_data='/home/irma/work/DATA/DATA/WEBKB/experiments_inference/page_class/RESULTS/furer/test.csv'
    output='/home/irma/work/DATA/DATA/WEBKB/experiments_inference/page_class/RESULTS/exact/'
    model=train_logistic_regression(train_data)
    predict_logistic_regression(test_data, model,output)
