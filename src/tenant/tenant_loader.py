import requests
from utils.helperutils import HelperUtils

class TenantLoader:
  def __init__(self):
      utils = HelperUtils()
      self.xero_api_config = utils.get_xero_api_config()

  def get_tenant(self, access_token):
    request_url = f"{self.xero_api_config['host']}{self.xero_api_config['tenant_endpoint']}"
    headers = {
      "Authorization": access_token,
      "Content-Type": self.xero_api_config["context_type"]
    }
    response = requests.get(request_url, headers=headers)
    response_body =  response.json()
    return response_body