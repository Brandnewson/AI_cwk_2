# COMP2611-Artificial Intelligence-Coursework#2 - Descision Trees

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.tree import export_text
import warnings
import os

# STUDENT NAME: Liang Quan Branson Tay 
# STUDENT EMAIL: sc22blqt@leeds.ac.uk
    
def print_tree_structure(model, header_list):
    tree_rules = export_text(model, feature_names=header_list[:-1])
    print(tree_rules)
    
# Task 1 [10 marks]: Load the data from the CSV file and give back the number of rows
def load_data(file_path, delimiter=','):
    num_rows, data, header_list=None, None, None
    if not os.path.isfile(file_path):
        warnings.warn(f"Task 1: Warning - CSV file '{file_path}' does not exist.")
        return None, None, None
    # load CSV file into a Pandas Dataframe
    df = pd.read_csv(file_path)
    num_rows = len(df)
    header_list = df.columns.tolist()
    data = df.to_numpy()

    return num_rows, data, header_list

# Task 2[10 marks]: Give back the data by removing the rows with -99 values 
def filter_data(data):
    filtered_data=[None]*1
    
    # Remove rows with -99 values
    filtered_data = data[~np.any(data == -99, axis=1)]

    return filtered_data

# Task 3 [10 marks]: Data statistics, return the coefficient of variation for each feature, make sure to remove the rows with nan before doing this. 
# coefficient of variation measures the relative variability or dispersion of a dataset
# feature = col
def statistics_data(data):
    coefficient_of_variation=None
    data=filter_data(data)
    # Remove rows with NaN values
    data = data[~np.isnan(data).any(axis=1)]
    # Calculate mean and standard deviation for each feature
    means = np.mean(data, axis=0)
    std_devs = np.std(data, axis=0)
    # Calculate coefficient of variation for each feature
    coefficient_of_variation = (std_devs / means)
    
    return coefficient_of_variation

# Task 4 [10 marks]: Split the dataset into training (70%) and testing sets (30%), 
# use train_test_split of scikit-learn to make sure that the sampling is stratified, 
# meaning that the ratio between 0 and 1 in the lable column stays the same in train and test groups.
# Also when using train_test_split function from scikit-learn make sure to use "random_state=1" as an argument. 
def split_data(data, test_size=0.3, random_state=1):
    x_train, x_test, y_train, y_test=None, None, None, None
    np.random.seed(1)
    # Assuming the target variable is in the last column
    x = data[:, :-1]  # Features, i.e. likelihood of fraudulent transaction
    y = data[:, -1]   # Target variable, i.e. prediction of fraudulent transaction

    # Split the dataset into training and testing sets, stratified by the target variable
    # Stratification refers to the process of dividing a dataset into subsets (such as training and testing sets) in such a way that the proportion of classes is approximately the same in each subset as it is in the original dataset.
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, stratify=y, random_state=random_state)
    
    return x_train, x_test, y_train, y_test

# Task 5 [10 marks]: Train a decision tree model with cost complexity parameter of 0
def train_decision_tree(x_train, y_train,ccp_alpha=0):
    model=None
    # Initialize the DecisionTreeClassifier with the specified cost complexity parameter
    dt_classifier = DecisionTreeClassifier(ccp_alpha=ccp_alpha)
    # Train the decision tree model using the training data
    model = dt_classifier.fit(x_train, y_train)

    return model

# Task 6 [10 marks]: Make predictions on the testing set 
def make_predictions(model, X_test):
    y_test_predicted=None
    # Make predictions using the trained decision tree model
    y_test_predicted = model.predict(X_test)
    
    return y_test_predicted

# Task 7 [10 marks]: Evaluate the model performance by taking test dataset and giving back the accuracy and recall 
def evaluate_model(model, x, y):
    accuracy, recall=None,None
    # Make predictions using the trained model
    y_pred = model.predict(x_test)
    
    # Calculate accuracy and recall
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    return accuracy, recall

# Task 8 [10 marks]: Write a function that gives the optimal value for cost complexity parameter
# which leads to simpler model but almost same test accuracy as the unpruned model (+-1% of the unpruned accuracy)
def optimal_ccp_alpha(x_train, y_train, x_test, y_test):
    optimal_ccp_alpha=None

    # Initialize the DecisionTreeClassifier with ccp_alpha=0, trains it on the training data.
    dt_classifier = DecisionTreeClassifier(ccp_alpha=0)
    dt_classifier.fit(x_train, y_train)

    # Calculate the accuracy of the unpruned model
    unpruned_accuracy = accuracy_score(y_test, dt_classifier.predict(x_test))

    # Gradually increase ccp_alpha gradually until accuracy drops more than 1%
    ccp_alpha = 0.001  # Start with a small increment
    while True:
        ccp_alpha += 0.001  # Increase ccp_alpha gradually
        dt_classifier = DecisionTreeClassifier(ccp_alpha=ccp_alpha)
        dt_classifier.fit(x_train, y_train)
        test_accuracy = accuracy_score(y_test, dt_classifier.predict(x_test))

        # Stops if accuracy dropped more than 1% from the unpruned model
        if test_accuracy < unpruned_accuracy - 0.01:
            break
        
        # Update optimal_alpha and max_accuracy
        optimal_ccp_alpha = ccp_alpha
        # max_accuracy = test_accuracy

    return optimal_ccp_alpha

# Task 9 [10 marks]: Write a function that gives the depth of a decision tree that it takes as input.
def tree_depths(model):
    depth=None
    # Get the depth of the unpruned tree
    depth = model.tree_.max_depth

    return depth

 # Task 10 [10 marks]: Feature importance 
