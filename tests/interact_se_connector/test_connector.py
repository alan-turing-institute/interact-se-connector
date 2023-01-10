from interact_se_connector.connector import InteractConnection
import pandas as pd

def test_interact_connection_constructor():
    assert False


def test_upload_scrapper_content():
    iac = InteractConnection()
    hugo_df = pd.read_csv("test_hugo_output.csv")
    iac.upload_scrapper_content(hugo_df.head(2))
    assert False


def test_check_connection():
    iac = InteractConnection(
        display_url="https://mathison.turing.ac.uk/info",
        api_key="123",
        search_app_id=1
    )

    iac._get_api_details()