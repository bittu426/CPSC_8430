# -*- coding: utf-8 -*-
"""chaitanya_1(b)_trainonactualtask.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IaUqGvWz5IqCtP0DQzgHevcprbOcTY8v
"""

pip install tensorflow==2.4

# This program trains three feedforward DNNs on the MNIST dataset
# Graphs are produces showing loss and accuracy of all model for training and test sets

import tensorflow as tf
import numpy as np
import torch
import torchvision as tv
from torchvision import transforms, datasets
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# Grab MNIST dataset
trainingSet = datasets.MNIST('', train=True, download=True, transform=transforms.Compose([transforms.ToTensor()]))
testingSet = datasets.MNIST('', train=False, download=False, transform=transforms.Compose([transforms.ToTensor()]))
train = torch.utils.data.DataLoader(trainingSet, batch_size=100, shuffle=True)
test = torch.utils.data.DataLoader(testingSet, batch_size=100, shuffle=True)

# Calculate the number of parameters in a neural network
def calcParams(inputModel):
    val = sum(params.numel() for params in inputModel.parameters() if params.requires_grad)
    return val

# Set up NN for MNIST training
# Shallow NN for training - 1 Hidden layer / 24655 Parameters
class ShallowTrainNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 31)
        self.fc2 = nn.Linear(31, 10)

    def forward(self, val):
        val = F.relu(self.fc1(val))
        val = self.fc2(val)
        return val

# Middle NN for training - 4 Hidden layer / 24635 Parameters
class MiddleTrainNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 27)
        self.fc2 = nn.Linear(27, 41)
        self.fc3 = nn.Linear(41, 38)
        self.fc4 = nn.Linear(38, 14)
        self.fc5 = nn.Linear(14, 10)

    def forward(self, val):
        val = F.relu(self.fc1(val))
        val = F.relu(self.fc2(val))
        val = F.relu(self.fc3(val))
        val = F.relu(self.fc4(val))
        val = self.fc5(val)
        return val
    
# Deep NN for simulation -  6 Hidden Layers / 24647 Parameters
class DeepTrainNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 20)
        self.fc2 = nn.Linear(20, 40)
        self.fc3 = nn.Linear(40, 58)
        self.fc4 = nn.Linear(58, 50)        
        self.fc5 = nn.Linear(50, 34)
        self.fc6 = nn.Linear(34, 23)
        self.fc7 = nn.Linear(23, 10)        
        
    def forward(self, val):
        val = F.relu(self.fc1(val))
        val = F.relu(self.fc2(val))
        val = F.relu(self.fc3(val))
        val = F.relu(self.fc4(val))
        val = F.relu(self.fc5(val))
        val = F.relu(self.fc6(val))
        val = self.fc7(val)
        return val

model1 = ShallowTrainNN()
print(calcParams(model1))
model2=MiddleTrainNN()
print(calcParams(model2))
model3=DeepTrainNN()
print(calcParams(model3))

# Set up necessary auxilaries for neural net training
shallownn = ShallowTrainNN()
middlenn = MiddleTrainNN()
deepnn = DeepTrainNN()
costFunc = nn.CrossEntropyLoss()
shallowOpt = optim.Adam(shallownn.parameters(), lr=0.001)
middleOpt = optim.Adam(middlenn.parameters(), lr=0.001)
deepOpt = optim.Adam(deepnn.parameters(), lr=0.001)

# Train shalllow neural networks, Calculate accuracy for training and testing in each epoch
EPOCHS = 200
counter = 0
counterList = []
shallowCostList = []
shallowTestAccuracyList = []
shallowTrainAccuracyList = []
for index in range(EPOCHS):
    counterList.append(counter)
    counter += 1
    # Train model and keep track of loss
    for batch in train:
        inputImages, groundTruth = batch
        shallownn.zero_grad()
        output = shallownn(inputImages.view(-1,784))
        cost = costFunc(output, groundTruth)
        cost.backward()
        shallowOpt.step()
    shallowCostList.append(cost)
    
    # Calculate accuracy of shallow model on training data
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in train:
            inputImages, groundTruth = batch
            output = shallownn(inputImages.view(-1,784))
            for i, outputTensor in enumerate(output):
                if torch.argmax(outputTensor) == groundTruth[i]:
                    correct += 1
                total += 1
    shallowTrainAccuracyList.append(round(correct/total, 3))

    # Calculate accuracy of shallow model on test data
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in test:
            inputImages, groundTruth = batch
            output = shallownn(inputImages.view(-1,784))
            for i, outputTensor in enumerate(output):
                if torch.argmax(outputTensor) == groundTruth[i]:
                    correct += 1
                total += 1
    shallowTestAccuracyList.append(round(correct/total, 3))