def important_feature(x_train, y_train,header_list):
    best_feature=None
    # Train decision tree model and increase Cost Complexity Parameter until the depth reaches 1
    # Initialize the DecisionTreeClassifier with ccp_alpha=0
    dt_classifier = DecisionTreeClassifier(ccp_alpha=0)
    dt_classifier.fit(x_train, y_train)

    # Increase ccp_alpha gradually until the depth of the tree reaches 1
    ccp_alpha = 0.001  # Start with a small increment
    while True:
        ccp_alpha += 0.001  # Increase ccp_alpha gradually
        dt_classifier = DecisionTreeClassifier(ccp_alpha=ccp_alpha)
        dt_classifier.fit(x_train, y_train)
        
        # Check if the depth of the tree is 1
        if tree_depths(dt_classifier) == 1:
            break
    
    # Extract the remaining feature
    remaining_feature_index = dt_classifier.tree_.feature[0]
    if remaining_feature_index != -2:  # Check if a feature was selected
        best_feature = header_list[remaining_feature_index]

    return best_feature

# Example usage (Template Main section):
if __name__ == "__main__":
    # Load data
    file_path = "DT.csv"
    num_rows, data, header_list = load_data(file_path)
    print(f"Data is read. Number of Rows: {num_rows}"); 
    print("-" * 50)

    # Filter data
    data_filtered = filter_data(data)
    num_rows_filtered=data_filtered.shape[0]
    print(f"Data is filtered. Number of Rows: {num_rows_filtered}"); 
    print("-" * 50)

    # Data Statistics
    coefficient_of_variation = statistics_data(data_filtered)
    print("Coefficient of Variation for each feature:")
    for header, coef_var in zip(header_list[:-1], coefficient_of_variation):
        print(f"{header}: {coef_var}")
    print("-" * 50)

    # Split data
    x_train, x_test, y_train, y_test = split_data(data_filtered)
    print(f"Train set size: {len(x_train)}")
    print(f"Test set size: {len(x_test)}")
    print("-" * 50)
    
    # Train initial Decision Tree
    model = train_decision_tree(x_train, y_train)
    print("Initial Decision Tree Structure:")
    print_tree_structure(model, header_list)
    print("-" * 50)
    
    # Evaluate initial model
    acc_test, recall_test = evaluate_model(model, x_test, y_test)
    print(f"Initial Decision Tree - Test Accuracy: {acc_test:.2%}, Recall: {recall_test:.2%}")
    print("-" * 50)
    
    # Train Pruned Decision Tree
    model_pruned = train_decision_tree(x_train, y_train, ccp_alpha=0.002)
    print("Pruned Decision Tree Structure:")
    print_tree_structure(model_pruned, header_list)
    print("-" * 50)

    # Evaluate pruned model
    acc_test_pruned, recall_test_pruned = evaluate_model(model_pruned, x_test, y_test)
    print(f"Pruned Decision Tree - Test Accuracy: {acc_test_pruned:.2%}, Recall: {recall_test_pruned:.2%}")
    print("-" * 50)

    # Find optimal ccp_alpha
    optimal_alpha = optimal_ccp_alpha(x_train, y_train, x_test, y_test)
    print(f"Optimal ccp_alpha for pruning: {optimal_alpha:.4f}")
    print("-" * 50)

    # Train Pruned and Optimized Decision Tree
    model_optimized = train_decision_tree(x_train, y_train, ccp_alpha=optimal_alpha)
    print("Optimized Decision Tree Structure:")
    print_tree_structure(model_optimized, header_list)
    print("-" * 50)
    
    # Get tree depths
    depth_initial = tree_depths(model)
    depth_pruned = tree_depths(model_pruned)
    depth_optimized = tree_depths(model_optimized)
    print(f"Initial Decision Tree Depth: {depth_initial}")
    print(f"Pruned Decision Tree Depth: {depth_pruned}")
    print(f"Optimized Decision Tree Depth: {depth_optimized}")
    print("-" * 50)
    
    # Feature importance
    important_feature_name = important_feature(x_train, y_train,header_list)
    print(f"Important Feature for Fraudulent Transaction Prediction: {important_feature_name}")
    print("-" * 50)
        
# References: 
# Here please provide recognition to any source if you have used or got code snippets from
# Please tell the lines that are relavant to that reference.
# For example: 
# Line 80-87 is inspired by a code at https://stackoverflow.com/questions/48414212/how-to-calculate-accuracy-from-decision-trees

# Line 27, reading of CSV is from https://www.w3schools.com/python/pandas/pandas_csv.asp

# Line 39, usage of np.any is taught by https://www.geeksforgeeks.org/numpy-any-in-python/

# Line 47-55 is a maths formula derived from https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.cuemath.com%2Fcoefficient-of-variation-formula%2F&psig=AOvVaw3DdTF0HJvdw9bMExPlQn9F&ust=1712832552461000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLDZxc-8t4UDFQAAAAAdAAAAABAE

# Line 72 is learnt by studying documentation on train_test_split on https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html

# Line 80 on DecisionTreeClassifier is https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html

# Line 82 is inspired by a discussion on .fit on Stackoverflow https://stackoverflow.com/questions/45704226/what-does-the-fit-method-in-scikit-learn-do

# Lines 96 - 104 is learnt through https://scikit-learn.org/stable/tutorial/statistical_inference/supervised_learning.html

# Line 101 is from the scikit documentation https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html

# Line 102 is from the scikit documentation https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html

# Line 140 is drafted through a series of examples on https://scikit-learn.org/stable/modules/tree.html

# Line 164 was inspired by a series of discussions on what .feature means on stackoverflow https://stackoverflow.com/questions/39708304/what-is-the-output-of-clf-tree-feature