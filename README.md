
# Comprehensive Hospital Outcome Prediction System (CHOP)

**Table of Contents**
1. Pitch
2. Business understanding
3. Data understanding
4. Requirements
5. Usage.
6. Algorithm Overview
7. Results
8. Conclusion
References


**PITCH**

This project aims to predict facets of a patient's admission such as length of stay and cost. It is our vision that armed with this information, a hospital can better plan and allocate its resources. When a patient is admitted, the system will be able to predict the stay length and green or red light the admission based on resources needed.

---

**Business Understanding**

**Overview**

The CHOP Model aims to predict patient outcomes and optimize resource allocation in healthcare settings. By providing accurate predictions regarding patient stays, CHOP  will serve as a decision-support tool for healthcare administrators.

**Problem Statement**

Hospitals struggle to accurately forecast patient recovery times, potential complications, and necessary resources such as staff and beds. This uncertainty can result in either ***over-preparation*** 
(wasted resources), or **under-preparation**(poor service).

**Proposed Solution**

Our solution is to develop a model that given patient information, can predict aspects of their stay including duration and cost. By having a better picture of patient needs, the hospital can more efficiently plan for allocation of resources such as beds and staff.

The system will be able to monitor inpatient numbers to flag if available resources will meet demand in the near future. As an example, with projected number of patients in the coming days, if the system finds that staff on duty on a specific date falls short of demand, it will make this known to administrators.

---

**Objectives**

- **Dummy Hospital:** A fake hospital complete with room, patient and staff records will be created.

- **Data preparation:** The data is split into dozens of CSV files. Information in the relevant files will be extracted and joined in a way that is usable for model training.

- **Develop a Predictive Model:** Create a model capable of accurately predicting patient outcomes, including recovery time and likelihood of complications after the doctor has logged their diagnosis in the system.

- ***Model Accuracy:*** 80% has been set as the baseline for a successful model.

- **Hospital Management System:** A hospital management suite will be created featuring patient and staff management.

- **Deploy Model:** The model will be deployed to the management software.

- **Optimize Resource Allocation:** Use the model’s predictions to optimize the allocation of hospital resources, such as staff, equipment, and beds, ensuring they are used efficiently and effectively.

**Metrics of Success**

1. **Model Accuracy**: Achieving high accuracy in predicting patient outcomes is imperative.
2. **Compliance and Security**: Adherence to ethical standards and data privacy regulations.
3. **User Acceptance**: Positive feedback from hospital administration regarding the model's usability and insights.

**Challenges**

- **Data Availability and Quality:** Obtaining comprehensive, high-quality patient data that covers a wide range of variables is essential.

- **Complexity of Healthcare Data:** Medical data is complex. It includes medical records, lab results, and physician notes among others. Cleaning the data into a usable format will be a big undertaking.

- **Privacy and Security Concerns:** Handling sensitive patient data requires strict adherence to privacy regulations.

---

**Data Understanding**

**Data Sources**

The **MIMIC-IV** Clinical Database provides comprehensive clinical information on patients admitted to Beth Israel Deaconess Medical Center. The database contains de-identified patient data in compliance with HIPAA standards. Several subsets of the data have been pinpointed for use.

This dataset is a relational database where each table ha been stored as a CSV.

**Relevance of Data** 

The selected datasets collectively provide a holistic view of patient information, covering demographics, clinical diagnoses, lab results, and treatment services.

**Methodology**
Data Collection: Historical patient data was collected and stored for analysis.
Data Preprocessing: The data was cleaned, missing values were handled, and features were engineered to improve model performance.
Exploratory Data Analysis (EDA): Visualizations were created to understand the data distribution and correlations.
Model Development: Various machine learning models were developed, including Logistic Regression, Random Forest, and XGBoost.
Model Evaluation: The models were evaluated using accuracy, precision, recall, and F1 score to select the best-performing model.


**Data Visualization**

**Univariate Analysis**

![](Images/boxplot_age.PNG)
![](Images/distribution_age.PNG)
![](Images/Distribution_lengthofstay.PNG)
![](Images/box_lengthofstay.PNG)

**Bivariate Analysis**


