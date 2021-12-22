import pandas as pd
import sklearn.model_selection as md


"""here we are gonna seperate train and test set, 
so we use the same for every case(baselines, machinelearning)"""
data = pd.read_csv('act.txt', header = None)
df = data.sample(frac=1).reset_index(drop=True)
train, test = md.train_test_split(df, train_size = 0.85)
train.to_csv(r'train.txt', header=None, index=None, sep=',', mode='a')
test.to_csv(r'test.txt', header=None, index=None, sep=',', mode='a')