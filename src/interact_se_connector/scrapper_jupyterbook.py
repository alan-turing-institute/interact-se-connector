from pathlib import Path
from typing import List

from interact_se_connector.scrapper import (
    Scrapper,
    ParseSkipFile,
    get_keywords_from_headings,
    strip_formatting,
    strip_internal_anchors,
)
from bs4 import Tag
import re

from icecream import ic

class ScrapperJupyerBook(Scrapper):

    def __init__(self, root_dir: Path, allowed_extensions: List[str]):
        self.author = ""
        self.is_public = True
        super().__init__(root_dir, allowed_extensions)

    def pre_parse(self, soup: Tag) -> Tag:
        body = strip_internal_anchors(soup, "headerlink")

        # Skip the "genindex.html" and search pages
        # <div class="genindex-jumpbox">
        # <div id="search-results">
        skip_file = bool(body.find("div", attrs={"class":"genindex-jumpbox"})) \
            or bool(body.find("div", attrs={"id":"search-results"}))
        if skip_file:
            raise ParseSkipFile()

        return super().pre_parse(body)

    def assert_suitable_generator(self, soup: Tag) -> bool:
        signature = soup.find(
            "meta", attrs={"name":"generator", "content":re.compile("Docutils 0\.\d")}
        )
        return bool(signature)        

    def get_url(self, soup: Tag) -> str:
        url = soup.find("link", attrs={"rel": "canonical"})
        # for url in urls:
        #     ic(url)

        # return "nothing found"
        return url.attrs.get("href", None)

    def get_page_id(self, soup: Tag) -> str:
        pass

    def get_body(self, soup: Tag) -> str:
        body = soup.find("main", attrs={"id": "main-content", "role":"main"})

        # body = strip_internal_anchors(body, "anchor")
        return strip_formatting(body)

    def get_keywords(self, soup: Tag) -> str:
        body = soup.find("article", attrs={"class": "markdown"})
        # body = strip_internal_anchors(body, "anchor")
        return " ".join(get_keywords_from_headings(body))

    def get_title(self, soup: Tag) -> str:
        # The least worst option to do this in a single line seems to be to get the title from the currently highlight entry in the 
        # ```
        # title = soup.find("a", attrs={"class": "current reference internal"})        
        # ```
        # However it feels cleaner to do a two stage search in this case.
        head = soup.find("head")
        # ic(head)
        title = head.find("title")
        # ic(title)
        return title.attrs.get("content", None)

    def get_summary(self, soup: Tag) -> str:
        # TODO
        return self.get_body(soup)

    def get_author(self, soup: Tag) -> str:
        return self.author

    def get_is_public(self, soup: Tag) -> bool:
        return self.is_public
