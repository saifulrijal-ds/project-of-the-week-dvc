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


### DVC Practice Workflow
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

## Day 2
- [ ] Create an ML project pipeline that contains a processing, training, and evaluation step. For dataset ideas check the first link in the suggested materials [1]. I would suggest using small datasets and light libraries (sklearn and datasets) remember, the goal is to explore/learn the tool.
- [ ] For ideas on how to split your ML pipeline, you can check the official example: [2]. I made also a simple ml pipeline with a random forest with iris data if you want to copy: [3]
- [ ] Create a params.yml that is going to store important parameters for the processing and training steps of your ML pipeline. Check these examples: Official example [4], mine more simple example [5]
- [ ] Push your changes to GitHub.
- [ ] Share your progress in Slack and on social media.