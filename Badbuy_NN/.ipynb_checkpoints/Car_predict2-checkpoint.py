# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:15:43 2018

Build Neural network from perceptron，treating biases as part of weights and use 
matrix computation to optimize the stochastic gradient descent method.


@author: Feng
"""

#### Libraries
from datetime import datetime
import random
import numpy as np

class NeuralNetwork(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.weights = [np.random.randn(y, x+1) \
                        for x, y in zip((sizes[:-1]), sizes[1:])] # biases are included in weights
    
    
    def feedforward(self, a):
        for w in self.weights:
            a = np.concatenate((a,np.array([1]).reshape(1,1))) # add bias neuron 
            a = sigmoid(np.dot(w, a))
        return a


    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        if test_data: n_test = len(test_data)
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k+mini_batch_size] \
                            for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print ("Epoch {0}: {1} / {2}".format( \
                    j, self.evaluate_0(test_data), n_test))
            else:
                print ("Epoch {0} complete".format(j))   

                
    def update_mini_batch(self, mini_batch, eta):
        X = np.array([x[0] for x in mini_batch])
        Y = np.array([x[1] for x in mini_batch])
        nabla_w= self.backprop(X,Y)
        self.weights = [w-eta*nw
                        for w, nw in zip(self.weights, nabla_w)]
                

    def backprop(self, x, y):
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [activation] 
        zs = [] 
        for w in self.weights:
            activation = np.concatenate((activation,
                                         np.ones((activation.shape[0],1,1))),axis=1)
            activations[-1]=activation
            z = np.matmul(w, activation)
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
                                     sigmoid_prime(zs[-1])
        nabla_w[-1] = np.matmul(delta, activations[-2].transpose(0,2,1)).mean(axis=0)

        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.matmul(self.weights[-l+1].transpose(), delta)[:,:-1,:]
            delta = delta * sp
            nabla_w[-l] = np.matmul(delta, 
                   activations[-l-1].transpose(0,2,1)).mean(axis=0)
        return nabla_w                
                
    def evaluate_0(self, test_data):
        test_results = [(int(self.feedforward(x)[1][0]>0.1), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results) 
                
    def evaluate(self, test_data):
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)  


    def cost_derivative(self, output_activations, y):
        return (output_activations-y)


#### Miscellaneous functions
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))



####  prepare training data ,Validation data,  test data
import pandas as pd

car_data=pd.read_csv('car.csv')


car_data = car_data.reindex(columns=['IsBadBuy','Size','Make','VNST','IsOnlineSale','VehicleAge','Transmission',
                             'WheelType','Auction'])


shuffler= np.random.permutation(len(car_data))

car_shuffle = car_data.take(shuffler) # pandas' shuffling method in comparison of random.shuffle

# X preparation

Size = pd.get_dummies(car_data['Size'],prefix='Size')  # generate dummy varibles from categorical varible
Make = pd.get_dummies(car_data['Make'],prefix='Make')
VNST = pd.get_dummies(car_data['VNST'],prefix='VNST')
VehicleAge = pd.get_dummies(car_data['VehicleAge'],prefix='VehicleAge')
WheelType = pd.get_dummies(car_data['WheelType'],prefix='WheelType')
Auction = pd.get_dummies(car_data['Auction'],prefix='Auction')
IsOnlineSale =(car_data.IsOnlineSale=='Yes').apply(float)

X= Size.join(Make).join(VNST).join(IsOnlineSale).join(VehicleAge).join(WheelType).join(Auction)
Y=pd.get_dummies(car_data['IsBadBuy'],prefix='IsBadbuy')

car_training=[(X.iloc[i].values.reshape(93,1),Y.iloc[i].values.reshape(2,1)) for i in X.index]

#test data preparing, as did with training data

car_test=pd.read_csv('car_test.csv')


car_test = car_test.reindex(columns=['IsBadBuy','Size','Make','VNST','IsOnlineSale','VehicleAge','Transmission',
                             'WheelType','Auction'])

Size = pd.get_dummies(car_test['Size'],prefix='Size')  # generate dummy varibles from categorical varible
Make = pd.get_dummies(car_test['Make'],prefix='Make')
VNST = pd.get_dummies(car_test['VNST'],prefix='VNST')
VehicleAge = pd.get_dummies(car_test['VehicleAge'],prefix='VehicleAge')
WheelType = pd.get_dummies(car_test['WheelType'],prefix='WheelType')
Auction = pd.get_dummies(car_test['Auction'],prefix='Auction')
IsOnlineSale =(car_test.IsOnlineSale=='Yes').apply(float)

X= Size.join(Make).join(VNST).join(IsOnlineSale).join(VehicleAge).join(WheelType).join(Auction)
Y=car_test['IsBadBuy']

car_test=[(X.iloc[i].values.reshape(93,1),Y.iloc[i]) for i in X.index]


# set of net for Car training
net = NeuralNetwork([93, 186, 2])

start=datetime.now()
net.SGD(car_training, 30, 30, 1.0,test_data=car_test)
#net.SGD(training_data, 10, 50, 3.0, test_data=test_data)
end=datetime.now()
print("Runing time: %s seconds"%(end-start))

net.SGD(car_training, 30, 50, 1.0,test_data=car_test)

ProbIsGoodBuy=[net.feedforward(x)[0][0] for (x,y) in car_test]
ProbIsBadBuy=[net.feedforward(x)[1][0] for (x,y) in car_test]

import matplotlib.pyplot as plt

plt.hist(ProbIsBadBuy,bins=30,color='red',alpha=0.3)
plt.hist(ProbIsGoodBuy,bins=30,color='blue',alpha=0.5)

test_result=pd.read_csv('car_test.csv')


test_result = test_result.reindex(columns=['IsBadBuy','Size','Make','VNST','IsOnlineSale','VehicleAge','Transmission',
                             'WheelType','Auction'])


test_result['ProbIsBadBuy']=ProbIsBadBuy


test_result["ProbCat"]=pd.qcut(ProbIsBadBuy,10,precision=1)

#test_result=test_result.sort_values('ProbIsBadBuy')


test_result.groupby("ProbCat").count()
test_result.groupby("ProbCat").sum()




