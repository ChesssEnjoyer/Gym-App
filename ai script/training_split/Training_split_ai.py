import random
import csv
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib 

#define ai model
model = SVC()

#open csv file in order to train
with open('script/training_split.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    data = [row for row in reader]

#prepare data for training and testing
random.shuffle(data)
holdout = int(0.5 * len(data))
data_train = data[:holdout]
data_test = data[holdout:]

#assign individual data to training and testing sets
X_training = [[float(j[0]), float(j[2])] for j in data_train]
y_training = [j[3] for j in data_train]
X_testing = [[float(j[0]), float(j[2])] for j in data_test]
y_testing = [j[3] for j in data_test]

#encode y sets
label_encoder = LabelEncoder()
y_training_encoded = label_encoder.fit_transform(y_training)
y_testing_encoded = label_encoder.transform(y_testing)

#fit sets into model and make predictions
model.fit(X_training, y_training_encoded)
predictions = model.predict(X_testing)

#count correct and incoreect predictions 
total = 0
correct = 0
incorrect = 0
for actual, predicted in zip(y_testing_encoded, predictions):
    print(actual, predicted)
    total += 1
    if actual == predicted:
        correct += 1
    else: incorrect += 1

# save model with joblib 
filename = 'joblib_model.sav'
joblib.dump(model, filename)

#print results
print(f"Results for model {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Accuracy: {100 * correct/total:.2f}%")