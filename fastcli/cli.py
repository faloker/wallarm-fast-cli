import sys
import os
from time import sleep

import click

from fastcli.fast_helper import FASTHelper
from fastcli.log import console
from fastcli.helpers import fast_error_handler


@click.group(
    help="Wallarm FAST CLI - A simple command line interface for Wallarm FAST."
)
@click.option(
    "--uuid",
    default="",
    envvar="WALLARM_UUID",
    type=str,
    help="You personal UUID to authorize API calls. Defaults to the value of the env variable WALLARM_UUID.",
)
@click.option(
    "--secret",
    default="",
    envvar="WALLARM_SECRET",
    type=str,
    help="You personal secret key to authorize API calls. Defaults to the value of the env variable WALLARM_SECRET.",
)
@click.pass_context
def cli(ctx, uuid, secret):
    ctx.obj = FASTHelper(wallarm_uuid=uuid, wallarm_secret=secret)


@cli.command("create", short_help="Create a new test run with provided parameters.")
@click.option("--name", "-n", required=True, help="Test run name.")
@click.option(
    "--node",
    "-N",
    required=True,
    help="Node name for test execution. No cloud, only node.",
)
@click.option(
    "--desc", "-D", default="", help="Short description. Defaults to empty decription."
)
@click.option("--policy", "-P", help="Policy name to apply.")
@click.option("--tags", "-T", help="Comma-separated tags to test run.")
@click.option(
    "--rps-total", "-Rt", type=int, help="The max number of concurrent requests."
)
@click.option(
    "--rps-per-url",
    "-Rb",
    type=int,
    help="The max number of concurrent requests for one baseline (unique url).",
)
@click.option(
    "--track/--no-track",
    default=True,
    is_flag=True,
    help="If set, then test execution will be tracked and all findings will be exported at the end.",
)
@click.option(
    "--out-file",
    "-o",
    help="Save report to file. Otherwise, the results will be output to stdout.",
)
@click.pass_obj
def create(
    fast, name, desc, tags, node, policy, rps_total, rps_per_url, track, out_file
):
    with fast_error_handler():
        test_run = fast.create_test_run(
            name, desc, tags, node, policy, rps_total, rps_per_url
        )

    console.info(
        "Name: {}\nState: {}\nID: {}".format(
            test_run["name"], test_run["state"], test_run["id"]
        )
    )

    if track:
        while True:
            with fast_error_handler():
                tr = fast.fetch_test_run(test_run["id"])

            done = tr["baseline_check_all_terminated_count"]
            left = tr["baseline_count"]
            state = tr["state"]

            if left:
                console.info(
                    "Auditing {}/{} [ {} % ]".format(
                        done, left, round(done / left, 2) * 100
                    )
                )
            else:
                console.info("Waiting for baselines...")

            if state != "running":
                break
            else:
                sleep(120)

    with fast_error_handler():
        report = fast.fetch_vulns_from_test_run(test_run["id"])

    if out_file:
        with click.open_file(out_file, "w+") as f:
            f.write(report)
    else:
        print(report)


@cli.command(
    "report",
    short_help="Get all findings from test run by id. Findings will be in JSON format.",
)
@click.option(
    "--test-run-id", "-id", required=True, help="Test run id to get issues from."
)
@click.option(
    "--out-file",
    "-o",
    help="Save report to file. Otherwise, the results will be output to stdout.",
)
@click.pass_obj
def report(fast, test_run_id, out_file):
    with fast_error_handler():
        report = fast.fetch_vulns_from_test_run(test_run_id)

    if out_file:
        with click.open_file(out_file, "w+") as f:
            f.write(report)
    else:
        print(report)


@cli.command(
    "check", short_help="Check that credentials (UUID and Secret key) are valid."
)
@click.pass_obj
def check(fast):
    with fast_error_handler():
        if fast.get_client_id():
            console.info("Credentials are valid.")
