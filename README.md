# ML-Models ( From Scratch )

This repository contains **machine learning models implemented from scratch**, without using pre-built ML libraries like scikit-learn or TensorFlow.

The purpose of this repo is to **understand how ML works internally** and to practice **real-world Machine Learning Engineer (MLE) workflows**.

---

## What this repo focuses on

- Writing **core ML algorithms manually**
- Understanding the **math behind models**
- Working with data like real systems (DB → features → model)
- Separating **training** and **inference**
- Logging metrics and debugging model behavior

No black-box `.fit()` or `.predict()` calls.

---

## Repo structure

Each model follows a real-world style structure:

```text
model-name/
├── data/           # Data & database logic
├── features/       # Feature engineering
├── models/         # Core algorithms & math
├── training/       # Training logic
├── inference/      # Prediction logic
└── utils/          # Logging & helpers
```


## How to use

Each model folder is independent.

1. Install dependencies
2. Set up the database
3. Train the model
4. Store Model and scaler features
5. Run inference on trained model and features
6. Use Pipeline script to run a specific problem set

Check the model-specific `README.md` for details.

---

**Built for learning, clarity, and real-world understanding.**