# ML-Based Network Intrusion Detection
**Dataset:** UNSW-NB15 Network Intrusion Dataset  
**Tools:** Python, PyCaret

## Overview
Binary classification system for network intrusion detection
using automated machine learning. Evaluates multiple ML
algorithms on the UNSW-NB15 benchmark dataset to identify
the most effective model for distinguishing normal vs
attack network traffic.

## Problem Statement
Traditional signature-based intrusion detection systems
fail against novel attack patterns. This project explores
ML-based approaches that learn behavioral patterns rather
than relying on known signatures. 

## Dataset
**UNSW-NB15** — Created by the Australian Centre
for Cyber Security (ACSC).

- 2,540,044 total records
- 49 features including network flow attributes
- 9 attack categories:
  Fuzzers, Analysis, Backdoors, DoS,
  Exploits, Generic, Reconnaissance,
  Shellcode, Worms
- Binary label: Normal (0) vs Attack (1)

## Methodology

### 1. Automated ML Pipeline (PyCaret)
- Compared multiple classification algorithms

### 2. Models Evaluated
- Random Forest
- Gradient Boosting
- LightGBM
- XGBoost
- Logistic Regression
- Decision Tree
- K-Nearest Neighbors

### 5. Evaluation Metrics
- Accuracy

## Results
| Model | Feature | Accuracy% | Confusion Matrix | Analysis 
|---|---|---|---|---|
| Logistic Regression | Source interpacket arrival time (mSec) | 73.86 | Confusion observed | Slightly Lower accuracy
|  Ridge | Transaction protocol | 87.13 | No confusion | Transaction protocol is identified as an indication of cyber-attack with high accuracy models
| Linear Discriminant Analysis | Transaction protocol | 87.13 | Slight confusion | Transaction protocol is identified as an indication of cyber-attack with high accuracy models
| Random Forest Classifier | No of connections of the same source (1) and the destination (3) address in 100 connections according to the last time (26) | 90.29 | No confusion | Same source destination IPs indicate denial of service attacks
| Gradient Boosting Classifier | Source to destination time to live value | 90.12 | No Confusion | Time to live is an indication for the pack to stay alive before it is discarded
| Ada Boost Classifier | Source to destination transaction bytes | 89.62 | No confusion | Time to live is an indication for the pack to stay alive before it is discarded
| Extra Trees Classifier | Source to destination time to live value | 89.92 | No confusion | Time to live is an indication for the pack to stay alive before it is discarded
| Decision Tree Classifier | Source to destination time to live value | 89.58 | No confusion | Time to live is an indication for the pack to stay alive before it is discarded
| SVM | Destination bits per second | 39.6 | High confusion | Low accuracy
| Keras NN | Represents the pipelined depth into the connection of http request/response transaction | 74.19 | Confusion observed | Slightly lower accuracy

## Key Findings
A clear pattern has emerged after the analysis of model features, confusion matrix and accuracy. The top three features identified for the dataset with the highest accuracy models are transaction protocols, same source and destination IPs, and packet time to live. These three features can be used to detect cyber-attacks in the network using the highest accuracy models. Random forest, gradient boosting and extra trees are the top three models observed based on accuracy.

## Tech Stack
`Python` `PyCaret` `matplotlib` 

## References
- Moustafa, N. & Slay, J. (2015). UNSW-NB15 Dataset
- PyCaret Documentation
- Australian Centre for Cyber Security

## Connect
[LinkedIn](your-linkedin-url) |
[GitHub Profile](https://github.com/abrarmalik2000)
