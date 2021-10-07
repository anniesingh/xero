import pandas as pd
import time
import math

from google.cloud import bigquery

from bigquery_helper import BiqQueryHelper
from utils.helperutils import HelperUtils

from tenant.tenant_loader import TenantLoader
from tenant.tenant_data import TenantData


def get_tenant_dataframe(access_token):
  tenant_loader = TenantLoader()
  tenant_data = TenantData()
  raw_tenants = tenant_loader.get_tenant(access_token)

  for raw_tenant in raw_tenants:
    tenant_data.add_tenant(raw_tenant)

  return pd.DataFrame(tenant_data.get_tenants())

def load_tenant_dataframe(bq_config, dataframe):
    bq_helper = BiqQueryHelper(bq_config["tenant_table_id"], bigquery.LoadJobConfig(
        write_disposition=bq_config["tenant_write_deposition"]))

    bq_helper.load_table(dataframe)
    table = bq_helper.get_table()
    print(
        f"Tenant => Loaded {table.num_rows} rows with {len(table.schema)} columns to {bq_helper.table_id}"
    )
    bq_helper.close_client()

    
def tenant_init(access_token):
    utils = HelperUtils()
    bq_config = utils.get_bigquery_config()
    start_time = time.time()
    # Load Tenant dataframe into BigQuery
    print("Tenant import and load started")
    tenant_dataframe = get_tenant_dataframe(access_token)
    load_tenant_dataframe(bq_config, tenant_dataframe)
    

    print(f"Tenant => Completed in {math.ceil(time() - start_time)} seconds")
