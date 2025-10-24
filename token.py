import json
import os
import subprocess
import sys

CREDENTIAL_FILE = os.path.join(os.getenv("HOMEPATH"), ".aws", "sso", "cache")
ENV_FILE = os.path.join(os.getcwd(), ".env")
ENV_LIST = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"]
PAYLOAD = """{"aws_access_key_id": "$clientId", "aws_secret_access_key": "$clientSecret", "aws_session_token": "$accessToken", "region" : "$region"}"""

profile = sys.argv[1]


def _load_credentials_from_aws_file():
    json_credentials = {}
    for file_name in os.listdir(CREDENTIAL_FILE):
        with open(os.path.join(CREDENTIAL_FILE, file_name)) as file:
            json_credentials.update(json.load(file))

    return (
        PAYLOAD.replace("$clientId", json_credentials["clientId"])
        .replace("$clientSecret", json_credentials["clientSecret"])
        .replace("$accessToken", json_credentials["accessToken"])
        .replace("$region", json_credentials["region"])
    )


def _load_aws_config(key):
    return subprocess.check_output(
        args=f"aws configure get {key} --profile {profile}", shell=True, encoding="utf-8"
    ).rstrip()


def _process_aws_config(credentials):
    account_id = _load_aws_config("sso_account_id")
    role_name = _load_aws_config("sso_role_name")
    region = _load_aws_config("sso_region")

    output = subprocess.check_output(
        args=f"aws sso get-role-credentials --account-id {account_id} --role-name {role_name} --access-token {json.loads(credentials)['aws_session_token']} --region {region} --profile {profile}",
        shell=True,
    )
    return json.loads(output)["roleCredentials"]


def _write_env_file(credentials: dict):
    try:
        with open(ENV_FILE, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            for key in ENV_LIST:
                if line.startswith(key + "="):
                    if key == "AWS_ACCESS_KEY_ID":
                        lines[i] = f"{key}={credentials['accessKeyId']}\n"
                    if key == "AWS_SECRET_ACCESS_KEY":
                        lines[i] = f"{key}={credentials['secretAccessKey']}\n"
                    if key == "AWS_SESSION_TOKEN":
                        lines[i] = f"{key}={credentials['sessionToken']}\n"

        with open(ENV_FILE, "w") as file:
            file.writelines(lines)

        print("Token updated in .env file.")
    except Exception as err:
        print("Error when trying to update .env file:", err)


_write_env_file(_process_aws_config(_load_credentials_from_aws_file()))
