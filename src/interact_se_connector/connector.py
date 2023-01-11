from pathlib import Path
import pandas as pd
import requests
from interact_se_connector.scrapper_hugo import ScrapperHugo
from interact_se_connector.scrapper_jupyterbook import ScrapperJupyterBook
from interact_se_connector.scrapper_grubermarkdown import ScrapperGruberMarkdown
from interact_se_connector.scrapper import ParseWrongGeneratorType
from icecream import ic
import json
from urllib.parse import urljoin


def find_suitable_scrapper(root_dir: Path):
    """
    This probably isn't the right place for this method, but it saves faffing arround
    trying to solve circular imports.
    """
    candidate_scrapers = [
        ScrapperGruberMarkdown,
        ScrapperJupyterBook,
        ScrapperHugo,
    ]

    scrapper = None

    for candidate in candidate_scrapers:
        try:
            scrapper = candidate(root_dir)
            scrapper.do_walk()
            break
        except ParseWrongGeneratorType:
            scrapper = None

    return scrapper


class InteractConnection:
    """
    # enterprise_search_name
    # secret_key
    # content_type_name
    # document_icon_asset

    See https: // developer.interactsoftware.com/docs/how-to-set-up-enterprise-search

    # http: // {your domain}/api/searchapp
    # http: // {your domain}/api/searchapp/{appid}/document

    # CRUD methods
    # Create records
    # Delete records
    """

    def __init__(self, display_url, api_key, search_app_id: int) -> None:
        self.display_url = display_url
        self.common_headers = {"X-ApiKey": api_key, "Accept": "application/json"}

        self._get_api_details()
        self.search_app_url = urljoin(
            self.api_url, f"/api/searchapp/{search_app_id}/document"
        )

    def _get_api_details(self):
        """
        Get details from the `{display_url}/info` page required to access to the API
        https://developer.interactsoftware.com/reference/information
        """
        info_url = urljoin(self.display_url, "/info")
        response = requests.get(info_url)
        response.raise_for_status()
        tenant_info = response.json()
        ic(tenant_info)

        self.api_url = tenant_info.get("ApiDomain")

        self.common_headers.update({"X-Tenant": tenant_info.get("TenantGuid")})

    def get_all_current_docs(self):
        """
        How can this be done?
        How to list existing `docimentid`s?
        """
        pass

    def delete_doc(self, doc_id):
        """
        HTTP DELETE verb.

        http: // /api/searchapp/1/document/{documentid}
        requests.delete('https://httpbin.org/delete')
        """
        response = requests.delete(
            url=urljoin(self.search_app_url, doc_id),
            headers=self.common_headers,
        )
        response.raise_for_status()

    def upload_scrapper_content(self, data_frame: pd.DataFrame):
        """
        $templateJSON = "{
          ""Url"": ""file: " + $uncPath + "/{filepath}"",
          ""Id"": ""{id}"",
          ""Title"": ""{filename}"",
          ""IsPublic"": ""true"",
          ""Body"": ""{filename}"",
          ""summary"": ""{filename}"",
          ""Author"": ""{author}"",
        }"
        """
        for row in data_frame.itertuples():
            # ic(row)
            # row_as_json = json.dumps({
            #   "Url": row.url,
            #   "Id": row.id,
            #   "Title": row.title,
            #   "IsPublic": row.is_public,
            #   "Body": row.body,
            #   "summary": row.summary,
            #   "Author": row.author,
            # }, indent = 4)
            # print(row_as_json)

            row_as_dict = {
                "Url": row.url,
                "Id": row.id,
                "Title": row.title,
                "IsPublic": row.is_public,
                "Body": row.body,
                "summary": row.summary,
                "Author": row.author,
            }
            print(row_as_dict)
            self.upload_single_file(row_as_dict)

            # json.dumps(ro)

    def upload_single_file(self, row_as_dict):
        """
        Invoke-RestMethod
          -Uri $interactURI
          -Method Put
          -ContentType "application/json"
          -Headers @{'X-ApiKey'='<API Key from Search Apps>'; }
          -Body $fileJSON
        """
        response = requests.put(
            url=self.search_app_url, headers=self.common_headers, json=row_as_dict
        )
        response.raise_for_status()
