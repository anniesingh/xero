import asyncio
from auth_helper import AuthHelper
from tenant_df_loader import tenant_init



async def main():
  xero_helper = AuthHelper()
  access_token = await xero_helper.get_access_token()
  tenant_init(access_token)

  
  
if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())

