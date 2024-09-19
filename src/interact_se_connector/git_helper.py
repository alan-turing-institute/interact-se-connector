from git import Repo
import re


def get_remote_url(dir_path) -> str:
    """
    raises git.exc.InvalidGitRepositoryError if `dir_path` is not a valid git repo.
    """
    repo = Repo(dir_path)

    if len(repo.remotes) != 1:
        raise ValueError(
            "Cannot handle cases where either no 'git remote' exists, or more than one 'git remote' url exists"
        )

    return repo.remote().url


def get_base_from_remote_url(remote: str) -> str:
    # Check of `.git` at the end of the string
    if not remote.endswith(".git"):
        raise ValueError(
            f"The URL '{remote}' does not appear to be a remote git clone. Expecting a URL ending with `.git"
        )

    result = re.sub(".wiki.git$", "/wiki/", remote, flags=re.IGNORECASE)
    result = re.sub(".git$", "/", result, flags=re.IGNORECASE)

    return result


def get_remote_url_type(url: str) -> str:
    """
    Checks if the url is ssh, https
    """

    if url.startswith("git@"):
        return "SSH"
    elif url.startswith("https://"):
        return "HTTPS"
    else:
        raise ValueError(f"Unknown url type: {url} ")


def build_ssh_https_url(remote_base: str, remote_type: str) -> str:
    """
    Returns a formatted remote url for ssh or https from a given base
    """
    if remote_type == "SSH":
        return "git@github.com:" + remote_base
    elif remote_type == "HTTPS":
        return "https://github.com/" + remote_base
    else:
        raise ValueError(f"Unknown remote type {remote_type}")
