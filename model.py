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


data = gpd.read_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/Model/combined_data_encoding.gpkg")

def ClassifMethod(method,X_train, X_test, y_train, y_test):
    #X_train, X_test, y_train, y_test = train_test_split(X_f,Y_l, test_size = 0.3, random_state = 42)
    match method:
        case "LR":
            LR =LogisticRegression(random_state=15, solver='lbfgs', multi_class='multinomial', max_iter=5000).fit(X_train, y_train)
            return LR
        

def calculate_vif(data):
  vif=pd.DataFrame()
  vif["features"]= data.columns
  vif["VIF_Value"] =[variance_inflation_factor(data.values, i) for i in range(data.shape[1])]

  return(vif)

def train_and_evaluate_random_forest(X_train, y_train, X_test, y_test):
    # Create a RandomForestClassifier model
    model = RandomForestClassifier(n_estimators=100, random_state=0)
    
    # Train the model on the training data
    model.fit(X_train, y_train)
    
    # Evaluate the model on the test data
    score = model.score(X_test, y_test)
    
    return score



class ClassifMethod:
    def __init__(self, method, X_train, X_test, y_train, y_test):
        if method == "LR":
            self.model = LogisticRegression()
            self.model.fit(X_train, y_train)
        # Add other classifiers if needed

    def score(self, X_test, y_test):
        return self.model.score(X_test, y_test)

    @property
    def intercept_(self):
        return self.model.intercept_

    @property
    def coef_(self):
        return self.model.coef_

    def predict(self, X_test):
        return self.model.predict(X_test)

def calculate_metrics_and_confusion_matrix(method, X_train, X_test, y_train, y_test):
    classifier = ClassifMethod(method, X_train, X_test, y_train, y_test)
    score = round(classifier.score(X_test, y_test), 6)
    print(f"{method} score: {score * 100}")
    print(f"intercept {method}: {classifier.intercept_}")
    print(f"coef {method}: {classifier.coef_}")
    predicted_values = classifier.predict(X_test)
    cnf_matrix = confusion_matrix(y_test, predicted_values)
    return cnf_matrix

def ClassifMethod(method,X_train, X_test, y_train, y_test):
    #X_train, X_test, y_train, y_test = train_test_split(X_f,Y_l, test_size = 0.3, random_state = 42)
    match method:
        case "LR":
            LR =LogisticRegression(random_state=15, solver='lbfgs', multi_class='multinomial', max_iter=5000).fit(X_train, y_train)
            return LR
        case "RF":
            RF=RandomForestClassifier(n_estimators=100, random_state=0).fit(X_train, y_train)
            return RF

def train_and_evaluate_svm(X_train, y_train, X_test, y_test):
    # Create an SVC model
    model = SVC()
    
    # Train the model on the training data
    model.fit(X_train, y_train)
    
    # Evaluate the model on the test data
    score = model.score(X_test, y_test)
    
    return score

def train_and_evaluate_decision_tree(X_train, y_train, X_test, y_test):
    # Create a DecisionTreeClassifier model
    model = DecisionTreeClassifier(random_state=0)
    
    # Train the model on the training data
    model.fit(X_train, y_train)
    
    # Evaluate the model on the test data
    score = model.score(X_test, y_test)
    
    return score

def train_random_forest(X_train, y_train):
    # Create a RandomForestClassifier model
    model = RandomForestClassifier()
    model1 = DecisionTreeClassifier()
    # Train the model with training data
    model.fit(X_train, y_train)
    model1.fit(X_train, y_train)
    return model

def important_factors(model, feature_names):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    # Display the importance of factors
    print("Importance of Factors:")
    for i in range(len(indices)):
        print(f"{feature_names[indices[i]]}: {importances[indices[i]]}")

    # Visualize the importance of factors
    plt.figure(figsize=(25, 8))
    plt.title("Importance of Factors")
    plt.bar(range(len(indices)), importances[indices], align="center")
    plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45)
    plt.show()


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

features = data.iloc[:,:-1]
print(calculate_vif(features))
data.drop(columns=['Area', 'Population','meteo_C','etat_route_PM','type_route_RN'], inplace=True)

X_f = data.drop(columns=['accident'])
Y_l = data['accident'] #.values.reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X_f,Y_l, test_size = 0.3, random_state = 20)
X_train = X_train.drop('geometry', axis=1)
X_test = X_test.drop('geometry', axis=1)

# Assuming X_train, y_train, X_test, y_test are defined elsewhere
conf_matrix = calculate_metrics_and_confusion_matrix("LR", X_train, X_test, y_train, y_test)
print("Confusion Matrix:")
print(conf_matrix)

# Assuming X_train, y_train, X_test, y_test are defined elsewhere
random_forest_score = train_and_evaluate_random_forest(X_train, y_train, X_test, y_test)
print(f"RandomForestClassifier score: {random_forest_score * 100:.6f}")

RF=ClassifMethod("RF", X_train, X_test, y_train, y_test)
rf=round(RF.score(X_test,y_test), 6)
print("Random Forest regression score",rf*100)

# Assuming X_train, y_train, X_test, y_test are defined elsewhere
svm_score = train_and_evaluate_svm(X_train, y_train, X_test, y_test)
print(f"SVM score: {svm_score * 100:.6f}")

# Assuming X_train, y_train, X_test, y_test are defined elsewhere
decision_tree_score = train_and_evaluate_decision_tree(X_train, y_train, X_test, y_test)
print(f"DecisionTreeClassifier score: {decision_tree_score * 100:.6f}")


# Assuming X_train, y_train, and X_f.columns (feature names) are defined elsewhere
model = train_random_forest(X_train, y_train)
important_factors(model, X_f.columns)
model1 = train_random_forest(X_train, y_train)
important_factors(model1, X_f.columns)

# Assuming X_train, y_train, X_test, y_test are defined elsewhere
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

results = calculate_f1_and_p_values(y_test, LRPredict, rf_predict, svm_predict, dt_predict, X_test)

# Print the results
for key, value in results.items():
    print(f"{key}: {value}")