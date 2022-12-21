
from pathlib import Path
import os
from icecream import ic
from typing import List, Tuple, MutableSet
from bs4 import BeautifulSoup, Tag
import re

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

    for anchor_tags in soup.find_all("a", attrs={"class":class_name}):
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

def strip_formatting(soup: Tag) -> List[str]:
    """"
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


class Scrapper:
    def __init_():
        pass


    def do_walk(self, root_dir: Path, allowed_extensions: List[str]):
        for root, dirs, files in os.walk(root_dir, topdown=False):
            # ic(root)
            # ic(type(rootfd))
            for file_name in files:
                ic(file_name)
                fname = Path(root, file_name).resolve()
                # ic(fname.exists())

                if fname.suffix in allowed_extensions:
                    self.read_file(fname)
            # for dir_name in dirs:
            #     ic(type(dir_name))
                

    def read_file(self, fname: Path):
        with open(fname) as fp:
            soup = BeautifulSoup(fp, features="html5lib")

            url = soup.find("meta", attrs={"property":"og:url"})
            url = url.attrs.get("content", None)

            title = soup.find("meta", attrs={"property":"og:title"})
            title = title.attrs.get("content", None)

            # <meta property="og:url" content="https://alan-turing-institute.github.io/REG-handbook/docs/communications/">

            # body = soup.find_all("article", class="markdown")
            body = soup.find("article", attrs={"class":"markdown"})
            # body = "\n".join([text for text in body.stripped_strings])
            # [u'I linked to', u'example.com']
            # body = body.get_text(" ", strip=True)
            # body = body.get_text()

            ic(url)
            ic(title)
            ic(body)
            ic(type(body))



        # tag = soup.article
        # # tag[]

        # body = unicode(tag.string)

        """
        body =
          - xpath = /html/body/main/div/article
          - tag = article
          - class = markdown
        """

