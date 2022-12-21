from pathlib import Path
import os
from icecream import ic
from typing import List, Tuple, MutableSet
from bs4 import BeautifulSoup, Tag
import re
from abc import ABC, abstractmethod

"""
$templateJSON = "{
  ""Url"": ""file:" + $uncPath + "/{filepath}"",
  ""Id"": ""{id}"",
  ""Title"": ""{filename}"",
  ""IsPublic"": ""true"",
  ""Body"": ""{filename}"",
  ""summary"": ""{filename}"",
  ""Author"": ""{author}"",
}"
"""
# ic.disable()

"""
Striping out common words
https://stackoverflow.com/questions/9953619/technique-to-remove-common-wordsand-their-plural-versions-from-a-string
"""


def strip_internal_anchors(soup: Tag, class_name: str) -> Tag:

    for anchor_tags in soup.find_all("a", attrs={"class": class_name}):
        anchor_tags.decompose()

    return soup


def _do_strip_formatting(soup: Tag) -> List[str]:
    """
    Recursively search the html extracting the contents as plain text.
    This function is an intermediatory - You probably should call `strip_formatting` which returns a single `str`.

    @returns An array of strings which collectively form the plain text representation of the input html.
    """

    if not hasattr(soup, "contents"):
        # This element is text. The process here is to:
        # - Split the text into separate lines.
        # - If this results in an empty line, than add a newline char back in.
        # - For all other lines, strip out most of the white space, but ensure that there is exactly one space at the end.
        return [f"{s.strip()} " if s else "\n" for s in soup.string.splitlines()]

    result_body = []
    for child in soup.contents:
        # This element contains other elements
        # Call `_strip_formmatting` recursively on the child elements.
        result_body.extend(_do_strip_formatting(child))

    return result_body


def strip_formatting(soup: Tag) -> str:
    """ "
    Recursively search the html extracting the contents as plain text.
    The real work of this is performed by the function `_do_strip_formatting`.

    @returns An array of strings which collectively form the plain text representation of the input html.
    """
    return "".join(_do_strip_formatting(soup))


def get_keywords_from_headings(soup: Tag) -> MutableSet[str]:

    result_keywords = set()

    headers = soup.find_all(re.compile("^h\d"))
    if headers:
        for kws in headers:
            for kw in kws.stripped_strings:
                result_keywords.update(kw.split())

    return result_keywords


class Scrapper(ABC):
    def __init__(self, root_dir: Path, allowed_extensions: List[str]):
        self.root_dir = root_dir
        self.allowed_extensions = allowed_extensions

    def do_walk(self):
        for root, _, files in os.walk(self.root_dir, topdown=False):
            for file_name in files:
                ic(file_name)
                fname = Path(root, file_name).resolve()

                if fname.suffix in self.allowed_extensions:
                    self._scrape_file(fname)

    def _scrape_file(self, fname: Path) -> dict:
        with open(fname) as fp:
            soup = BeautifulSoup(fp, features="html5lib")

            """
            # Playing around assuming hugo
            url = soup.find("meta", attrs={"property": "og:url"})
            url = url.attrs.get("content", None)

            title = soup.find("meta", attrs={"property": "og:title"})
            title = title.attrs.get("content", None)

            body = soup.find("article", attrs={"class": "markdown"})

            ic(url)
            ic(title)
            ic(body)
            ic(type(body))
            """

            return {
                "Url": self.get_url(soup),
                "Id": "{id}soup",
                "Title": self.get_title(soup),
                "IsPublic": self.get_is_public(soup),
                "Body": self.get_body(soup),
                "summary": self.get_summary(soup),
                "Author": self.get_author(soup),
            }

    @abstractmethod
    def get_url(self, soup: Tag) -> str:
        pass

    @abstractmethod
    def get_page_id(self, soup: Tag) -> str:
        pass

    @abstractmethod
    def get_body(self, soup: Tag) -> str:
        pass

    @abstractmethod
    def get_keywords(self, soup: Tag) -> str:
        pass

    @abstractmethod
    def get_title(self, soup: Tag) -> str:
        pass

    @abstractmethod
    def get_summary(self, soup: Tag) -> str:
        pass

    @abstractmethod
    def get_author(self, soup: Tag) -> str:
        pass

    @abstractmethod
    def get_is_public(self, soup: Tag) -> str:
        pass
