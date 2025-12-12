# Equity Signals - Proeject Overview
Owner: Enrique Zafra Mena

## 1. Purpose
This repository implements a small but realistic **quant equity forecasting** pipeline based on daily OHLCV data for a fixed universe of US large-cap stocks and equity indices.  
The main goal is to estimate the **probability that next-day return is positive** and evaluate simple trading strategies based on these signals.


---
## 2. Directory Structure
```text
data/
    raw/
    processed/

features/
    raw/                                        # intermediate feature tables
    processed/                                  # final feature panel usedfor modeling

models/

notebooks/
    01_download_checks.ipynb
    02_exploratory_analysis.ipynb               # univariate and multivariate EDA
    03_feature_engineering.ipynb                # construction and validation of feature sets
    04_modelling.ipynb                          # baeline models + LSTM training/validation
    05_backtest_and_eval.ipynb                  # strategy backtest and performance evaluation
    06_final_report.ipynb                       # figures/bles for final report

reports/


src/
    data_ingest/
        yahoo.py
        sync_data.py
    processing/
        cleaners.py
        readers.py
        data_cleaning.py
        validation.py
        panel.py
        windowing.py
    modelling/
    backtest/
    utils/
        config.py                               # Imports config.yaml as a dict. and other utilities

tests/

config.yaml
requirements.txt
Dockerfile

```

---
## 3. Data Flow (high-level)

### 1. Ingestion (src/data_ingest)


### 2. Processing (src/processing)


### 3. Feature Engineering (03_feature_engineering.ipynb + src/processing)
From the processed panel, compute
- log-returns and lags
- rolling volatilities
- normalized volumnes
- PCA factors from multiassets panel

Save final feature panel to features/processed

### 4. Modelling (04_modelling.ipynb + src/modelling)
Build train/validation/test splits according to config


### 5. Backtest


---
## 4. Configuration (config.yaml)




---
## 5. Core data objects (TODO)
Main logical data objects used across the project

- Price/return Panel

- Feature panel

- Windowed dataset 

---
## 6. Notebooks vs. Modules
Notebooks will be used for:
- Exploratory work, plots and some analysis
- Developing of reusable functions from 'src/'

Python modules from 'src/' must contain:
- Reusable logic with stable functions
- Minimal printing/logging, no plotting
- Clear assumptions about inputs/outputs
