import pandas as pd
from sklearn import metrics
import sklearn.model_selection as md
import operator
import collections
from random import randint

"""On the file trainTestTxt we created 2 txt files, 
one for training and one for testing, so we use the same files for our results"""
train = pd.read_csv('train.txt', header = None)
test = pd.read_csv('test.txt', header = None)
train_X = train[1]
train_Y = train[0]
test_X =  test[1]
test_Y = test[0]

"""calculati number of apperiences 
and the total sum of acts in the training set
"""
act_freq = {}
sum = 0
for act in train_Y:
    if act not in act_freq:
        act_freq[act] = 0
    act_freq[act] +=1
    sum +=1

"""/sum for frequency, sorting and 
then adding the previous frequencies to the next one
"""
for act in act_freq:
    act_freq[act] = act_freq[act]/sum

sorted_act = sorted(act_freq.items(), key=operator.itemgetter(1))
sorted_dict = collections.OrderedDict(sorted_act)


for act in sorted_dict:
    print(act)
    print(sorted_dict[act])

sum1 = 0
for act in sorted_dict:
    sorted_dict[act] = sorted_dict[act] + sum1
    sum1 = sorted_dict[act]
    #print(act)
    #print(sorted_dict[act])

print("\n")
for act in sorted_dict:
    print(sorted_dict[act])

predicted_Y = []
for ut in test_X:
    k = randint(100,100000000)/100000000
    #print(k)
    for act in sorted_dict:
        if sorted_dict[act]>=k:
            predicted_Y.append(act)
            #print(act)
            break

print(metrics.classification_report(test_Y,predicted_Y))

while True:
    phrase = input('Give me a sentence! || Type: "EXIT" to exit (case-sensitive) .\nSentence: ')
    if phrase == 'EXIT':
        break
    k = randint(100,100000000)/100000000
    #print(k)
    for act in sorted_dict:
        if sorted_dict[act]>=k:
            action = act
            #print(act)
            break
    print("predicted dialog act: " + action)

