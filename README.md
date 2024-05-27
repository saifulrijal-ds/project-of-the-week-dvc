# Project of the Week: DVC
## Overview
This repository documents my progress following the Project of the Week by DataTalksClub, focusing on Data Version Control (DVC).

Project Guideline Link: [#project-of-the-week](https://github.com/DataTalksClub/project-of-the-week/blob/main/2024-05-22-DVC.md)

### Why DVC?
DVC helps data scientists adopt best practices for organizing their projects and collaborating effectively by:
- Tracking and saving data and ML models similarly to code.
- Creating and switching between versions of data and ML models effortlessly.
- Understanding how datasets and ML artifacts were initially built.
- Comparing model metrics among experiments.
- Adopting engineering tools and best practices in data science projects.

## Day 1: Preparation
### Tasks Completed
- [x] Create a GitHub repository
    - Repository: [project-of-the-week-dvc](https://github.com/saifulrijal-ds/project-of-the-week-dvc)
- [x] Install DVC in your own OS with [2], I work on Ubuntu.
    - Prerequisite: Git must be installed.
    ```bash
    git --version
    # git version 2.43.0
    ```
    To install Git:
    ```bash
    sudo apt-get install git
    ```
    - Create Conda environment and install DVC:
    ```bash
    conda create --name dvc_env
    conda activate dvc_env
    conda install -c conda-forge dvc
    ```
    - Install additional storage plugins:
    ```bash
    conda install -c conda-forge dvc-s3 dvc-oss
    ```
    - Verify DVC installation:
    ```bash
    dvc --version
    # 3.50.2
    ```
- [x] Understand and run Data version control capabilities (with custom data for example txt or csv) check out [1] and [3]. Friendly reminder: DVC is not just a version control tool it also contains experimentation, pipelines, and more.

- [x] Share your progress in Slack and on social media.


### DVC Command Practice
#### Step-by-Step Guide
1. Create a sample data file (`data/data.txt`):
    ```text
    First version of data
    ```

2. Initialize DVC:
    ```bash
    dvc init
    ```
    The command will create `.dvc` folder and `.dvcignore`.

3. Add data file to DVC tracking:
    ```bash
    dvc add data/data.txt
    ```
    DVC performs the following action:
    - Adds the `data/data.txt` path to `data/.gitignore` to ensure that the data file is not tracked by Git but by DVC instead.
    - Generates a `.dvc` file (e.g., `data/data.txt.dvc`), which contains metadata about the data file such as its MD5 hash, size, and relative path.
    - Stores a copy of the data file in the DVC cache located in the `.dvc/cache directory`. This cached file serves as a reference and is identified by a hash value derived from the file’s content, rather than creating a duplicate of the original file.

4. Modify the data file:
    ```text
    First version of data. (modified)
    ```
    - Add the changed file:
        ```bash
        dvc add data/data.txt
        ```
5. Commit changes to Git:
    ```bash
    git add .
    git commit -m "Updated data.txt with modifications"
    ```
6. Further modify the data file:
    ```text
    First version of data. (modified)
    Second edition
    ```
    - Add the modified file:
        ```bash
        dvc add data/data.txt
        ```
    - Commit changes:
        ```bash
        git add .
        git commit -m "Added second edition to data.txt"
        ```
7. Rollback data changes:
    - Find the previous commit ID:
        ```bash
        git log
        ```
    - Checkout the desired commit:
        ```bash
        git checkout {commit_id}
        ```
    - Restore the data:
        ```bash
        dvc checkout
        ```
8. Return to the main branch:
    ```bash
    git checkout main
    dvc checkout
    ```
### Using AWS S3 as Remote Storage for DVC
#### Configuration Steps

1. Install `awscli`:
    ```bash
    conda install conda-forge::awscli
    ```

2. Configure AWS profile:
    ```bash
    aws configure --profile dvc-s3-profile
    ```

3. Add S3 remote storage:
    ```bash
    dvc remote add -d myremote s3://saiful-dvc-remote-bucket/project-of-the-week-dvc/
    ```
4. Modify the remote to use the AWS profile:
    ```bash
    dvc remote modify myremote --local profile dvc-s3-profile
    ```
    Note: The --local flag ensures this configuration is not tracked by Git.
5. Verify the setup:
    - Add a new data file (data/bank-marketing.csv) and track with DVC:
        ```bash
        dvc add data/bank-marketing.csv
        ```
    - Commit the changes:
        ```bash
        git add .
        git commit -m "Added bank-marketing.csv and tracked with DVC"
        ```
    - Push DVC cache to remote:
        ```bash
        dvc push
        ```
    - Check the S3 bucket for the uploaded data.

## Day 2: Prepare ML Project
- [x] Create an ML project pipeline that contains a processing, training, and evaluation step. For dataset ideas check the first link in the suggested materials [1]. I would suggest using small datasets and light libraries (sklearn and datasets) remember, the goal is to explore/learn the tool.
- [x] For ideas on how to split your ML pipeline, you can check the official example: [2]. I made also a simple ml pipeline with a random forest with iris data if you want to copy: [3]
- [x] Create a params.yml that is going to store important parameters for the processing and training steps of your ML pipeline. Check these examples: Official example [4], mine more simple example [5]
- [x] Push your changes to GitHub.
- [x] Share your progress in Slack and on social media.

The machine learning project involves binary classification using the [Bank Marketing dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing). I use a RandomForest classifier with all features and applying CatBoostEncoder for categorical data transformation.  
In the `params.yaml` configuration file, we discovered a parameter called `drop_columns`. In this use case, we’ll explore how adjusting the number of features used for training the model impacts its performance. By selectively dropping certain columns, we can fine-tune our feature set and optimize the model’s predictive capabilities.

## Day 3: Practice with DVC Command
- [x]  Finish preparing your own project if you haven’t from the previous day
- [x]  Perform a version of your dataset with DVC: [1],[2]
- [x]  For configuring the storage you can check [3]. In case you don’t want to spend time setting a remote storage, you can also use a local folder.
- [x]  Play with dvc commands `dvc status`,`dvc add`, `dvc push`, `dvc checkout` (also with your git commands)
- [x]  Push your changes to GitHub.
- [x]  Share your progress in Slack and on social media.

## Day 4: DVC Pipeline
- [x]  Try to build pipelines based on the official documentation [1]
- [x]  You can follow the official video tutorial [2]. The video is from 3 years ago and some commands might have changed so make sure you use [1] docs in parallel.
- [ ]  Check out the summary in [3] to understand what this DVC feature solves.
- [x]  Push your changes to GitHub.
- [x]  Share your progress in Slack and on social media.

### DVC Pipeline Practice
Git add and commit files created on Day 2 (You can find in `src/`)
```bash
git add params.yaml src/
git commit -m 'add ml sample project'
```

Create stages, in my case there are 3 stages:
- prepare
- train, and
- evaluate

prepare stage:
```bash
dvc stage add -n prepare -d src/prepare.py -d data/bank-marketing.csv -o data/preprocessed/ python src/prepare.py
```
train stage:
```bash
dvc stage add -n train -d src/train.py -d data/preprocessed/ -o models/ python src/train.py
```
evaluate stage:
```bash
dvc stage add -n evaluate -d src/evaluate.py -d data/preprocessed/ -d models/ -o metrics/ python src/evaluate.py
```
the commands above will create `dvc.yaml`, Git add and commit it
```bash
git add dvc.yaml .gitignore data/.gitignore 
git commit -m 'pipeline defined'
```

We can run our pipeline with
```bash
dvc repro
```
with the output
```text
'data/bank-marketing.csv.dvc' didn't change, skipping                                                                                                           
Running stage 'prepare':                                                                                                                                        
> python src/prepare.py
Directory created: data/preprocessed/
Data saved to: data/preprocessed/
Train shape: (28831, 21)
Test shape: (12357, 21)
Generating lock file 'dvc.lock'                                                                                                                                 
Updating lock file 'dvc.lock'                                                                                                                                   

Running stage 'train':                                                                                                                                          
> python src/train.py
['job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week', 'poutcome']
['age', 'duration', 'campaign', 'pdays', 'previous', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']
Pipeline(steps=[('preprocessor',
                 ColumnTransformer(transformers=[('cat',
                                                  Pipeline(steps=[('catboost_encoder',
                                                                   CatBoostEncoder(verbose=False))]),
                                                  ['job', 'marital',
                                                   'education', 'default',
                                                   'housing', 'loan', 'contact',
                                                   'month', 'day_of_week',
                                                   'poutcome']),
                                                 ('num', 'passthrough',
                                                  ['age', 'duration',
                                                   'campaign', 'pdays',
                                                   'previous', 'emp.var.rate',
                                                   'cons.price.idx',
                                                   'cons.conf.idx', 'euribor3m',
                                                   'nr.employed'])])),
                ('model',
                 RandomForestClassifier(max_depth=5, random_state=20240524))])
Directory created: models/
Model saved to: models/model.joblib
Label encoder saved to: models/label_encoder.joblib
Updating lock file 'dvc.lock'                                                                                                                                   
                                                                                                                                                                
Running stage 'evaluate':                                                                                                                                       
> python src/evaluate.py
Accuracy: 0.902889050740471
F1 Score: 0.8777650289010959
Recall: 0.902889050740471
Precision: 0.8909718045361412
ROC AUC: 0.6026729366864307
[[10856    94]
 [ 1106   301]]


              precision    recall  f1-score   support

           0       0.91      0.99      0.95     10950
           1       0.76      0.21      0.33      1407

    accuracy                           0.90     12357
   macro avg       0.83      0.60      0.64     12357
weighted avg       0.89      0.90      0.88     12357

ERROR: failed to reproduce 'evaluate': output 'metrics' does not exist 
```
In this case, it give an error because my `evaluate.py` has no action to create `metrics` directory that I define as output of evaluate stage.

After try add some code to save metrics to `metrics/metrics.txt` and run `dvc repro`. It give the output
```text
'data/bank-marketing.csv.dvc' didn't change, skipping                                                                                                           
Stage 'prepare' didn't change, skipping                                                                                                                         
Stage 'train' didn't change, skipping                                                                                                                           
Running stage 'evaluate':                                                                                                                                       
> python src/evaluate.py
Accuracy: 0.902889050740471
F1 Score: 0.8777650289010959
Recall: 0.902889050740471
Precision: 0.8909718045361412
ROC AUC: 0.6026729366864307
[[10856    94]
 [ 1106   301]]


              precision    recall  f1-score   support

           0       0.91      0.99      0.95     10950
           1       0.76      0.21      0.33      1407

    accuracy                           0.90     12357
   macro avg       0.83      0.60      0.64     12357
weighted avg       0.89      0.90      0.88     12357

Directory created: metrics/
Metrics saved to metrics/metrics.txt
Updating lock file 'dvc.lock'                                                                                                                                   
                                                                                                                                                                
To track the changes with git, run:

        git add dvc.lock

To enable auto staging, run:

        dvc config core.autostage true
Use `dvc push` to send your updates to remote storage.
```

We can show the pipline dag with
```bash
dvc dag

+-----------------------------+  
| data/bank-marketing.csv.dvc |  
+-----------------------------+  
                *                
                *                
                *                
          +---------+            
          | prepare |            
          +---------+            
          **        **           
        **            *          
       *               **        
 +-------+               *       
 | train |             **        
 +-------+            *          
          **        **           
            **    **             
              *  *               
          +----------+           
          | evaluate |           
          +----------+           
+-------------------+  
| data/data.txt.dvc |  
+-------------------+  
```
_I don't know why `data/data.txt.dvc` appears in the dag, I don't think I included it in any stage_.
And don't forget to check the Git and DVC status.
```bash
dvc status

# Data and pipelines are up to date.
```