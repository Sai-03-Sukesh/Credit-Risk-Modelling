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

| Feature | Formula | Insight |
|---|---|---|
| `loan_to_income` | `loan_amount / income` | Higher LTI → higher default risk |
| `delinquency_ratio` | `delinquent_months / total_loan_months × 100` | % of loan life spent delinquent |
| `avg_dpd_per_delinquency` | `total_dpd / delinquent_months` (0 if none) | Severity of late payments |

### 4. Feature Selection

**VIF Analysis** — Removed multicollinear features:
`sanction_amount`, `processing_fee`, `gst`, `net_disbursement`, `principal_outstanding`

**Weight of Evidence (WOE) / Information Value (IV)** — Retained only features with IV > 0.02, removing low-signal columns like `city`, `state`, `gender`, `marital_status`, `employment_status`.

### 5. Encoding
One-hot encoding (`drop_first=True`) on remaining categorical features: `residence_type`, `loan_purpose`, `loan_type`.

### 6. Modeling — 4 Attempts

| Attempt | Model | Imbalance Handling | Tuning |
|---|---|---|---|
| 1 | LR / RF / XGBoost | None | None |
| 2 | LR + XGBoost | RandomUnderSampler | RandomizedSearchCV |
| 3 | Logistic Regression | SMOTETomek | Optuna (50 trials) |
| 4 | XGBoost | SMOTETomek | Optuna (50 trials) |

SMOTETomek combines oversampling of minority class with Tomek link removal to clean decision boundaries.

**Final model: Logistic Regression (Attempt 3)** — chosen for interpretability while matching XGBoost performance.
---

## Performance & Validation

| Metric | Value |
|---|---|
| AUC-ROC | **0.98** |
| Gini Coefficient | **0.96** |
| KS Statistic | Strong rank ordering across all deciles |

**Rank ordering** confirmed — deciles with highest predicted default probability consistently show the highest actual default rates.
---

## Credit Score System

The model's default probability is mapped to a **300–900 credit score**:

```
credit_score = 300 + (1 - default_probability) × 600
```

| Score Range | Rating |
|---|---|
| 750 – 900 | Excellent |
| 650 – 749 | Good |
| 500 – 649 | Average |
| 300 – 499 | Poor |

---

## Project Structure

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

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10 |
| ML | scikit-learn, XGBoost, imbalanced-learn |
| Hyperparameter Tuning | Optuna |
| Feature Selection | WOE/IV, VIF (statsmodels) |
| Data | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| App | Streamlit |
| Serialization | Joblib |

---

## Key Takeaways & Best Practices

1. **Strict Data Leakage Controls**: Performing pre-EDA stratified splitting protected the inference pipeline against cross-sample variance leakage.
2. **Explainability Over Black-Box Models**: Linear risk scorecards preserve regulatory defensibility by ensuring each coefficient represents an exact marginal effect on log-odds.
3. **Real-Time Assessment**: The Streamlit deployment provides an intuitive, immediate risk evaluation interface for loan officers, removing manual review bottlenecks.