**Time Series**
![](Images/admi_month.PNG)
![](Images/lengthofstay.PNG)
![](Images/readmi_month.PNG)
![](Images/drugs.png)





Modeling and Evaluation
Several models were developed and evaluated to determine the best approach for predicting patient outcomes. The following models were compared:

Length of stay

![](Images/boxcox_lengthofstay.PNG)
![](Images/probability_plot.PNG)
![](Images/lengthofstay_b_outliers.PNG)
![](Images/lengthofstay_a_outliers.PNG)
![](Images/probability_plot_2.PNG)


array([[ 0.        ,  0.        ,  0.        , ..., -0.39147085,
         0.34252208,  2.01675533],
       [ 0.        ,  0.        ,  0.        , ...,  1.17351989,
         1.07734694, -0.14947275],
       [ 0.        ,  0.        ,  0.        , ..., -0.39147085,
         0.34252208,  2.01675533],
       ...,
       [ 0.        ,  0.        ,  0.        , ...,  1.17351989,
         1.07734694, -0.14947275],
       [ 0.        ,  0.        ,  0.        , ...,  0.43290455,
        -1.6782463 , -1.27270212],
       [ 0.        ,  0.        ,  0.        , ...,  1.17351989,
         1.07734694, -0.14947275]])

Readmissions

**Logistic Regression**
Accuracy: 0.82035
              precision    recall  f1-score   support

           0       0.89      0.85      0.87     13716
           1       0.70      0.76      0.73      6284

    accuracy                           0.82     20000
   macro avg       0.79      0.80      0.80     20000
weighted avg       0.83      0.82      0.82     20000

**Confussion Matrix**

Accuracy: 0.84505
              precision    recall  f1-score   support

           0       0.90      0.87      0.88     13716
           1       0.73      0.80      0.76      6284

    accuracy                           0.85     20000
   macro avg       0.82      0.83      0.82     20000
weighted avg       0.85      0.85      0.85     20000



**Logistic Regression**

Mean Absolute Error (MAE): 0.53
Mean Squared Error (MSE): 0.45
Root Mean Squared Error (RMSE): 0.67
R-squared (R²): 0.37
Median Absolute Error: 0.43
Explained Variance Score: 0.37

Accuracy: 0.82035
              precision    recall  f1-score   support

           0       0.89      0.85      0.87     13716
           1       0.70      0.76      0.73      6284

    accuracy                           0.82     20000
   macro avg       0.79      0.80      0.80     20000
weighted avg       0.83      0.82      0.82     20000

Death

sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cbar=False, xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel("Predicted Values")
plt.ylabel("Actual values")
plt.title("Random Forest Confusion Matrix")
plt.show()

**Random Forest**

Mean Absolute Error (MAE): 0.23
Mean Squared Error (MSE): 0.23
Root Mean Squared Error (RMSE): 0.48
R-squared (R²): 0.78
Median Absolute Error: 0.00
Explained Variance Score: 0.78

Accuracy: 0.84505
              precision    recall  f1-score   support

           0       0.90      0.87      0.88     13716
           1       0.73      0.80      0.76      6284

    accuracy                           0.85     20000
   macro avg       0.82      0.83      0.82     20000
weighted avg       0.85      0.85      0.85     20000



**XGBoost**

Model Accuracy
The final model was evaluated based on the following metrics:

Accuracy: 85%
Precision: 82%
Recall: 80%
F1 Score: 81%

Figure 3: Comparison of model accuracy across different models.

Results
The CPORP Model was able to accurately predict patient outcomes with a high degree of accuracy. The most significant features contributing to predictions were patient age, previous medical history, and the type of treatment received. The model's predictions were validated against a test dataset, and the results were consistent with the expected outcomes.

Conclusion
The CPORP Model demonstrates the potential for machine learning in healthcare to improve patient outcomes and optimize resource allocation. By leveraging historical data, the model provides actionable insights that can assist healthcare providers in making informed decisions.

Future Work
Model Refinement: Further tuning and testing with more diverse datasets to improve accuracy.
Integration: Implementing the model into hospital management systems for real-time predictions.
Expanding Features: Including additional features such as patient lifestyle factors to improve prediction accuracy.

