import pandas as pd
from sklearn.model_selection import train_test_split 
import yaml
import os

def load_and_preprocess():
    with open('params.yaml') as f:
        params = yaml.safe_load(f)

    # Accessing the parameters
    test_split = params['prepare']['test_size']
    seed = params['prepare']['seed']
    data_path = params['prepare']['data_source']
    train_test_path = params['prepare']['train_test_dir']
    drop_columns = params['prepare']['drop_columns']

    # Reading the data
    df = pd.read_csv(data_path, sep=';')

    # Drop column(s) if needed
    if drop_columns:
        df = df.drop(columns=drop_columns)

    # Splitting the data
    train_df, test_df = train_test_split(df, test_size=test_split, random_state=seed)
    
    # Checking if directory already exist
    if not os.path.exists(train_test_path):
        os.makedirs(train_test_path)
        print('Directory created:', train_test_path)
    else:
        print('Directory already exists:', train_test_path)
    
    # Saving the data
    train_df.to_csv(os.path.join(train_test_path, 'train.csv'), index=False)
    test_df.to_csv(os.path.join(train_test_path, 'test.csv'), index=False)

    print('Data saved to:', train_test_path)
    print('Train shape:', train_df.shape)
    print('Test shape:', test_df.shape)

if __name__ == '__main__':
    load_and_preprocess()
