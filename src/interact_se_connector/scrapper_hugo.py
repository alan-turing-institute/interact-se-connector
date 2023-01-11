from pathlib import Path
from typing import List

import interact_se_connector.scrapper as scrapper

from bs4 import Tag
from icecream import ic
import re


class ScrapperHugo(scrapper.Scrapper):
    def __init__(self, root_dir: Path):
        self.author = ""
        self.is_public = True
        super().__init__(root_dir, [".html"])

    def pre_parse(self, soup: Tag) -> Tag:
        body = scrapper.strip_internal_anchors(soup, "anchor")
        return super().pre_parse(soup)

    def assert_suitable_generator(self, soup: Tag) -> bool:
        signature = soup.find(
            "meta", attrs={"name": "generator", "content": re.compile("Hugo 0\.\d")}
        )
        return bool(signature)

    def get_url(self, soup: Tag, fname: Path) -> str:
        url = soup.find("meta", attrs={"property": "og:url"})
        return url.attrs.get("content", None)

    def get_page_id(self, soup: Tag) -> str:
        pass

    def get_body(self, soup: Tag) -> str:
        body = soup.find("article", attrs={"class": "markdown"})
        # body = strip_internal_anchors(body, "anchor")
        return scrapper.strip_formatting(body)

    def get_keywords(self, soup: Tag) -> str:
        body = soup.find("article", attrs={"class": "markdown"})
        # body = strip_internal_anchors(body, "anchor")
        return " ".join(scrapper.get_keywords_from_headings(body))

    def get_title(self, soup: Tag, fname: Path) -> str:
        title = soup.find("meta", attrs={"property": "og:title"})
        return title.attrs.get("content", None)

    def get_summary(self, soup: Tag) -> str:
        # TODO
        return self.get_body(soup)

    def get_author(self, soup: Tag) -> str:
        return self.author

    def get_is_public(self, soup: Tag) -> bool:
        return self.is_public
