import re
from pathlib import Path

from playwright.sync_api import Page
from pytest import fixture, mark
from testcontainers.compose import DockerCompose

from tests.generate.test_login import get_login_test_cases
from tests.vulnurabilities.conftest import VulnerableApp

PATH = Path(__file__).parent
BASE_URL = "http://localhost:4281/WebGoat"


class WebGoat(VulnerableApp):
    def __init__(self, page: Page):
        self.page = page
        self._register()

    def _register(self):
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
def compose():
    with DockerCompose(PATH) as compose:
        yield compose


@fixture(scope="module")
def wait_for_compose(compose):
    while True:
        stdout, stderr = compose.get_logs()

        if m := re.findall(r"Please browse to (.*) to start using WebGoat...", stdout):
            return m[0]


@fixture(scope="module")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()


@fixture(scope="module")
def app(context, wait_for_compose):
    page = context.new_page()
    app = WebGoat(page)
    return app


params = get_login_test_cases("admin", "password")
params = [(x["username"], x["password"]) for x in params]
if (x := ("admin", "password")) not in params:
    params.append(x)


@mark.parametrize("username,password", params)
def test_webgoat(app, username, password, page):
    app.page = page
    app.login(username, password)
