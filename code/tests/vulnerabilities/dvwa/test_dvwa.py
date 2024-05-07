from playwright.sync_api import Page
from pytest import fixture, mark

from tests.generate.test_login import get_login_test_cases
from tests.vulnerabilities.conftest import VulnerableApp


class DVWA(VulnerableApp):
    def __init__(self, page: Page):
        self.page = page

    def login(self, username: str, password: str) -> bool:
        self.page.goto("http://localhost:4280/login.php")
        self.page.locator('input[name="username"]').fill(username)
        self.page.locator('input[name="password"]').fill(password)
        self.page.get_by_role("button", name="Login").click()
        if self.page.get_by_text("Login failed").is_visible():
            return False
        if self.page.get_by_text(
            "Welcome to Damn Vulnerable Web Application"
        ).is_visible():
            return True
        raise Exception("Unknown state")


@fixture
def app(page) -> VulnerableApp:
    return DVWA(page)


params = get_login_test_cases("admin", "password")
params = [(x["username"], x["password"]) for x in params]
if (x := ("admin", "password")) not in params:
    params.append(x)


@mark.parametrize("username,password", params)
def test_dvwa(app, username, password):
    if username == "admin" and password == "password":
        assert app.login(username, password)
    else:
        assert not app.login(username, password)
