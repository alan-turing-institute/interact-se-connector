from pathlib import Path

from bs4 import BeautifulSoup
from icecream import ic
from pytest import mark
from types import NoneType

from interact_se_connector.scrapper import (
    get_keywords_from_headings,
    strip_formatting,
    strip_internal_anchors,
)
from interact_se_connector.connector import find_suitable_scrapper

from interact_se_connector.scrapper_hugo import ScrapperHugo
from interact_se_connector.scrapper_jupyterbook import ScrapperJupyterBook

# @mark.skip()


@mark.parametrize(
    "test_dir, expected_type",
    [
        (Path(__file__, "..", "hugo").resolve(), ScrapperHugo),
        (Path(__file__, "..", "jupyterbook").resolve(), ScrapperJupyterBook),
        (Path(__file__, "..", "unsupported").resolve(), NoneType),
    ],
)
def test_pick_scrapper(test_dir, expected_type):
    # test_dir = Path(__file__, "..", "hugo").resolve()
    ic(test_dir)

    scrapper = find_suitable_scrapper(test_dir)
    ic(type(scrapper))
    actual_type = type(scrapper)
    assert actual_type == expected_type

    # assert False


def test_do_walk():

    # Run Hugo example
    test_dir = Path("/Users/a.smith/code/knowledgemanagement/REG-handbook/public/docs")
    allowed_extensions = [".html"]
    hugo_scrapper = ScrapperHugo(test_dir, allowed_extensions)
    result = hugo_scrapper.do_walk()
    result.to_csv("test_hugo_output.csv")

    # Run JupyterBook example
    test_dir = Path(
        "/Users/a.smith/code/knowledgemanagement/the-turing-way/book/website/_build/html"
    )
    allowed_extensions = [".html"]
    jb_scrapper = ScrapperJupyterBook(test_dir, allowed_extensions)
    result = jb_scrapper.do_walk()
    result.to_csv("test_jupyter_output.csv")

    assert False


def test_strip_formatting():
    input_fpath = Path(
        __file__, "..", "hugo", "hugo_input_content_only.html-extract"
    ).resolve()
    ic(input_fpath)

    expected_fpath = Path(__file__, "..", "hugo", "hugo_expected_body.txt").resolve()

    with open(input_fpath) as in_file:
        soup = BeautifulSoup(in_file, features="html5lib")

    with open(expected_fpath) as expect_file:
        expected_body = expect_file.read()

    soup = strip_internal_anchors(soup, "anchor")
    actual_body = strip_formatting(soup)

    print()
    print(actual_body)
    print()

    # Strip the whitespace at either end rather than faff around
    # stopping pre-commit from altering the example files
    assert actual_body.strip() == expected_body.strip()


def test_strip_internal_anchors():

    input_str = """
    <h2>
    Bonus Section: Learning from Mistakes<a class="headerlink" href="#bonus-section-learning-from-mistakes" title="Permalink to this headline">#</a>
    </h2>
    """

    expected_str = """
    <h2>
    Bonus Section: Learning from Mistakes
    </h2>
    """

    soup = BeautifulSoup(input_str, features="html5lib")
    actual_body = strip_internal_anchors(soup, "headerlink")

    expected_soup = BeautifulSoup(expected_str, features="html5lib")

    ic(actual_body)
    ic(expected_soup)
    assert str(actual_body) == str(expected_soup)


def test_get_keywords_from_headings():

    fname = Path(
        __file__, "..", "hugo", "hugo_input_content_only.html-extract"
    ).resolve()
    ic(fname)

    expected_body = "b"
    expected_keywords = "k"

    with open(fname) as fp:
        soup = BeautifulSoup(fp, features="html5lib")

    expected = {
        "#",
        "Lightning",
        "Talks",
        "Talk",
        "Format",
        "Sign",
        "Up",
        "Previous",
        "Talks",
    }
    actual = get_keywords_from_headings(soup)

    assert expected == actual
