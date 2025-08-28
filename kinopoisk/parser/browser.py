from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent


class BrowserPlaywright:
    def __init__(self, visible=False):
        self.visible = visible
        self.headless = False if self.visible else True # visible Ui interface
        self.playwright = None
        self.browser = None
        self.context = None

    def create_browser(self, headers: dict):
        if not self.playwright:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=self.headless)
            self.context = self.browser.new_context(**headers)

    def create_page(self):
        return self.context.new_page()

    @staticmethod
    def open_url(page: object, link: str, wait_until="load", timeout=20000):
        return page.goto(link, wait_until=wait_until, timeout=timeout)

    def close(self):
        self.browser.close()
        self.playwright.stop()

    @staticmethod
    def get_user_agent() -> dict:
        """Получение рандомный User-Agent"""
        return {'user_agent': UserAgent().random}
