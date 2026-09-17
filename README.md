# Credit Risk Modelling

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22+-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-4CAF50)
![Optuna](https://img.shields.io/badge/Optuna-3.x-6C63FF)
![License](https://img.shields.io/badge/License-MIT-green)

An end-to-end credit risk evaluation and scoring engine designed to assess retail borrower default probabilities, generate a 300–900 CIBIL-like credit score, and assign risk tiers (Poor to Excellent). Built across 50,000 multi-table relational records, the final production model leverages an explainable Logistic Regression architecture achieving **ROC-AUC = 0.98** and **Gini = 0.96**.

The platform features an interactive, modern **Streamlit** dashboard tailored for underwriting officers to assess loan applications in real-time.

---

## Business Problem & Context

Non-Banking Financial Companies (NBFCs) and retail lenders face high operational costs and loss rates due to manual, subjective underwriting. This project automates the risk evaluation pipeline by:
* Predicting the individual likelihood of default ($P(\text{Default})$) from demographic, loan, and bureau indicators.
* Transforming probabilities into an interpretable credit scorecard calibrated to industry credit tiering.
* Laying the algorithmic foundation for **Straight-Through Processing (STP)** for prime, low-risk applicants.

---

## System Architecture

```text
                  +----------------------------------------------+
                  |    Relational Sources (50k records each)    |
                  |  [customers.csv] [loans.csv] [bureau_data]   |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |             Data Hygiene & Prep              |
                  | - Stratified Split (75/25) prior to EDA      |
                  | - Mode Imputation & Business Rule Filtering  |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |        Feature Engineering & Selection       |
                  | - Ratios: LTI, Delinquency %, Avg DPD/Delinq |
                  | - VIF Multicollinearity Pruning              |
                  | - Information Value (IV) / WOE Filtering     |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |          Model Selection & Training          |
                  | - Imbalance Handling (SMOTETomek)            |
                  | - Benchmarking: LR, Random Forest, XGBoost   |
                  | - Hyperparameter Optimization (Optuna)       |
                  | - Selected: High-Explainability Logistic Reg |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |         Inference & Deployment Layer         |
                  | - Artifact: model_data.joblib (Weights/Meta) |
                  | - UI Client: Streamlit Interactive Portal    |
                  +----------------------------------------------+
```

---

## Data Pipeline & Schema

The dataset consolidates three tables joined via unique primary key `cust_id`:

| Source | Volume | Dimensions | Core Attributes |
|---|---|---|---|
| `customers.csv` | 50,000 | 12 | Demographics: Age, Gender, Income, Dependents, Residence Type |
| `loans.csv` | 50,000 | 15 | Financials: Sanction/Disbursed Amounts, Tenure, Purpose, `default` flag |
| `bureau_data.csv` | 50,000 | 8 | Credit Bureau History: DPD, Delinquent Months, Accounts, Utilization |

* **Class Distribution**: Non-Default (`0`) = 45,703 (91.41%), Default (`1`) = 4,297 (8.59%).
* **Imbalance Ratio**: ~10.6:1 (Requires targeted sampling and threshold calibration).

---

## Machine Learning Lifecycle

### 1. Data Splitting & Leakage Prevention
* Executed a stratified **75/25 train-test split** (`random_state=42`) strictly before any exploratory analysis or transformation to prevent target leakage.

### 2. Data Cleaning & Business Rules
* **Imputation**: Categorical nulls in `residence_type` imputed using the training set mode (`'Owned'`) across both splits.
* **Integrity Validation**: Filtered record anomalies where processing fee exceeded institutional caps (> 3% of principal) and verified GST/net disbursement alignments.

### 3. Feature Engineering

| Feature | Formula | Financial Rationale |
|---|---|---|
| `loan_to_income` | $\frac{\text{loan\_amount}}{\text{income}}$ | Measures leverage burden relative to borrower earning capacity. |
| `delinquency_ratio` | $\frac{\text{delinquent\_months}}{\text{total\_loan\_months}} \times 100$ | Percentage of active credit lifecycle spent in past-due status. |
| `avg_dpd_per_delinquency` | $\frac{\text{total\_dpd}}{\text{delinquent\_months}}$ | Reflects structural payment distress vs. accidental short delay. |

### 4. Feature Selection & Pruning
* **Multicollinearity Elimination (VIF)**: Dropped redundant linear combinations (`sanction_amount`, `processing_fee`, `gst`, `net_disbursement`, `principal_outstanding`).
* **Information Value (IV) / WOE**: Retained features with $\text{IV} \ge 0.02$, stripping non-predictive noise (e.g., localized demographic identifiers).
* **Encoding**: One-hot encoded remaining categorical attributes (`residence_type`, `loan_purpose`, `loan_type`) with reference base categories dropped (`drop_first=True`).

### 5. Benchmark Experiments & Modeling Matrix

| Iteration | Candidate Architecture | Resampling Strategy | Optimization Method | Performance / Status |
|:---:|---|---|---|---|
| **1** | Logistic Regression / Random Forest / XGBoost | None (Class Imbalance Intact) | Default baseline | High precision, inadequate minority recall |
| **2** | Logistic Regression + XGBoost | Random Under Sampling | RandomizedSearchCV | Information loss from undersampling |
| **3** | **Logistic Regression (Production)** | **SMOTETomek** | **Optuna (50 Trials)** | **Best Generalized Explainability (Selected)** |
| **4** | XGBoost Classifier | SMOTETomek | Optuna (50 Trials) | Matched AUC-ROC; rejected due to black-box nature |

> **Selection Justification**: In compliance with regulatory standards (e.g., Fair Lending / RBI guidelines) and project SOW constraints, **Logistic Regression** was chosen as it delivers mathematical parameter transparency ($W^T x + b$), coefficient interpretability, and direct score translation while matching gradient boosted tree performance.

---

## Performance & Validation

```text
  Metric                  Validation Result
  =========================================
  ROC-AUC Score           0.98
  Gini Coefficient        0.96
  KS-Statistic            > 65% (Strong separation)
  Decile Rank Ordering    Monotonic default distribution
```

* **Gini & Decile Validation**: Risk profiles demonstrated pure monotonic rank-ordering; top deciles capture over 80% of systemic defaults.

---

## Scorecard & Risk Classification

The model computes log-odds, maps them through the sigmoid link function to determine $P(\text{Default})$, and derives the non-default probability $P(\text{Non-Default})$:

$$\text{Log-Odds: } z = \mathbf{w}^T \mathbf{x} + b$$

$$P(\text{Default}) = \frac{1}{1 + e^{-z}}$$

$$P(\text{Non-Default}) = 1 - P(\text{Default})$$

$$\text{Credit Score} = 300 + \Big(P(\text{Non-Default}) \times 600\Big)$$

### Risk Tier Alignment

| Score Band | Category Rating | Underwriting Action | Phase 2 STP Policy |
|:---:|:---:|---|---|
| **750 – 900** | **Excellent** | Immediate Approval / Preferential APR | **Straight-Through Processing (STP)** |
| **650 – 749** | **Good** | Standard Approval Workflow | Fast-Track Verification |
| **500 – 649** | **Average** | Enhanced Collateral / Income Audit | Manual Underwriter Review |
| **300 – 499** | **Poor** | Automated Reject / Adverse Action Notice | Rejected |

---

## Repository Structure

```text
.
├── my_credit_risk_modelling.ipynb      # End-to-end notebook: EDA, WOE/IV, Tuning, Evaluation
├── dataset/
│   ├── customers.csv                   # Borrower demographics (50,000 records)
│   ├── loans.csv                       # Historical loan performance & default label
│   └── bureau_data.csv                 # Credit bureau metrics, DPD, & utilization
├── artifacts/
│   └── model_data.joblib               # Production artifacts: Weights, Scaler, Feature schema
├── app/
│   ├── main.py                         # Streamlit front-end with dark glassmorphic styling
│   └── prediction_helper.py            # Preprocessing vectorizer & scoring algorithm
└── requirements.txt                    # Project environment dependencies
```

---

## Getting Started

### 1. Prerequisites & Environment
Ensure Python 3.10+ is installed:
```bash
git clone https://github.com/Sai-03-Sukesh/Credit-Risk-Modelling.git
pip install -r requirements.txt
```

### 2. Run the Streamlit Application
Launch the interactive loan officer portal:
```bash
cd app
streamlit run main.py
```
---

## Key Takeaways & Best Practices

1. **Strict Data Leakage Controls**: Performing pre-EDA stratified splitting protected the inference pipeline against cross-sample variance leakage.
2. **Explainability Over Black-Box Models**: Linear risk scorecards preserve regulatory defensibility by ensuring each coefficient represents an exact marginal effect on log-odds.
3. **Real-Time Assessment**: The Streamlit deployment provides an intuitive, immediate risk evaluation interface for loan officers, removing manual review bottlenecks.
