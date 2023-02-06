# Interact Search Engine Connector

The Interact Search Engine Connector (isec) updates the search index for [Interact's](https://www.interactsoftware.com/) Search Engine feature.

** This has been developed independently from Interact and is not supported by them. **


## Todo

- [x] setup.py / pyproject.toml
- [ ] Local pyenv
- [x] Check whether args are passed with '-' or '_'
- [ ] Option to represent the base page URL if it is not available from html header
- [x] Option to derive base page URL from git repo (catch case where there is multiple repos).
- [ ] Create Dockerfile
- [ ] Publish as GitHub Action
- [ ] Unit tests on CI
- [ ] Publish to PyPI
- [ ] Solve how to delete old/stale page index entries
- [ ] Testing
- [ ] Docs + Docstring
- [x] Linting
- [ ] Typing
- [x] Link CLI to main methods
- [ ] Force option
- [ ] Dry-run option
- [ ] Add Author option
- [ ] Add summary option
- [ ] Add is_public option
- [ ] Add security page access options
- [ ] Meaningful error codes
- [ ] Filter by doc_id prefix
- [ ] Test `test_do_walk` is too slow. Need to make this run on subsample, not entire source books.

## Useful reference docs

https://developer.interactsoftware.com/docs/enterprise-search


## Target Static site generators

- [Hugo](https://gohugo.io/) - For the REG Handbook
- [JupyterBook](https://jupyterbook.org/en/stable/intro.html) - For the Turing Way.
- GitHub wikis
- Other GitHub content
- GitHub Flavored Markdown. Possible renderers:
  - [GitHub's fork of CommonMark](https://github.com/github/cmark-gfm)
  - https://docs.github.com/en/rest/markdown?apiVersion=2022-11-28#render-a-markdown-document
  - https://github.com/gollum/gollum
  - https://github.com/vmg/redcarpet
    See also:
      - https://stackoverflow.com/questions/7694887/is-there-a-command-line-utility-for-rendering-github-flavored-markdown
      - https://softwareengineering.stackexchange.com/questions/128712/what-is-a-markdown-formatted-readme-file-on-github/128721#128721

# Acknowledgements

## Sample data

The dir `tests/test_static_sites` contains subsets from sample sites, which where built using a range of different static site generators.

- **`hugo`** contains a sample from [The Alan Turing Institute's Research Engineering Group (REG) Handbook](https://alan-turing-institute.github.io/REG-handbook/), [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

- **`jupyterbook`** contains a sample from [The Turing Way](https://the-turing-way.netlify.app/welcome.html), by The Turing Way Community, © Copyright 2020-2021. [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
