import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from category_encoders.cat_boost import CatBoostEncoder
import os
import yaml
import joblib

def train_model():
    # Load parameters
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)

    seed = params['train']['seed']
    train_test_dir = params['train']['train_test_dir']
    train_file = params['train']['train_file']
    target_column = params['train']['target_column']
    rf_parameters = params['train']['rf_parameters']
    model_artifacts_dir = params['train']['model_artifacts_dir']
    
    train_data_path = os.path.join(train_test_dir, train_file)
    train_df = pd.read_csv(train_data_path)

    X = train_df.drop(columns=target_column, axis=1)
    y = train_df[target_column]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    cat_columns = X.select_dtypes(include=['object', 'category']).columns.to_list()
    num_columns = X.select_dtypes(exclude=['object', 'category']).columns.to_list()
    print(cat_columns)
    print(num_columns)

    categorical_transformer = Pipeline(steps=[
        ('catboost_encoder', CatBoostEncoder(verbose=False))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('cat', categorical_transformer, cat_columns),
        ('num', 'passthrough', num_columns)
    ])

    model = RandomForestClassifier(n_estimators=rf_parameters['n_estimators'],
                                   max_depth=rf_parameters['max_depth'],
                                   min_samples_leaf=rf_parameters['min_samples_leaf'],
                                   min_samples_split=rf_parameters['min_samples_split'],
                                   random_state=seed)
    
    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                            ('model', model)])

    model_pipeline.fit(X, y_encoded)
    print(model_pipeline)

    if not os.path.exists(model_artifacts_dir):
        os.makedirs(model_artifacts_dir)
        print('Directory created:', model_artifacts_dir)
    else:
        print('Directory already exists:', model_artifacts_dir)

    joblib.dump(model_pipeline, os.path.join(model_artifacts_dir, 'model.joblib'))
    joblib.dump(label_encoder, os.path.join(model_artifacts_dir, 'label_encoder.joblib'))

    print('Model saved to:', os.path.join(model_artifacts_dir, 'model.joblib'))
    print('Label encoder saved to:', os.path.join(model_artifacts_dir, 'label_encoder.joblib'))

if __name__ == '__main__':
    train_model()
