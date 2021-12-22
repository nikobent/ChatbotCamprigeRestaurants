import pandas as pd
from sklearn import metrics
import sklearn.model_selection as md

"""On the file trainTestTxt we created 2 txt files, 
one for training and one for testing, so we use the same files for our results"""
train = pd.read_csv('train.txt', header = None)
test = pd.read_csv('test.txt', header = None)
train_X = train[1]
train_Y = train[0]
test_X =  test[1]
test_Y = test[0]

"""to observe different patterns of keywords"""
print(train.head(100))

liss = []
for my_var in test_X:
    if "okay" in my_var or "good" in my_var or "fine" in my_var or "kay" in my_var or "great" in my_var or "thatll do" in my_var:
        #print("dialog act: ack")
        liss.append("ack ")
    elif "is it" in my_var or "does it"  in my_var or "is there" in my_var or "is that" in my_var or "is this" in my_var:
        #print("dialog act: confirm")
        liss.append("confirm ")
    elif "repeat" in my_var or "again" in my_var or "back" in my_var:
        #print("dialog act:  repeat")
        liss.append("repeat")
    elif "more " in my_var:
        #print("dialog act: reqmore")
        liss.append("reqmore ")
    elif "start" in my_var or "reset" in my_var:
        #print("dialog act: restart")
        liss.append("restart ")
    elif "thank you" in my_var or "thanks" in my_var:
        #print("dialog act: thankyou")
        liss.append("thankyou ")
    elif "yes" in my_var or "right" in my_var or "yea" in my_var or "uh huh" in my_var or "ye" in my_var:
        #print("dialog act: affirm")
        liss.append("affirm ")
    elif "goodbye" in my_var or "bye" in my_var:
        #print("dialog act: bye")
        liss.append("bye ")
    elif "not" in my_var or "dont want" in my_var or "wrong" in my_var or "change" in my_var:
        #print("dialog act: deny")
        liss.append("deny ")
    elif "hello" in my_var or "hi" in my_var or "halo" in my_var:
        #print("dialog act: hello")
        liss.append("hello ")
    elif "how about" in my_var or "else" in my_var or "anything" in my_var:
        #print("dialog act: reqalts")
        liss.append("reqalts ")
    elif "looking" in my_var or "food" in my_var or "i dont care" in my_var or "south" in my_var or "west" in my_var or "north" in my_var or "east" in my_var or "spanish" in my_var or "french" in my_var or "chinese" in my_var or "asian" in my_var:
        #print("dialog act: inform")
        liss.append("inform ")
    elif "expansive" in my_var or "moderate" in my_var or "cheap" in my_var or "any area" in my_var or "center" in my_var or "doesnt matter" in my_var or "any kind" in my_var or "traditional" in my_var or "barbecue" in my_var:
        #print("dialog act: inform")
        liss.append("inform ")
    elif "no" in my_var:
        #print("dialog act: negate")
        liss.append("negate ")
    elif "what" in my_var or "whats" in my_var or "may" in my_var or "can you" in my_var or "address" in my_var or "post code" in my_var or "phone number" in my_var or "price range" in my_var:
        #print("dialog act: request4")
        liss.append("request4 ")
    else:
        #print("dialog act: null")
        liss.append("null ")

test.insert(2,"our_ack",liss)
print(test.head())
print(metrics.classification_report(test_Y,liss))


while True:
    my_var = input('Give me a sentence! || Type: "EXIT" to exit (case-sensitive) .\nSentence: ')
    liss =[]
    if my_var == 'EXIT':
        break
    if "okay" in my_var or "good" in my_var or "fine" in my_var or "kay" in my_var or "great" in my_var or "thatll do" in my_var:
        #print("dialog act: ack")
        liss.append("ack ")
    elif "is it" in my_var or "does it"  in my_var or "is there" in my_var or "is that" in my_var or "is this" in my_var:
        #print("dialog act: confirm")
        liss.append("confirm ")
    elif "repeat" in my_var or "again" in my_var or "back" in my_var:
        #print("dialog act: repeat")
        liss.append("repeat ")
    elif "more" in my_var:
        #print("dialog act: reqmore")
        liss.append("reqmore ")
    elif "start" in my_var or "reset" in my_var:
        #print("dialog act: restart")
        liss.append("restart ")
    elif "thank you" in my_var or "thanks" in my_var:
        #print("dialog act: thankyou")
        liss.append("thankyou ")
    elif "yes" in my_var or "right" in my_var or "yea" in my_var or "uh huh" in my_var or "y " in my_var:
        #print("dialog act: affirm")
        liss.append("affirm ")
    elif "goodbye" in my_var or "bye" in my_var:
        #print("dialog act: bye")
        liss.append("bye ")
    elif "not" in my_var or "dont want" in my_var or "wrong" in my_var or "change" in my_var:
        #print("dialog act: deny")
        liss.append("deny ")
    elif "hello" in my_var or "hi" in my_var or "halo" in my_var:
        #print("dialog act: hello")
        liss.append("hello ")
    elif "how about" in my_var or "else" in my_var or "anything" in my_var:
        #print("dialog act: reqalts")
        liss.append("reqalts ")
    elif "looking" in my_var or "food" in my_var or "i dont care" in my_var or "south" in my_var or "west" in my_var or "north" in my_var or "east" in my_var or "spanish" in my_var or "french" in my_var or "chinese" in my_var or "asian" in my_var:
        #print("dialog act: inform")
        liss.append("inform ")
    elif "expansive " in my_var or "moderate" in my_var or "cheap" in my_var or "any area" in my_var or "center" in my_var or "doesnt matter" in my_var or "any kind" in my_var or "traditional" in my_var or "barbecue" in my_var:
        #print("dialog act: inform")
        liss.append("inform ")
    elif "no " in my_var:
        #print("dialog act: negate")
        liss.append("negate")
    elif "what" in my_var or "whats" in my_var or "may" in my_var or "can you" in my_var or "adress" in my_var or "post code" in my_var or "phone number" in my_var or "price range" in my_var:
        #print("dialog act: request4")
        liss.append("request4 ")
    else:
        #print("dialog act: null")
        liss.append("null ")

    print("predicted dialog act: " + liss[0])
