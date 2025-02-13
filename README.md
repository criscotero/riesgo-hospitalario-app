# Hospitalization Prediction for Elderly People in Mexico

## Project Overview

This project aims to predict the **probability of hospitalization** for **elderly individuals in Mexico** using **machine learning algorithms**. The model is designed to assist **healthcare providers and insurers** in identifying **high-risk patients**, enabling better **risk assessment, resource allocation, and insurance underwriting decisions**.

## Goal

The primary goal is to allow users to **complete a form** with their health-related information, and the **trained machine learning model** will predict their **risk of hospitalization** in the next year.

---

## 1. Dataset Description

### Source

The dataset is sourced from the **Mexican Health and Aging Study (MHAS)**, which consists of **household surveys** collecting information on health, economic status, and quality of life for elderly individuals over multiple waves.

### Preprocessing Steps

- Data from **Wave 5** was selected to ensure the most recent and reliable predictions.
- **Filtering criteria** included:
  - **Age 50+** (focusing on elderly individuals)
  - **Living respondents only** (excluding deceased individuals)
  - **Direct survey responses only** (removing data from proxy respondents)
- **Missing Data Handling:**
  - **High-missing-value columns (>50%)** were dropped.
  - **Categorical data** was encoded using **LabelEncoder**.
  - **Numerical missing values** were treated with a placeholder (-9999).
- **Class Balancing:**
  - **SMOTE (Synthetic Minority Over-sampling Technique)** was applied to balance the dataset, ensuring better model generalization.

---

## 2. Feature Selection

### Methods Used

1. **Statistical Methods (Cramér’s V, ANOVA, Chi-square, Mutual Information)** to identify relevant features.
2. **Feature Importance from Random Forest** to rank predictors based on their contribution.
3. **Business Logic** to manually select the most meaningful features based on domain knowledge.

### Selected Features

After applying these techniques, the final model was trained on the **top 13 most important features**, including:

- **Medical history indicators** (e.g., hospitalizations, doctor visits, medication costs).
- **Mobility and functional dependency** (e.g., difficulty with daily activities, number of falls, mobility limitations).
- **Cognitive and psychological factors** (e.g., life satisfaction, cognitive function tests).

---

## 3. Model Development

### Models Evaluated

We tested multiple machine learning models to optimize predictive performance:

#### **Baseline Model: Logistic Regression**

- Trained on a balanced dataset.
- Performance was **evaluated using accuracy, precision, recall, and AUC-ROC**.

#### **Random Forest Classifier**

- Used for further **feature selection** and benchmark comparisons.

#### **XGBoost Classifier**

- Selected to capture **non-linear relationships**.
- Trained with **optimized hyperparameters** (e.g., max depth, learning rate, number of estimators).

#### **SGD Classifier (Stochastic Gradient Descent)**

- Experimented with **logistic regression loss** and **L2 regularization**.
- Used for **fast and scalable training on large datasets**.

#### **Threshold Optimization for Logistic Regression**

- Adjusted the **decision threshold** to **increase recall** for hospitalized cases while maintaining precision.
- Used the **Precision-Recall Curve** to select an optimal threshold.

---

## 4. Model Evaluation

Each model was evaluated using:

- **Accuracy**: Overall correctness of predictions.
- **Precision & Recall**: Trade-offs between false positives and false negatives.
- **F1-Score**: Balance between precision and recall.
- **Confusion Matrix**: Breakdown of classification performance.
- **AUC-ROC Curve**: Measure of model discrimination ability.

### Key Results

- **Logistic Regression (Baseline):** Accuracy \~81%, but low recall for hospitalized cases.
- **Random Forest:** High accuracy (\~90%) but weak recall (\~35%) for hospitalized patients.
- **XGBoost:** Improved recall (\~79%) but precision suffered (\~16%), leading to many false positives.
- **Threshold-tuned Logistic Regression:** Achieved better recall (\~80%) while improving precision.

---

## 5. Deployment & Future Steps

### Model Deployment

- The final optimized model was **saved using Joblib** for future use.
- Feature encoders and mappings were stored to maintain consistency in production.

### Future Improvements

- **Further optimize hyperparameters** to reduce bias-variance trade-offs.
- **Explore deep learning approaches** for better feature interactions.
- **Test alternative resampling techniques** instead of SMOTE for class balancing.
- **Deploy as a web API** to integrate predictions into healthcare applications.

---

## 6. Conclusion

This project successfully developed and optimized a **machine learning model** to predict **hospitalization risk** for elderly individuals in Mexico. The use of **feature selection, class balancing, and threshold tuning** significantly improved model performance, particularly in **recalling high-risk patients**. While further improvements are possible, this model lays the groundwork for **real-world applications in healthcare and insurance risk assessment**.

