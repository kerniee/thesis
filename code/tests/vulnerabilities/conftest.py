from abc import abstractmethod
from pathlib import Path
from typing import Iterator, OrderedDict

from playwright.sync_api import BrowserContext, Page
from pytest import fixture

from tests.utils import DockerCompose


class VulnerableApp:
    def __init__(self, page: Page):
        self.page = page
        self.init()

    @abstractmethod
    def init(self) -> None: ...


@fixture(scope="module")
def compose(request) -> Iterator[DockerCompose]:
    dc = DockerCompose(Path(request.path).parent)
    dc.kill()
    dc.start()
    yield dc
    dc.kill()


@fixture(scope="module")
def context(browser) -> Iterator[BrowserContext]:
    context = browser.new_context()
    yield context
    context.close()


@fixture(scope="module")
def page_init(context) -> Page:
    page = context.new_page()
    return page


@fixture(scope="module")
def app(page_init) -> VulnerableApp:
    raise NotImplementedError


def to_parametrize(
    params: list[OrderedDict],
) -> tuple[str, list[list[str]] | list[str]]:
    keys = ",".join(params[0].keys())
    if "," in keys:
        values = list(map(lambda d: list(d.values()), params))
    else:
        values = list(map(lambda d: list(d.values())[0], params))
    return keys, values
