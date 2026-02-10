# Logistic Regression – Real-Time Fraud Detection (From Scratch)

## Overview

This project builds a **real-time fraud detection system** using a Logistic Regression model implemented **from scratch**.

The goal is to simulate how a real Machine Learning system works in production using:

- Kafka streaming
- Real-time prediction
- WebSocket live output
- PostgreSQL logging

This is not a notebook-style model.  
It is a **streaming ML system**.


## Dataset

Fraud Detection Dataset  
https://www.kaggle.com/datasets/kartik2112/fraud-detection

The dataset is used for:
- training the model
- simulating live transaction streams


### Raw Data Handling
- CSV files are stored in `data/raw/`
- All columns from the dataset are loaded directly into a **raw database table**
- No feature engineering is performed at the raw layer
- The database is treated as the **source of truth**


## System Flow

```text
Transaction Generator
        ↓
      Kafka
        ↓
   ML Consumer
        ↓
    Prediction
        ↓
     Decision
        ↓
WebSocket (Real-Time Output)
        ↓
   PostgreSQL

```


### Flow Steps

1. Producer reads dataset and streams transactions to Kafka  
2. Consumer receives transaction from Kafka  
3. Feature engineering applied  
4. Logistic regression predicts fraud probability  
5. Decision made:
   - BLOCK  
   - ALLOW  
6. Result pushed to WebSocket (real-time console output)  
7. Result stored in PostgreSQL  


## Model

Logistic Regression implemented **from scratch**:
- sigmoid
- loss
- gradient descent
- weight updates
- prediction pipeline

No pre-built ML libraries used.


## Problem Statement

Build a simple but realistic **real-time ML pipeline** that mimics how fraud detection systems work in production.