from abc import ABC, abstractmethod


class VulnerableApp(ABC):
    @abstractmethod
    def login(self, username, password) -> bool: ...
