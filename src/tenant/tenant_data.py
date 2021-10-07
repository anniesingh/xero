

class TenantData:
  def __init__(self):
    self.tenants = []

  def add_tenant(self, raw_tenant):
    parsed_tenant = {
      "Tenant_ID":raw_tenant["tenantId"],
      "Tenant_Name":raw_tenant["tenantName"]
    }
    self.tenants.append(parsed_tenant)

  def get_tenants(self):
    return self.tenants