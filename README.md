# Description     
Wallarm FAST CLI - A simple command line interface for [Wallarm FAST](https://wallarm.com/products/fast/). For now, this tool can be used in CI system to create test runs and retrieve detected vulnerabilities.

# Installation
To install the latest release from PyPI, you can run the following command:   
`pip install wallarm-fast-cli`   
Also, you can use docker image:   
`docker pull faloker/wallarm-fast-cli`

# Usage
```
Usage: fast-cli [OPTIONS] COMMAND [ARGS]...

  Wallarm FAST CLI - A simple command line interface for Wallarm FAST.

Options:
  --uuid TEXT    You personal UUID to authorize API calls. Defaults to the
                 value of the env variable WALLARM_UUID.
  --secret TEXT  You personal secret key to authorize API calls. Defaults to
                 the value of the env variable WALLARM_SECRET.
  --help         Show this message and exit.

Commands:
  check   Check that credentials (UUID and Secret key) are valid.
  create  Create a new test run with provided parameters.
  report  Get all findings from test run by id. Findings will be in JSON
          format.
```

Main purpose of this tool is to create test runs from CI system (i.e. Jenkins), it can be done with create command:
```
Usage: fast-cli create [OPTIONS]

Options:
  -n, --name TEXT             Test run name.  [required]
  -N, --node TEXT             Node name for test execution. No cloud, only
                              node.  [required]
  -D, --desc TEXT             Short description. Defaults to empty decription.
  -P, --policy TEXT           Policy name to apply.
  -T, --tags TEXT             Comma-separated tags to test run.
  -Rt, --rps-total INTEGER    The max number of concurrent requests.
  -Rb, --rps-per-url INTEGER  The max number of concurrent requests for one
                              baseline (unique url).
  --track / --no-track        If set, then test execution will be tracked and
                              all findings will be exported at the end.
  -o, --out-file TEXT         Save report to the file. Otherwise, the results will
                              be output to stdout.
  --help                      Show this message and exit.
```
Example of command to create test run:   
`fast-cli create -n awesome_run -N super_node -P my_policy -T fast,cli,test -Rt 200 -Rb 20`