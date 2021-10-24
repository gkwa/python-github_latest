import abc
import dataclasses
import json
import logging
import pathlib
import re

import requests


class ResolverStategy(abc.ABC):
    @abc.abstractmethod
    def resolve(self):
        pass


class ApiResolvingStragey(ResolverStategy):
    def resolve(self, url: str) -> str:
        api_url = url.replace("https://github.com", "https://api.github.com/repos")
        logging.debug(f"{api_url=}")

        response = requests.get(api_url)
        js = response.json()
        logging.debug(json.dumps(js, indent=2))

        tag = js.get("tag_name")
        logging.debug(f"{tag=}")

        version = tag.replace("v", "")
        logging.debug(f"{version=}")

        return version


class RedirectResolvingStragey(ResolverStategy):
    def resolve(self, url: str) -> str:
        response = requests.get(url)
        logging.debug(f"{response.url=}")

        path = pathlib.Path(response.url)
        logging.debug(f"{path=}")
        logging.debug(f"{path.name=}")

        version = path.name.replace("v", "")
        logging.debug(f"{version=}")

        return version


@dataclasses.dataclass
class Resolver:
    url: str
    resolver: ResolverStategy
    version: str = None

    def __post_init__(self):
        logging.debug(f"{self.url=}")

    def resolve(self):
        self.version = self.resolver.resolve(self.url)

    def version_found(self):
        if re.search(r"([\d.]+)", self.version):
            return True
        return False
