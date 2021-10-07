import json
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud import bigquery_storage
from utils.helperutils import HelperUtils

class BiqQueryHelper:
  def __inti__(self, table_id = None, job_config = None):
    utils = HelperUtils()
    bigquery_config = utils.get_bigquery_config()
    bigquery_key = utils.get_bigquery_key()

    if bigquery_key != None:
      bigquery_credentials = json.loads(bigquery_key)
      self.credentials = service_account.Credentials.from_service_account_info(
          bigquery_credentials)
      self.client = bigquery.Client(
          credentials=self.credentials, project=bigquery_config['project_id'])
      self.storage_client = bigquery_storage.BigQueryReadClient(
          credentials=self.credentials)
    else:
      raise Exception('Environment variable `BIGQUERY_KEY` is not set.')

    self.table_id = table_id
    self.job_config = job_config

    def load_table(self, dataframe):
        self.job = self.client.load_table_from_dataframe(
            dataframe, self.table_id, job_config=self.job_config)
        self.job.result()
    
    def get_table(self):
        if (self.job != None and self.job.done()):
            return self.client.get_table(self.table_id)
        else:
            return None

    def get_dataframe_from_query(self, query):
        return self.client.query(query).result().to_dataframe(self.storage_client)

    def close_bigquery_client(self):
        self.client.close()