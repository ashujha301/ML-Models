# Linear Regression – Marketing Revenue Prediction (From Scratch)

## Project Overview

This project focuses on building a **production-oriented Linear Regression system from scratch**, following real-world **Machine Learning Engineering (MLE)** practices.

The goal is not just to train a model, but to design an **end-to-end ML pipeline** including:
- Data ingestion
- Storage in a relational database
- Feature engineering
- Model training from scratch ( Without using pre build ml-models )
- Inference and logging
- Testing and reproducibility

---

## Dataset

### Dataset Name
**Marketing Campaign Performance Dataset**

### Source
Downloaded from Kaggle and stored locally as raw data.

### Dataset Characteristics
The dataset contains performance metrics of marketing campaigns, including:
- Spend-related features
- Engagement metrics
- Conversion-related signals
- Revenue outcomes

The raw dataset is ingested **as-is** into PostgreSQL without transformations.

### Raw Data Handling
- CSV files are stored in `data/raw/`
- All columns from the dataset are loaded directly into a **raw database table**
- No feature engineering is performed at the raw layer
- The database is treated as the **source of truth**

---

## Problem Statement

### Business Objective
Predict **campaign revenue** based on campaign performance metrics.