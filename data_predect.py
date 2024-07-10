import geopandas as gpd
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from shapely.geometry import LineString
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from scipy.stats import f as f_distribution
import joblib
import os

data = gpd.read_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/data_predect/combined_data_encoding.gpkg")
data.drop(columns=['sit_fam_DIV', 'sit_fam_INC', 'sit_fam_MAR', 'sit_fam_SF', 'niveau_L', 'niveau_M',
                    'niveau_P', 'niveau_SN', 'niveau_U', 'cat_veh_Lour', 'cat_veh_MOTO', 'cat_veh_NA',
                    'cat_veh_Transport','type_route_RN','Population','Area','etat_route_PM','meteo_C'], inplace=True)



def calculate_f1_and_p_values(y_test, lr_predict, rf_predict, svm_predict, dt_predict, X_test):
    # Calculate F-score for the Logistic Regression model
    lr_f1 = f1_score(y_test, lr_predict, average='macro')

    # Calculate F-score for the Random Forest model
    rf_f1 = f1_score(y_test, rf_predict, average='macro')

    # Calculate F-score for the SVM model
    svm_f1 = f1_score(y_test, svm_predict, average='macro')

    # Calculate F-score for the Decision Tree model
    dt_f1 = f1_score(y_test, dt_predict, average='macro')

    # Calculate p-value for the F-scores
    def calculate_p_value(f1_score, y_test, X_test):
        dfn = y_test.shape[0] - 1
        dfd = X_test.shape[1]
        f_value = (f1_score * (dfn - 1)) / ((1 - f1_score) * dfd)
        p_value = 1 - f_distribution.cdf(f_value, dfn, dfd)
        return p_value

    p_value_lr = calculate_p_value(lr_f1, y_test, X_test)
    p_value_rf = calculate_p_value(rf_f1, y_test, X_test)
    p_value_svm = calculate_p_value(svm_f1, y_test, X_test)
    p_value_dt = calculate_p_value(dt_f1, y_test, X_test)

    return {
        "Logistic Regression F-score": lr_f1,
        "Random Forest F-score": rf_f1,
        "SVM F-score": svm_f1,
        "Decision Tree F-score": dt_f1,
        "Logistic Regression F-score p-value": p_value_lr,
        "Random Forest F-score p-value": p_value_rf,
        "SVM F-score p-value": p_value_svm,
        "Decision Tree F-score p-value": p_value_dt
    }

X_ff = data.drop(columns=['accident'])
Y_ll = data['accident'] #.values.reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X_ff,Y_ll, test_size = 0.3, random_state = 20)
X_train = X_train.drop('geometry', axis=1)
X_test = X_test.drop('geometry', axis=1)



# Train Logistic Regression model
LR = LogisticRegression()
LR.fit(X_train, y_train)
LRPredict = LR.predict(X_test)

# Train Random Forest model
RF = RandomForestClassifier()
RF.fit(X_train, y_train)
rf_predict = RF.predict(X_test)

# Train SVM model
svm_model = SVC()
svm_model.fit(X_train, y_train)
svm_predict = svm_model.predict(X_test)

# Train Decision Tree model
dt_model = DecisionTreeClassifier()
dt_model.fit(X_train, y_train)
dt_predict = dt_model.predict(X_test)

# Calculate F1 scores and p-values
results = calculate_f1_and_p_values(y_test, LRPredict, rf_predict, svm_predict, dt_predict, X_test)

# Print the results
for key, value in results.items():
    print(f"{key}: {value}")

# Save the Logistic Regression model
joblib.dump(LR, "rta_model_deploy3.joblib", compress=9)

# Optionally, save other models
joblib.dump(RF, "rf_model_deploy3.joblib", compress=9)
joblib.dump(svm_model, "svm_model_deploy3.joblib", compress=9)
joblib.dump(dt_model, "dt_model_deploy3.joblib", compress=9)
data.to_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/predection/data.gpkg")
print(data.info())