# Train middle neural networks, Calculate accuracy for training and testing in each epoch
middleCostList = []
middleTrainAccuracyList = []
middleTestAccuracyList = []
for index in range(EPOCHS):
    # Train model and keep track of loss
    for batch in train:
        inputImages, groundTruth = batch
        middlenn.zero_grad()
        output = middlenn(inputImages.view(-1,784))
        cost = costFunc(output, groundTruth)
        cost.backward()
        middleOpt.step()
    middleCostList.append(cost)
    
    # Calculate accuracy of middle nn on training data
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in train:
            inputImages, groundTruth = batch
            output = middlenn(inputImages.view(-1,784))
            for i, outputTensor in enumerate(output):
                if torch.argmax(outputTensor) == groundTruth[i]:
                    correct += 1
                total += 1
    middleTrainAccuracyList.append(round(correct/total, 3))

    # Calculate accuracy of middle nn on test data
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in test:
            inputImages, groundTruth = batch
            output = middlenn(inputImages.view(-1,784))
            for i, outputTensor in enumerate(output):
                if torch.argmax(outputTensor) == groundTruth[i]:
                    correct += 1
                total += 1
    middleTestAccuracyList.append(round(correct/total, 3))

# Train Deep neural networks, Calculate accuracy for training and testing in each epoch
deepCostList = []
deepTrainAccuracyList = []
deepTestAccuracyList = []
for index in range(EPOCHS):
    # Train model and keep track of loss
    for batch in train:
        inputImages, groundTruth = batch
        deepnn.zero_grad()
        output = deepnn(inputImages.view(-1,784))
        cost = costFunc(output, groundTruth)
        cost.backward()
        deepOpt.step()
    deepCostList.append(cost)
    
    # Calculate accuracy of deep nn on training data
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in train:
            inputImages, groundTruth = batch
            output = deepnn(inputImages.view(-1,784))
            for i, outputTensor in enumerate(output):
                if torch.argmax(outputTensor) == groundTruth[i]:
                    correct += 1
                total += 1
    deepTrainAccuracyList.append(round(correct/total, 3))

    # Calculate accuracy of deep nn on test data
    correct = 0
    total = 0
    with torch.no_grad():
        for batch in test:
            inputImages, groundTruth = batch
            output = deepnn(inputImages.view(-1,784))
            for i, outputTensor in enumerate(output):
                if torch.argmax(outputTensor) == groundTruth[i]:
                    correct += 1
                total += 1
    deepTestAccuracyList.append(round(correct/total, 3))

# Visulaize Training process of nn for MNIST dataset
plt.plot(counterList, shallowCostList, 'c', label='Shallow-1 hidden layer')
plt.plot(counterList, middleCostList, 'y', label='Middle-4 hidden layers')
plt.plot(counterList, deepCostList, 'r', label='Deep-6 hidden layers')
plt.title("Learning Progression for MNIST")
plt.xlabel("EPOCHS")
plt.ylabel("Cross Entropy Loss")
plt.legend(loc="upper right")
plt.show()

# Visulaize Accuracy of nn for for MNIST dataset
plt.plot(counterList, shallowTrainAccuracyList, 'c--', label='Shallow Train')
plt.plot(counterList, shallowTestAccuracyList, 'c', label='Shallow Test')
plt.plot(counterList, middleTrainAccuracyList, 'y--', label='Middle Train')
plt.plot(counterList, middleTestAccuracyList, 'y', label='Middle Test')
plt.plot(counterList, deepTrainAccuracyList, 'r--', label='Deep Train')
plt.plot(counterList, deepTestAccuracyList, 'r', label='Deep Test')
plt.title("Accuracy of NNs")
plt.xlabel("EPOCHS")
plt.ylabel("Accuracy")
plt.legend(loc="lower right")
plt.show()