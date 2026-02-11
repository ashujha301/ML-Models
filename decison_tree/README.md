# Decision Tree – Loan Approval System (From Scratch)

## Overview

This project builds a **Decision Tree model from scratch** and integrates it into a small production-style ML system for loan approval decisions.

The focus is on:
- Implementing the model from scratch  
- Running a real inference API  
- Handling concurrent prediction requests  
- Logging predictions  
- Retraining and model versioning  
- Monitoring with Prometheus + Grafana  
- Safe model rollback  

This is not a notebook-only project.  
It simulates how decision-based ML systems run in production.

## Dataset

Loan Prediction Dataset:- https://www.kaggle.com/datasets/nikhil1e9/loan-default

Used for:
- training the model  
- simulating user loan applications  
- retraining with new data  

### Raw Data Handling

- CSV stored in `data/raw/`  
- Loaded into PostgreSQL raw tables  
- Database treated as source of truth  


## System Flow

```text
        User Request
            ↓
    FastAPI (Concurrent API)
            ↓
     Feature Builder
            ↓
    Decision Tree Model
            ↓
     Approval Decision
            ↓
    PostgreSQL Logging
            ↓
 Monitoring (Prometheus + Grafana)
            ↓
 Model Retraining & Versioning
            ↓
 Model Rollback if needed

```

## Flow Steps

1. User sends loan application request

2. FastAPI handles concurrent requests

3. Features generated from input

4. Decision tree predicts approval

5. Result returned to user

6. Prediction logged in PostgreSQL

7. Metrics tracked via Prometheus

8. Grafana dashboards monitor model behavior

9. Model retrained on new data

10. New version deployed with rollback support


## Problem Statement
Build a realistic ML system that shows how loan approval models are trained, served via API, monitored, retrained, and safely rolled back in production.