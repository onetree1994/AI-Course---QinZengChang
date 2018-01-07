import csv
import numpy as np

def load_train_data(s):
    X=[];
    y=[];
    with open(s,'r') as csvfile:
        data_train=csv.reader(csvfile)
        for row in data_train:
            temp=np.array(np.zeros(10),dtype=np.float32)
            temp[int(row[0])]=1.0
            y.append(temp)
            temp=np.array(np.zeros(784),dtype=np.float32)
            for rank in range(1,785):
                temp[rank-1]=(float(row[rank]))
            X.append(temp)
    return [X,y]

def load_test_data(s):
    X=np.mat(np.zeros((28000,784)))
    with open(s,'r') as csvfile:
        data_test=csv.reader(csvfile)
        count=0
        for row in data_test:
            k=0
            for data in row:
                X[count,k]=float(data)
                k=k+1
            count=count+1
    return X

def output_result(result,s):
    with open(s,'w',newline='') as csvfile:
        pen=csv.writer(csvfile)
        pen.writerow(['ImageId','Label'])
        count=1
        for element in result:
            pen.writerow([count,int(element)])
            count=count+1
            