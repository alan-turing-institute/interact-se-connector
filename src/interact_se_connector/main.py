import os
from argparse import ArgumentParser
from interact_se_connector.connector import InteractConnection, find_suitable_scrapper
import sys
from icecream import ic


def main():
    args = get_args(sys.argv[1:])
    source_dir = args.interact_source_dir
    display_url = args.interact_root_url
    api_key = args.interact_app_secret
    search_app_id = args.interact_app_id

    do_work(
        source_dir=args.interact_source_dir,
        display_url=args.interact_root_url,
        api_key=args.interact_app_secret,
        search_app_id=args.interact_app_id,
    )


def do_work(source_dir, display_url, api_key, search_app_id):
    # Don't make changes to Interact until we are sure that we can
    # (i) parse the new content
    # (ii) remove the old pages from the index

    # Parse content
    scrapper = find_suitable_scrapper(source_dir)
    scrapped_content = scrapper.do_walk()

    # Create the connection to Interact
    conn = InteractConnection(
        display_url=display_url, api_key=api_key, search_app_id=search_app_id
    )

    # Remove the old index
    page_list = conn.get_all_current_docs()
    for page_id in page_list:
        conn.delete_doc(page_id)

    # Now add the new content
    conn.upload_scrapper_content(scrapped_content)


def environ_or_required(key):
    """
    Using solution from: https://stackoverflow.com/a/45392259/3837936
    """
    return (
        {"default": os.environ.get(key)} if os.environ.get(key) else {"required": True}
    )


def get_args(args) -> ArgumentParser:
    ic(args)
    main_parser = ArgumentParser(
        prog="isec",
        description=(
            "The Interact Search Engine Connector (isec) updates the search index for the Interact's Search Engine feature."
            " (This has been developed independently from Interact and is not supported by them.)"
        ),
    )

    options_grp = main_parser.add_mutually_exclusive_group(required=False)

    options_grp.add_argument(
        "--force",
        action="store_true",
        help=(
            "Updates the entire index for this application, even if no change is detected"
            " in any of the input files. (`--force` and `--dry-run`  cannot"
            " be specified together.)"
        ),
    )

    options_grp.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Do not make any changes to the Interact Search Engine index. Run through each step"
            " and attempt to identify any potential errors with parsing the input data."
            " (`--dry-run` and `--force` cannot be specified together.)"
        ),
    )

    main_parser.add_argument(
        "--interact-source-dir",
        **environ_or_required("ISEC_INTERACT_SOURCE_DIR"),
        help=(
            "The directory containing the pages to be indexed. If the environment variable `ISEC_INTERACT_SOURCE_DIR` is set then that value will be used and this command-line option can be omitted. If both are supplied, then the command-line option take precedence."
        ),
    )

    main_parser.add_argument(
        "--interact-root-url",
        **environ_or_required("ISEC_INTERACT_ROOT_URL"),
        help=(
            "The URL of the home page of the Interact Server. Typically this is just in the form 'https://intranet.example.com'. If the environment variable `ISEC_INTERACT_ROOT_URL` is set then that value will be used and this command-line option can be omitted. If both are supplied, then the command-line option take precedence."
        ),
    )

    main_parser.add_argument(
        "--interact-app-id",
        **environ_or_required("ISEC_INTERACT_APP_ID"),
        help=(
            "The Interact `appid`. See 'https://developer.interactsoftware.com/docs/how-to-set-up-enterprise-search#api' for details on how to obtain this. If the environment variable `ISEC_INTERACT_APP_ID` is set then that value will be used and this command-line option can be omitted. If both are supplied, then the command-line option take precedence."
        ),
    )

    main_parser.add_argument(
        "--interact-app-secret",
        **environ_or_required("ISEC_INTERACT_APP_SECRET"),
        help=(
            "The secret key specified when then search app was created in Interact (This should always be kept confidential). See 'https://developer.interactsoftware.com/docs/how-to-set-up-enterprise-search#setting-up-an-enterprise-search-application' for details.  If the environment variable `ISEC_INTERACT_APP_SECRET` is set then that value will be used and this command-line option can be omitted. If both are supplied, then the command-line option take precedence. **It is strongly recommended** that the environment variable option is used in any production setting to ensure that the secret is not exposed in any publicly visible scripts or logfiles."
        ),
    )

    try:
        return main_parser.parse_args(args=args)
    except AttributeError:
        main_parser.print_usage()


if __name__ == "__main__":
    main()
