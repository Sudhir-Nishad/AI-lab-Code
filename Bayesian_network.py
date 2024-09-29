import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import numpy as np
import pgmpy.models as pgm
from pgmpy.estimators import HillClimbSearch, BicScore, MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from sklearn.preprocessing import LabelEncoder

def load_data():
    data = [
        {'EC100': 'AA', 'IT101': 'AB', 'MA101': 'BB', 'PH100': 'CC', 'Internship': 'Yes'},
        {'EC100': 'DD', 'IT101': 'CC', 'MA101': 'BB', 'PH100': 'DD', 'Internship': 'No'},
        {'EC100': 'BB', 'IT101': 'AA', 'MA101': 'AB', 'PH100': 'AA', 'Internship': 'Yes'},
        {'EC100': 'CC', 'IT101': 'BB', 'MA101': 'AB', 'PH100': 'AB', 'Internship': 'Yes'},
        {'EC100': 'AB', 'IT101': 'DD', 'MA101': 'CC', 'PH100': 'BB', 'Internship': 'No'},
    ]
    return pd.DataFrame(data)

data = load_data()

label_encoder = LabelEncoder()
for col in data.columns[:-1]:
    data[col] = label_encoder.fit_transform(data[col])

def learn_bayesian_network(data):
    hc = HillClimbSearch(data)
    best_model = hc.estimate(scoring_method=BicScore(data))
    bayes_net = pgm.BayesianModel(best_model.edges())
    bayes_net.fit(data, estimator=MaximumLikelihoodEstimator)
    return bayes_net

bayesian_net = learn_bayesian_network(data)

def predict_ph100(bayesian_net, ec100, it101, ma101):
    inference = VariableElimination(bayesian_net)
    query = inference.query(variables=['PH100'], evidence={'EC100': ec100, 'IT101': it101, 'MA101': ma101})
    return query

encoded_evidence = {
    'EC100': label_encoder.transform(['DD'])[0],
    'IT101': label_encoder.transform(['CC'])[0],
    'MA101': label_encoder.transform(['CD'])[0]
}
prediction = predict_ph100(bayesian_net, **encoded_evidence)
print("Prediction for PH100 grade:", prediction)

def naive_bayes_classifier(data, n_repeats=20):
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    
    accuracies = []
    for _ in range(n_repeats):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=np.random.randint(0, 1000))
        nb_model = GaussianNB()
        nb_model.fit(X_train, y_train)
        y_pred = nb_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        accuracies.append(accuracy)
    
    return np.mean(accuracies)

independent_accuracy = naive_bayes_classifier(data)
print(f"Naive Bayes (independent) average accuracy over 20 runs: {independent_accuracy:.2f}")

def bayesian_naive_bayes_classifier(bayesian_net, data, n_repeats=20):
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    
    accuracies = []
    inference = VariableElimination(bayesian_net)
    
    for _ in range(n_repeats):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=np.random.randint(0, 1000))
        y_pred = []
        for i in range(len(X_test)):
            evidence = dict(X_test.iloc[i].to_dict())
            result = inference.map_query(variables=[y.name], evidence=evidence)
            y_pred.append(result[y.name])
        accuracy = accuracy_score(y_test, y_pred)
        accuracies.append(accuracy)
    
    return np.mean(accuracies)

dependent_accuracy = bayesian_naive_bayes_classifier(bayesian_net, data)
print(f"Naive Bayes (dependent) average accuracy over 20 runs: {dependent_accuracy:.2f}")
