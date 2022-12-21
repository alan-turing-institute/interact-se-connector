import os
from argparse import ArgumentParser


def my_func(args):
    for k, v in args:
        print(f"k={k}, v={v}")


def main():
    parser = get_args()
    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.print_usage()


def environ_or_required(key):
    """
    Using solution from: https://stackoverflow.com/a/45392259/3837936
    """
    return (
        {"default": os.environ.get(key)} if os.environ.get(key) else {"required": True}
    )


def get_args() -> ArgumentParser:
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

    # main_parser.set_defaults(func=TO_BE_CONFIRMED)

    return main_parser


if __name__ == "__main__":
    main()
