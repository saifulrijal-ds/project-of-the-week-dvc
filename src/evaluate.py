from sklearn.metrics import (confusion_matrix,
                             classification_report,
                             accuracy_score,
                             f1_score,
                             recall_score,
                             precision_score,
                             roc_auc_score)

import joblib
import yaml
import os
import pandas as pd

def evaluate_model():
    with open('params.yaml') as f:
        params = yaml.safe_load(f)

    train_test_dir = params['evaluate']['train_test_dir']
    train_file = params['evaluate']['train_file']
    test_file = params['evaluate']['test_file']
    target_column = params['evaluate']['target_column']
    model_artifacts_dir = params['evaluate']['model_artifacts_dir']
    model_file = params['evaluate']['model_file']
    label_encoder_file = params['evaluate']['label_encoder_file']
    metrics_dir = params['evaluate']['metrics_dir']
    
    # Loading the model
    model = joblib.load(os.path.join(model_artifacts_dir, model_file))

    # Loading the label encoder
    label_encoder = joblib.load(os.path.join(model_artifacts_dir, label_encoder_file))

    # Loading the test data
    test_data_path = os.path.join(train_test_dir, test_file)
    test_df = pd.read_csv(test_data_path)
    X_test = test_df.drop(target_column, axis=1)
    y_test = test_df[target_column]
    y_test_encoded = label_encoder.transform(y_test)

    # Making predictions on the test data
    y_pred = model.predict(X_test)

    # Evaluating the model
    accuracy = accuracy_score(y_test_encoded, y_pred)
    f1 = f1_score(y_test_encoded, y_pred, average='weighted')
    recall = recall_score(y_test_encoded, y_pred, average='weighted')
    precision = precision_score(y_test_encoded, y_pred, average='weighted')
    roc_auc = roc_auc_score(y_test_encoded, y_pred, average='weighted')
    print(f"Accuracy: {accuracy}")
    print(f"F1 Score: {f1}")
    print(f"Recall: {recall}")
    print(f"Precision: {precision}")
    print(f"ROC AUC: {roc_auc}")

    # Confusion matrix
    cm = confusion_matrix(y_test_encoded, y_pred)
    print(cm)
    print("\n")
    print(classification_report(y_test_encoded, y_pred))

if __name__ == '__main__':
    evaluate_model()
