# Shows all available models
#from pycaret.classification import *
#help(create_model)

#import libraries time and pandas 
import time
import pandas as pd
#import pycaret classification models 
from pycaret.classification import *
#import json to save results 
import json
#import numpy 
import numpy as np 

#start time calculation 
start = time.time()

#define paths for test and train data 
testing_data = pd.read_csv("D:\\Courses USU\\Spring 2026\\Adv Python for Analytics DATA6500\\final project\\UNSW_NB15_testing-set1.csv")
training_data = pd.read_csv("D:\\Courses USU\\Spring 2026\\Adv Python for Analytics DATA6500\\final project\\UNSW_NB15_training-set1.csv")

#clean data to remove unnecessary columns of id and attack category 
testing_data = testing_data.drop(columns=['attack_cat','id', ])
training_data = training_data.drop(columns=['attack_cat','id'])

#initialize the classification to train data on column "label"
# value 0 is for normal traffic and value 1 is for cyber attack traffic 
clf = setup(data=training_data, target= 'label')

#create test object for random forest 
#rf_model=create_model('rf')

#list of models to iterate through for calculations 
models = ['lr', 'ridge', 'lda','rf','nb', 'gbc','ada','et','qda','knn','dt','svm','mlp'] 

#gpc & rbfsvm are excluded due to high processing time

#test model list 
#models = ['lr']

#results dictionary to store results 
results = {}

#run to compare models
#print("comparing model ...")
#comp_model = compare_models(exclude = ['catboost', 'xgboost', 'gpc', 'rbfsvm', 'lightgbm','nb','qda','knn','mlp'])
#comparison_results = pull()
#print()
#results['compare_models']= comparison_results.to_dict(orient='records')
#print()

#iterate through all models in the list 
for model in models: 
    print ("calculating"," ",model,"....") # printout the model being calculated 
    m = create_model(model) # create the models 
    predictions = predict_model(m, data=testing_data) # predict the models for accuracy 
    
    #plots     
    #plot_model(m, plot='confusion_matrix') #plot confusion matrix 
    #plot_model(m, plot='auc') #plot area under curve
    #plot_model(m, plot='feature') #plot feature 

    
    #take out model summary to store in json 
    model_summary= pull()
    results[model] = model_summary.to_dict(orient='records') #store results in dictionary 


# add keras neural network analysis
print("calculating keras ...")

from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, recall_score, precision_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# keras data is taken from Pycaret setup 
# X is the features i.e. all columns except 'label'
#y is the target i.e. Normal = 0 and Attack = 1 

X_train_transformed = get_config('X_train_transformed') #training set for features  
X_test_transformed = get_config('X_test_transformed') #test set for features 
y_train = get_config('y_train_transformed') #training set for target 
y_test = get_config('y_test_transformed') #testing set for target 


# build  keras model for 64 -> 32 -> 1 nodes for neural network 
keras_model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train_transformed.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

# use parameters to train model 
keras_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# fit function to adjust model over training data 
keras_history = keras_model.fit(X_train_transformed, y_train, epochs=5, batch_size=32, verbose=1) # X as input, y as output, process 32 rows at a time, run 5 iterations and print process after each iteration

# predicting on data 
y_predict_probability = keras_model.predict(X_test_transformed) # make prediction probabilities 
y_predict = (y_predict_probability > 0.5).astype(int) # convert to 0 or 1 on prediction probability 

# get keras results metrics
keras_results = {
    'Model': 'Keras Neural Network',
    'Accuracy': round(accuracy_score(y_test, y_predict), 4),
    'AUC':      round(roc_auc_score(y_test, y_predict_probability), 4),
    'Recall':   round(recall_score(y_test, y_predict), 4),
    'Prec.':    round(precision_score(y_test, y_predict), 4),
    'F1':       round(f1_score(y_test, y_predict), 4)
}
#print keras results 
print("Keras Results:", keras_results)

# create keras confusion Matrix
keras_cm = confusion_matrix(y_test, y_predict)
display_cm = ConfusionMatrixDisplay(confusion_matrix=keras_cm, display_labels=['Normal', 'Attack']) #create a display object for confusion matrix 
display_cm.plot(cmap='Blues') #draw chart in blue 
plt.title('Keras Neural Network - Confusion Matrix') #chart title 
#plt.show() # show chart 

# keras feature 
# Get feature names
feature_names = X_train_transformed.columns.tolist() #store column names in a list 

# Calculate feature importance 
print("calculating keras feature importance ....")

baseline_accuracy = accuracy_score(y_test, y_predict) # get accuracy score 
importance_scores = [] #create empty list to store scores 

#loop all columns to test feature importance 
for i in range(X_test_transformed.shape[1]):
    X_temp = X_test_transformed.values.copy() #convert pandas dataframe to numpy array 
    np.random.shuffle(X_temp[:, i])  # shuffle one feature
    y_temp_probability = keras_model.predict(X_temp, verbose=0) # get prediction probabilities 
    y_temp_prediction = (y_temp_probability > 0.5).astype(int) # convert to 0 or 1 
    accuracy = accuracy_score(y_test, y_temp_prediction) #measure accuracy 
    importance_scores.append(baseline_accuracy - accuracy)  # calc drop in accuracy score 

# convert scores to array
importance_scores = np.array(importance_scores)

# plot top 15 features for keras 
top_idx = importance_scores.argsort()[-15:] # take highest 15 importance score feature scores 
plt.figure(figsize=(10, 6)) 
plt.barh(
    [feature_names[i] for i in top_idx], #get feature names 
    importance_scores[top_idx] # get scores at these features
)

plt.title('Keras Neural Network - Top 15 Feature Importance') #plot title label
plt.xlabel('Drop in Accuracy when Feature is Shuffled') # plot x axis label
plt.tight_layout() #correct layout 
plt.show() # show plot 

# save top keras features to results
top_features = [
    {'feature': feature_names[i], 'importance': round(importance_scores[i], 4)}
    for i in importance_scores.argsort()[::-1][:15]
]

# save results to json 
results['keras'] = [keras_results]
results['keras_features'] = top_features


print("saving results to json ...")
#save results to json file 
with open ("D:\\Courses USU\\Spring 2026\\Adv Python for Analytics DATA6500\\final project\\results.json",'w') as f:
    json.dump(results,f,indent=4)

#calculate end time 
end = time.time()

#tell when done 
print("all done ..."," in time", int(end - start),"seconds")



