import os
import yaml as yml
import base64


class HelperUtils:
    def __init__(self):
        self.config_file = "/home/ananya/Code/xero/src/config.yml"

    def get_xero_config(self):
        with open(self.config_file, "r") as f:
            return yml.safe_load(f)['xero']

    def get_xero_username(self):
        return os.environ.get("XERO_USERNAME", None)

    def get_xero_password(self):
        return os.environ.get("XERO_PASSWORD", None)

    def get_xero_client_id(self):
        return os.environ.get("XERO_CLIENT_ID", None)

    def get_xero_client_secret(self):
        return os.environ.get("XERO_CLIENT_SECRET", None)

    def get_xero_secret_auth_base64(self):
        auth_base64 = base64.b64encode(
            f"{self.get_xero_client_id()}:{self.get_xero_client_secret()}".encode("ascii"))
        return f"Basic {auth_base64.decode('ascii')}"
    
    def get_bigquery_config(self):
        with open(self.config_file, "r") as f:
            return yml.safe_load(f)["big_query"]

    def get_bigquery_key(self):
        return os.environ.get("LOCAL_BIGQUERY_KEY", None)
    
    def get_xero_api_config(self):
        with open(self.config_file, "r") as f:
            return yml.safe_load(f)["xero_api"]

    def get_logging_config(self):
        with open(self.config_file, "r") as f:
            return yml.safe_load(f)['enable_logging']

    # def get_request_url(self, api, access_token, accept, tenant_id):
    #     return f"GET{api}"