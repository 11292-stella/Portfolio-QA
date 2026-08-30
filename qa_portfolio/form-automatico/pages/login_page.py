from playwright.sync_api import Page
from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.campo_username = page.get_by_label("Username")
        self.campo_password = page.get_by_label("Password")
        self.btn_entra = page.get_by_role("button", name="Entra")

    def vai_a_login(self, base_url: str):
        self.page.goto(f"{base_url}/accounts/login/")

    def login(self, username: str, password: str):
        self.campo_username.fill(username)
        self.campo_password.fill(password)
        self.btn_entra.click()
        self.page.wait_for_load_state("networkidle")