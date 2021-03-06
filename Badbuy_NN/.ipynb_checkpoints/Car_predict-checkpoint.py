# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:15:43 2018

@author: Feng
"""


"""
network.py
~~~~~~~~~~
A module to implement the stochastic gradient descent learning
algorithm for a feedforward neural network. Gradients are calculated
using backpropagation. Note that I have focused on making the code
simple, easily readable, and easily modifiable. It is not optimized,
and omits many desirable features.
"""
#### Libraries
# Standard library
import random
# Third-party libraries
import numpy as np

class Network(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) \
                        for x, y in zip(sizes[:-1], sizes[1:])]
    
    
    def feedforward(self, a):
        """Return the output of the network if "a" is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent. The ``training_data`` is a list of tuples
        ``(x, y)`` representing the training inputs and the desired
        outputs. The other non-optional parameters are
        self-explanatory. If ``test_data`` is provided then the
        network will be evaluated against the test data after each
        epoch, and partial progress printed out. This is useful for
        tracking progress, but slows things down substantially."""
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
                    j, self.evaluate(test_data), n_test))
            else:
                print ("Epoch {0} complete".format(j))   
                
    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The ``mini_batch`` is a list of tuples ``(x, y)``, and ``eta``
        is the learning rate."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)                
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]               
                
    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x. ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
                                     sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book. Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on. It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)                
                
    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(int(self.feedforward(x)[0][0]>0.1), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)  


    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations-y)


#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
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
Y=car_data['IsBadBuy']

car_training=[(X.iloc[i].values.reshape(93,1),Y.iloc[i].reshape(1,1)) for i in X.index]

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
net = Network([93, 10, 1])
net.SGD(car_training, 10, 50, 3.0)
net.SGD(car_training, 30, 50, 3.0,test_data=car_test)

ProbIsBadBuy=[net.feedforward(x)[0][0] for (x,y) in car_test]

import matplotlib.pyplot as plt

plt.hist(ProbIsBadBuy,bins=30)

test_result=pd.read_csv('car_test.csv')


test_result = test_result.reindex(columns=['IsBadBuy','Size','Make','VNST','IsOnlineSale','VehicleAge','Transmission',
                             'WheelType','Auction'])


test_result['ProbIsBadBuy']=ProbIsBadBuy


test_result["ProbCat"]=pd.qcut(ProbIsBadBuy,10,precision=1)

test_result=test_result.sort_values('ProbIsBadBuy')


test_result.groupby("ProbCat").count()
test_result.groupby("ProbCat").sum()



##################################################################################
##################################################################################



#### Libraries
# Standard library
import random
# Third-party libraries
import numpy as np

class Network(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) \
                        for x, y in zip(sizes[:-1], sizes[1:])]
    
    
    def feedforward(self, a):
        """Return the output of the network if "a" is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        """Train the neural network using mini-batch stochastic
        gradient descent. The ``training_data`` is a list of tuples
        ``(x, y)`` representing the training inputs and the desired
        outputs. The other non-optional parameters are
        self-explanatory. If ``test_data`` is provided then the
        network will be evaluated against the test data after each
        epoch, and partial progress printed out. This is useful for
        tracking progress, but slows things down substantially."""
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
                    j, self.evaluate(test_data), n_test))
            else:
                print ("Epoch {0} complete".format(j))   
                
    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The ``mini_batch`` is a list of tuples ``(x, y)``, and ``eta``
        is the learning rate."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)                
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb
                       for b, nb in zip(self.biases, nabla_b)]               
                
    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x. ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of numpy arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
                                     sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book. Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on. It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)                
                
    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)  


    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives \partial C_x /
        \partial a for the output activations."""
        return (output_activations-y)


#### Miscellaneous functions
def sigmoid(z):
    """The sigmoid function."""
    return 1.0/(1.0+np.exp(-z))

def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
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
net = Network([93, 10, 2])
net.SGD(car_training, 10, 50, 1.0)
net.SGD(car_training, 20, 50, 0.5,test_data=car_test)

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

test_result=test_result.sort_values('ProbIsBadBuy')


test_result.groupby("ProbCat").count()
test_result.groupby("ProbCat").sum()




