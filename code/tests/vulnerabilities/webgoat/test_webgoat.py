from playwright.sync_api import Page
from pytest import fixture, mark

from tests.utils import wait_for_logs
from tests.vulnerabilities.conftest import VulnerableApp, _test_app, get_params

BASE_URL = "http://localhost:4281/WebGoat"


class WebGoat(VulnerableApp):
    def __init__(self, page: Page):
        super().__init__(page)

    def init(self) -> None:
        self.page.goto(BASE_URL, timeout=5000)
        self.page.get_by_role("link", name="or register yourself as a new").click()
        self.page.get_by_placeholder("Username").fill("adminadmin")
        self.page.get_by_label("Password", exact=True).fill("password")
        self.page.get_by_label("Confirm password").fill("password")
        self.page.get_by_label("Agree with the terms and").check()
        self.page.get_by_role("button", name="Sign up").click()
        self.page.wait_for_selector("text=Introducing WebWolf", timeout=6000)
        assert self.page.get_by_role("heading", name="Introducing WebWolf").is_visible()

    def login(self, username, password) -> bool:
        self.page.goto(
            BASE_URL + "/start.mvc?username=adminadmin#lesson/LogSpoofing.lesson/1"
        )
        self.page.get_by_role("textbox", name="username").fill(username)
        self.page.get_by_role("textbox", name="password").fill(password)
        self.page.get_by_role("button", name="Submit").click()
        self.page.get_by_text(f"Login failed for username: {username}").is_visible()
        return False


@fixture(scope="module")
def wait_for_compose(compose):
    return wait_for_logs(compose, r"Please browse to (.*) to start using WebGoat...")


@fixture(scope="module")
def app_class(wait_for_compose):
    return WebGoat


@mark.parametrize("username,password", get_params())
def test_webgoat(app, username, password):
    _test_app(app, username, password)
