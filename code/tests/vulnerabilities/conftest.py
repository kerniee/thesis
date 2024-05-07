from abc import abstractmethod
from pathlib import Path
from typing import Iterator

from playwright.sync_api import BrowserContext, Page
from pytest import fixture
from testcontainers.compose import DockerCompose

from tests.generate.test_login import get_login_test_cases


class VulnerableApp:
    def __init__(self, page: Page):
        self.page = page

    @abstractmethod
    def init(self) -> None: ...

    @abstractmethod
    def login(self, username, password) -> bool: ...


@fixture(scope="module")
def compose(request) -> DockerCompose:
    with DockerCompose(Path(request.path).parent) as compose:
        yield compose


@fixture(scope="module")
def context(browser) -> Iterator[BrowserContext]:
    context = browser.new_context()
    yield context
    context.close()


@fixture(scope="module")
def app_class() -> type[VulnerableApp]:
    raise NotImplementedError


@fixture(scope="module")
def app(context, app_class) -> Iterator[VulnerableApp]:
    page_init = context.new_page()
    app = app_class(page_init)
    app.init()
    yield app
    page_init.close()


def get_params() -> list[tuple[str, str]]:
    params = get_login_test_cases("admin", "password")
    params = [(x["username"], x["password"]) for x in params]
    if (x := ("admin", "password")) not in params:
        params.append(x)
    return params
