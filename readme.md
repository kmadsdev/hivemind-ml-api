# HiveMind - Machine Learning API on AWS
API for the HiveMind's Machine Learning repository -> [/kmadsdev/hivemind-ml](https://kmadsdev/hivemind-ml/).

### Stack
- Language: Python
- Frameworks/Tools: FastAPI, Uvicorn
- Host: AWS (EC2 + S3)

## Cloud configuration for the API:
### Step 1 - Set up S3: 
Upload the [latest machine learning model file](https://drive.google.com/file/d/1EzA-nuICumjeDTXCCW3rhzpE0Ic3YSzi/view?usp=sharing) to a Bucket on S3  

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

---

### Usage:
Url: ```http://<your-ec2-public-host>:8000/predict?inputs='<inputs-here>'```  
- Note: inputs must be separated by commas (",") only, in the python's ```string``` format
  
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
