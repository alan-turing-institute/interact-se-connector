from pathlib import Path
from typing import List

from scrapper import (
    Scrapper,
    get_keywords_from_headings,
    strip_formatting,
    strip_internal_anchors,
)
from bs4 import Tag


class ScrapperHugo(Scrapper):
    def __init_(self, root_dir: Path, allowed_extensions: List[str]):
        super().__init__(root_dir, allowed_extensions)

        self.author = ""
        self.is_public = ""

    def get_url(self, soup: Tag) -> str:
        url = soup.find("meta", attrs={"property": "og:url"})
        return url.attrs.get("content", None)

    def get_page_id(self, soup: Tag) -> str:
        pass

    def get_body(self, soup: Tag) -> str:
        body = soup.find("article", attrs={"class": "markdown"})
        body = strip_internal_anchors(body, "anchor")
        return strip_formatting(body)

    def get_keywords(self, soup: Tag) -> str:
        body = soup.find("article", attrs={"class": "markdown"})
        body = strip_internal_anchors(body, "anchor")
        return " ".join(get_keywords_from_headings(body))

    def get_title(self, soup: Tag) -> str:
        title = soup.find("meta", attrs={"property": "og:title"})
        return title.attrs.get("content", None)

    def get_summary(self, soup: Tag) -> str:
        # TODO
        return self.get_body(soup)

    def get_author(self, soup: Tag) -> str:
        pass

    def get_is_public(self, soup: Tag) -> str:
        return self.is_public
