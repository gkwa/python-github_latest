import dataclasses
import json
import logging
import re

import requests


@dataclasses.dataclass
class Resolver:
    url: str
    version: str = None

    def __post_init__(self):
        logging.debug(f"{self.url=}")

    def resolve(self) -> str:
        x1 = self.url.replace("https://github.com", "https://api.github.com/repos")
        logging.debug(f"{x1=}")
        response = requests.get(x1)
        js = response.json()
        logging.debug(json.dumps(js, indent=2))

        tag = js.get("tag_name")
        logging.debug(f"{tag=}")

        self.version = tag.replace("v", "")

    def version_found(self):
        if re.search(r"([\d.]+)", self.version):
            return True
        return False
