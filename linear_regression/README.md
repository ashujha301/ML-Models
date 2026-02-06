# Linear Regression – (From Scratch)

## Project Overview

This project focuses on building a **production-oriented Linear Regression system from scratch**, following real-world **Machine Learning Engineering (MLE)** practices.

The goal is not just to train a model, but to design an **end-to-end ML pipeline** including:
- Data ingestion
- Storage in a relational database
- Feature engineering
- Model training from scratch ( Without using pre build ml-models )
- Inference and logging
- Testing and reproducibility
- Pipeline script

---

## Dataset

### Dataset Name
1. **Marketing Campaign Performance Dataset** Link :- https://www.kaggle.com/datasets/manishabhatt22/marketing-campaign-performance-dataset/data
2. **California Housing Price Dataset** Link :- https://www.kaggle.com/datasets/camnugent/california-housing-prices

### Source
Downloaded from Kaggle and stored locally as raw data.

### Dataset Characteristics
The dataset contains performance metrics of Both Dataset, including:
- Spend-related features
- Housing features
- Engagement metrics
- Conversion-related signals
- Revenue outcomes
- Inference Log
- Training runs log

The raw dataset is ingested **as-is** into PostgreSQL without transformations.

### Raw Data Handling
- CSV files are stored in `data/raw/`
- All columns from the dataset are loaded directly into a **raw database table**
- No feature engineering is performed at the raw layer
- The database is treated as the **source of truth**

---

## Problem Statement

### Business Objective
1. Predict **Clicks** based on performance metrics on **Marketing Campaign Raw** data.
2. Predict **House price** based on the metrics on **Housing Raw** data.