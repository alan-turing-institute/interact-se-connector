from pathlib import Path
from typing import List

import interact_se_connector.scrapper as scrapper
import interact_se_connector.git_helper as git_helper

from bs4 import Tag, BeautifulSoup
from icecream import ic
import markdown
from markdown.extensions.tables import TableExtension
from urllib.parse import urljoin
from git.exc import InvalidGitRepositoryError


class ScrapperGruberMarkdown(scrapper.Scrapper):
    def __init__(self, root_dir: Path):
        self.author = ""
        self.is_public = False

        # Attempt to work out base url from git repo
        try:
            remote_git_url = git_helper.get_remote_url(root_dir)
            self.base_url = git_helper.get_base_from_remote_url(remote_git_url)
        except InvalidGitRepositoryError:
            raise scrapper.ParseWrongGeneratorType

        self.md_reader = markdown.Markdown(extensions=[TableExtension()])
        super().__init__(root_dir, [".md"])

    def get_initial_soup(self, fname: Path) -> Tag:
        with open(fname, "r", encoding="utf-8") as input_file:
            text = input_file.read()

        html_str = self.md_reader.convert(text)
        self.md_reader.reset()
        soup = BeautifulSoup(html_str, features="html5lib")

        return soup

    def pre_parse(self, soup: Tag) -> Tag:
        body = scrapper.strip_internal_anchors(soup, "anchor")
        return super().pre_parse(soup)

    def assert_suitable_generator(self, soup: Tag) -> bool:
        """
        There is no way to detect if this isn't valid markdown, so we just return True
        """
        return True

    def get_url(self, soup: Tag, fname: Path) -> str:
        rel_path = fname.relative_to(self.root_dir).stem
        return urljoin(self.base_url, str(rel_path))

    def get_page_id(self, soup: Tag) -> str:
        pass

    def get_body(self, soup: Tag) -> str:
        return scrapper.strip_formatting(soup)

    def get_keywords(self, soup: Tag) -> str:
        return " ".join(scrapper.get_keywords_from_headings(soup))

    def get_title(self, soup: Tag, fname: Path) -> str:
        return "wrong"

    def get_summary(self, soup: Tag) -> str:
        # TODO
        return self.get_body(soup)

    def get_author(self, soup: Tag) -> str:
        return self.author

    def get_is_public(self, soup: Tag) -> bool:
        return self.is_public
