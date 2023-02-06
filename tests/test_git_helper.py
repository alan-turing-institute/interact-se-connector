import pytest
import interact_se_connector.git_helper as git_helper
from icecream import ic
from pathlib import Path
from git.exc import InvalidGitRepositoryError

def test_get_remote_url_not_a_git_repo(tmp_path):
    with pytest.raises(InvalidGitRepositoryError):
        git_helper.get_remote_url(tmp_path)


def test_get_remote_url():
    root_dir = (Path(__file__) / ".." / "..").resolve()
    expected_remote = "https://github.com/andrewphilipsmith/interact-se-connector.git"

    actual_remote = git_helper.get_remote_url(root_dir)

    assert actual_remote == expected_remote


@pytest.mark.parametrize(
    "remote,expected_base",
    [
        (
            "https://github.com/example/interact-se-connector.git",
            "https://github.com/example/interact-se-connector/",
        ),
        (
            "https://github.com/example/interact-se-connector.wiki.git",
            "https://github.com/example/interact-se-connector/wiki/",
        ),
        ("https://github.com/example/interact-se-connector", ValueError),
    ],
)
def test_get_base_from_remote_url(remote, expected_base):
    if isinstance(expected_base, type):
        with pytest.raises(expected_base):
            git_helper.get_base_from_remote_url(remote)

    else:
        actual_base = git_helper.get_base_from_remote_url(remote)
        assert actual_base == expected_base
