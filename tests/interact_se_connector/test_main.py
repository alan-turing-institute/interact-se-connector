import pytest
from interact_se_connector.main import get_args
from icecream import ic


def test_main():
    pass


@pytest.mark.parametrize(
    "arg_pairs",
    [
        ("ISEC_INTERACT_SOURCE_DIR", "--interact-source-dir"),
        ("ISEC_INTERACT_ROOT_URL", "--interact-root-url"),
        ("ISEC_INTERACT_APP_ID", "--interact-app-id"),
        ("ISEC_INTERACT_APP_SECRET", "--interact-app-secret"),
    ],
    ids=[
        "interact-source-dir",
        "interact-root-url",
        "interact-app-id",
        "interact-app-secret",
    ],
)
def test_get_args_from_env(monkeypatch, arg_pairs):

    env_name, arg_name = arg_pairs
    arg_name_py = arg_name.replace("--", "").replace("-", "_")

    all_arg_names = [
        "--interact-source-dir",
        "--interact-root-url",
        "--interact-app-id",
        "--interact-app-secret",
    ]

    monkeypatch.setenv(env_name, "value_from_env", prepend=False)

    # Now check that the cmdline overrider the env var
    cmdline_args = []
    for aname in all_arg_names:
        cmdline_args.append(aname)
        cmdline_args.append("value_from_cmdline")

    actual_args = get_args(cmdline_args)
    actual_dict = vars(actual_args)
    assert actual_dict[arg_name_py] == "value_from_cmdline"

    # Now check that the env value is picked up if there is not cmdline arg
    cmdline_args = []
    for aname in all_arg_names:
        if not aname == arg_name:
            cmdline_args.append(aname)
            cmdline_args.append("value_from_cmdline")

    actual_args = get_args(cmdline_args)
    actual_dict = vars(actual_args)
    assert actual_dict[arg_name_py] == "value_from_env"

    # Now check that there is an error is there is no cmdline arg or env value
    monkeypatch.delenv(env_name, raising=True)
    with pytest.raises(SystemExit):
        get_args(cmdline_args)

    # pytest.fail()
