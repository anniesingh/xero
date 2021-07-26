from os import access
import urllib
import requests
import asyncio
import urllib.parse as urlparse
from pyppeteer import launch
from utils.helperutils import HelperUtils


class XeroAuthHelper:
    def __init__(self):
        utils = HelperUtils()
        self.xero_config = utils.get_xero_config()
        self.xero_username = utils.get_xero_username()
        self.xero_password = utils.get_xero_password()
        self.xero_client_id = utils.get_xero_client_id()
        self.xero_secret_auth_base64 = utils.get_xero_secret_auth_base64()
        self.access_token = None
        self.refresh_token = None
        self.expired_in = None
        self.token_type = None

    def get_base_url(self):
        return self.xero_config["base_url"]

    def get_headless_config(self):
        return self.xero_config["headless"]

    def get_xero_selectors(self):
        return self.xero_config["selectors"]

    def get_query_param_string(self):
        params = self.xero_config['params']
        params["client_id"] = self.xero_client_id

        def get_param_value(key):
            value = params[key]
            if (type(value) is list):
                return f"{key}={urllib.parse.quote(' '.join(value))}"
            else:
                return f"{key}={value}"

        return "&".join(map(get_param_value, params.keys()))

    def get_token_config(self):
        return self.xero_config["token"]

    async def get_xero_auth_context(self):
        browser = await launch(headless=self.get_headless_config())
        page = await browser.newPage()
        await page.setViewport({"width": 1600, "height": 1600})
        page_url = f"{self.get_base_url()}?{self.get_query_param_string()}"
        await page.goto(page_url, waitUntil="networkidle0")

        return {
            "browser": browser,
            "page": page
        }

    async def get_auth_code(self):
        auth_context = await self.get_xero_auth_context()
        auth_browser = auth_context["browser"]
        auth_page = auth_context["page"]

        selectors = self.get_xero_selectors()
        await auth_page.evaluate(f"""() => {{
            document.querySelector(
                '{selectors["user_name"]}').value = '{self.xero_username}';
        }}""")
        await auth_page.evaluate(f"""() => {{
            document.querySelector(
                '{selectors["password"]}').value = '{self.xero_password}';
        }}""")
        await asyncio.wait([
            auth_page.click(selectors["login"]),
            auth_page.waitForNavigation(),
        ])
        await auth_page.waitForSelector(selectors["approve"], {"visible": True})
        await asyncio.wait([
            auth_page.click(selectors["approve"]),
            auth_page.waitForNavigation(),
        ])
        url_parts = list(urlparse.urlparse(auth_page.url))
        await auth_browser.close()

        return dict(urlparse.parse_qsl(url_parts[4]))["code"]

    async def get_access_token_by_auth_code(self):
        auth_code = await self.get_auth_code()
        params = self.xero_config["params"]
        token_config = self.get_token_config()
        headers = {
            "authorization": self.xero_secret_auth_base64,
            "Content-Type": token_config["content_type"]
        }
        body = {
            "grant_type": token_config['init_grant_type'],
            "code": auth_code,
            "redirect_uri": params['redirect_uri']
        }

        rq = requests.post(
            token_config["token_url"], headers=headers, data=body)

        return rq.json()

    async def get_access_token_by_refresh_token(self, refresh_token):
        token_config = self.get_token_config()
        headers = {
            "authorization": self.xero_secret_auth_base64,
            "Content-Type": token_config["content_type"]
        }
        body = {
            "grant_type": token_config['refresh_grant_type'],
            "refresh_token": refresh_token
        }

        rq = requests.post(
            token_config["token_url"], headers=headers, data=body)

        return rq.json()

    async def get_access_token(self):
        pass


async def main():
    xero_helper = XeroAuthHelper()
    access_token = await xero_helper.get_access_token()


asyncio.get_event_loop().run_until_complete(main())
