# Machine Learning Modeling Pipeline

## Overview
This project involves building a machine learning model to predict hospitalization risk in elderly individuals. The pipeline includes data preprocessing, feature selection using Cramér’s V, model training using logistic regression and random forest, and evaluation.

## Table of Contents
1. [Dataset and Preprocessing](#dataset-and-preprocessing)
2. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
3. [Feature Selection](#feature-selection)
4. [Model Training](#model-training)
5. [Evaluation](#evaluation)
6. [Results](#results)

---

## Dataset and Preprocessing
### **Data Source**
- The dataset consists of panel data collected from multiple survey waves.
- Only respondents aged 50+ were included to focus on elderly individuals.

### **Filtering Criteria**
- Include only **elderly individuals** (50 years or older).
- Exclude deceased individuals.
- Include only **directly surveyed respondents** (not proxy responses).

### **Handling Missing Data**
- Variables with more than 30% missing values were dropped.
- Missing values in categorical columns were labeled as 'Missing'.
- Missing numerical values were replaced with -999.

### **Balancing Data**
- The dataset had a high imbalance in the target variable (hospitalization).
- **SMOTE (Synthetic Minority Over-sampling Technique)** was applied to balance the dataset.

---

## Exploratory Data Analysis (EDA)
- **Class distribution analysis** to check the imbalance in hospitalization rates.
- **Correlation analysis** to check associations between features and target.
- **Cardinality check** to remove high-cardinality categorical variables.
- **Visualization** of missing data, class distribution, and feature distributions.

---

## Feature Selection
### **Step 1: Filter-Based Selection**
- **Variance Thresholding**: Low-variance features were removed.
- **Cramér’s V Chi-Square Test**:
  - Measures associations between categorical features and the target.
  - Features with weak associations were removed.
- **Mutual Information**: Selected variables with high relevance to the target variable.

### **Step 2: Importance-Based Selection**
- A **Random Forest Classifier** was used to rank feature importance.
- The top **30 most important features** were retained.

---

## Model Training
### **Logistic Regression**
- Standard logistic regression was trained with balanced class weights.
- Feature scaling was applied to standardize numerical features.

### **Random Forest Classifier**
- Used for both feature selection and final model training.
- Hyperparameters:
  - `n_estimators=1000`
  - `random_state=42`

### **Other Models Tested**
- XGBoost
- Stochastic Gradient Descent (SGD)
- K-Nearest Neighbors (KNN)

---

## Evaluation
- **Metrics Used**:
  - **Accuracy**
  - **Precision, Recall, F1-score**
  - **ROC-AUC Score**
- **Threshold Adjustment**:
  - Decision threshold optimized for **high recall** (to reduce false negatives).

---


## XGBoost Model for Maximizing Recall
### **Objective**
- The XGBoost model was designed to **maximize recall for class 1 (non-hospitalized patients)** by reducing false negatives.

### **Key Steps**
1. **Handling Class Imbalance**
   - Applied **SMOTE** to balance the training dataset.
   - Used `scale_pos_weight` to adjust for minority class weighting.

2. **Feature Selection**
   - Selected **top 30 features** based on Random Forest and Cramér’s V importance.

3. **Model Training**
   - **Hyperparameters:**
     - Learning rate: `0.03`
     - Estimators: `300`
     - Max depth: `6`
     - Gamma: `2`
     - Subsample & Colsample_bytree: `0.7`
   - **Objective:** `"binary:logistic"` with `"logloss"` as the evaluation metric.

4. **Threshold Adjustment**
   - Optimized threshold to improve recall while maintaining reasonable precision.
   - Used precision-recall curve analysis to find the best probability threshold.

5. **Performance Metrics**
   - **High recall for class 1** (non-hospitalized patients) to minimize false negatives.
   - **Confusion Matrix** adjusted for recall optimization.
   - **ROC-AUC Score** used for overall model calibration.

   

## Results
- **Top Features Influencing Hospitalization Risk**:
  - Mobility limitations
  - ADL (Activities of Daily Living) impairments
- **Feature explanations included for interpretability.**

---

## Outputs:
- Processed dataset (`cleaned_dataset.csv`)
- Trained models (`logistic_regression_model.joblib`, `random_forest_model.joblib`, `xgb_model.pkl`)
- Feature importance (`top_features.joblib`)
