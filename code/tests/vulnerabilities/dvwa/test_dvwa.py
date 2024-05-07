from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from pytest import fixture, mark

from tests.utils import wait_for_logs
from tests.vulnerabilities.conftest import VulnerableApp, get_params


class DVWA(VulnerableApp):
    def init(self) -> None:
        fails = 1
        while True:
            self.page.goto("http://localhost:4280/login.php")
            try:
                self.page.wait_for_selector("input[name=Login]", timeout=500)
                break
            except PlaywrightTimeoutError:
                fails += 1
            if fails > 10:
                raise PlaywrightTimeoutError("Failed to load DVWA")
        self.page.get_by_role("button", name="Login").click()
        self.page.get_by_role("button", name="Create / Reset Database").click()

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


@fixture(scope="module")
def wait_for_compose(compose):
    wait_for_logs(compose, r"AH00094: Command line: 'apache2 -D FOREGROUND'")
    wait_for_logs(compose, r"mariadbd: ready for connections.")


@fixture(scope="module")
def app_class(wait_for_compose):
    return DVWA


@mark.parametrize("username,password", get_params())
def test_login(app, username, password):
    if username == "admin" and password == "password":
        assert app.login(username, password)
    else:
        assert not app.login(username, password)
