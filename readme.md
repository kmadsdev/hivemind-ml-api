# HiveMind - Machine Learning API on AWS
API for the HiveMind's Machine Learning repository -> [/kmadsdev/hivemind-ml](https://github.com/kmadsdev/hivemind-ml/).

### Stack
- Language: Python
- Frameworks/Tools: FastAPI, Uvicorn, Boto3
- Deploy: AWS (EC2 + S3)

### Dependencies
- FastAPI
- Boto3
- Uvicorn
- Pydantic
- Pathlib
- Datetime

## Pipeline - AWS configuration for the API:
### Step 1 - Set up S3: 
Upload the [latest machine learning model file](https://drive.google.com/file/d/1snga__dyYhn12j72pIBRPNwQVMXnYJj_/view?usp=sharing) to a Bucket on S3  

```Note: the default bucket name on the code is 'hivemind-ml-models', and can be changed on app.py by changing the BUCKET variable.```

### Step 2 - Set up EC2: 
- Application OS: Amazon Linux (Prefered)
    - Architecture: 64-bit Arm (Prefered)
- Intance type: t4g.small (or similar)
- Network settings / Check all these:
    - Allow SSH traffic from Anywhere (0.0.0.0:0)
    - Allow HTTP traffic from the internet
    - Allow HTTPS traffic from the internet

### Step 3 - Run app:  
- Inside EC2 (Amazon Linux)
    - Install python, pip and git: 'sudo yum install -y python pip git'
    - Install libs & requirements: 'pip install -r requirements.txt'
    - Clones git repository: 'git clone <repository link>'
    - Check for updates: 'git pull'
    - Run app 'python3 hivemind-ml-api/app.py'

<!-- Add step 4 -> tutorial on how to get the public host + set the port on EC2 -->

<!--
### step 4 - Setting up the host/endpoint
-->

---

## Usage:
Url: ```http://<ec2-public-host>:<ec2-port>/predict?inputs='<inputs-here>'```  
- Note: make sure you typed http, because it won't work if your try to use https  
- Inputs must be in the python's ```string``` format and be separated by commas (",") only  

Example: ```http://1337.101.404:8000/predict?inputs='200,450,1,0,1,1,0,1,0.72418,271.48123'```  

Input list:
<ol type="1">
    <li> &nbsp; int </li>
    <li> &nbsp; int </li>
    <li> &nbsp; int (0 or 1) </li>
    <li> &nbsp; int (0 or 1) </li>
    <li> &nbsp; int (0 or 1) </li>
    <li> &nbsp; int (0 or 1) </li>
    <li> &nbsp; int (0 or 1) </li>
    <li> &nbsp; int (0 or 1) </li>
    <li> &nbsp; float (between 0.00001 and 1)   </li>
    <li> &nbsp; float (between 0 and 999.99999) </li>
</ol>

## Update log
<div>
    <p>
        <h3> ●  &nbsp;  27 oct 2025  &nbsp; | &nbsp;  New Machine Learning Model File  &nbsp; | &nbsp;  <a 
            href="https://drive.google.com/file/d/1snga__dyYhn12j72pIBRPNwQVMXnYJj_/view?usp=sharing" style="text-decoration: none">< Go to file ></a>
        </h3>
        &nbsp; • &nbsp; Mode choosen: Logistic Regression <br>
        &nbsp; • &nbsp; Size: 1.2KB <br>
        &nbsp; • &nbsp; Accuracy: 97.94%
    </p>
    <p>
        <h3> ●  &nbsp;  23 oct 2025  &nbsp; | &nbsp;  New Machine Learning Model File  &nbsp; | &nbsp;  <a 
            href="https://drive.google.com/file/d/1_6TZ-_eiZw8-sx-nNc2-ykeS9aUogsVR/view?usp=sharing" style="text-decoration: none">< Go to file ></a>
        </h3>
        &nbsp; • &nbsp; Model choosen: Random Forest Classifier </strong> <br>
        &nbsp; • &nbsp; Size: 756.3MB <br>
        &nbsp; • &nbsp; Accuracy: 97.72%
    </p>
</div>
