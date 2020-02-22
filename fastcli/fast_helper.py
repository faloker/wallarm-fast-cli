import sys
import requests
from requests.exceptions import RequestException
import json

from fastcli.log import console
from fastcli.exceptions import FASTError


class FASTHelper:
    def __init__(self, wallarm_uuid="", wallarm_secret=""):
        self.wallarm_headers = {
            "X-WallarmAPI-UUID": wallarm_uuid,
            "X-WallarmAPI-Secret": wallarm_secret,
            "Accept": "application/json",
        }

    def create_test_run(
        self,
        name,
        desc,
        tags,
        node,
        policy,
        rps_total,
        rps_per_url,
        stop_on_first_fail=False,
        type="node",
    ):
        url = "https://api.wallarm.com/v1/test_run"
        client_id = self.get_client_id()
        payload = {
            "name": name,
            "desc": desc,
            "node_id": self.get_node_id_by_name(client_id, node),
            "stop_on_first_fail": stop_on_first_fail,
            "type": type,
            "clientid": client_id,
        }

        if policy:
            payload["policy_id"] = self.get_test_policy_by_name(client_id, policy)

        if tags:
            payload["tags"] = tags.split(",")

        if rps_total:
            payload["rps"] = rps_total

        if rps_per_url:
            payload["rps_per_baseline"] = rps_per_url

        try:
            response = requests.post(url, headers=self.wallarm_headers, json=payload)
        except RequestException as e:
            console.error("Request issue:\n{}".format(e))

        if response.status_code in (200, 201):
            return response.json()["body"]
        else:
            raise FASTError("Unable to create test run:\n{}".format(response.json()))

    def fetch_test_run(self, test_run_id):
        url = "https://api.wallarm.com/v1/test_run/"
        payload = str(test_run_id)

        try:
            response = requests.get(url + payload, headers=self.wallarm_headers)
        except RequestException as e:
            console.error("Request issue:\n{}".format(e))

        if response.status_code != 200:
            raise FASTError(f"Unable to fetch test run:\n{response.json()}")

        return response.json()["body"]

    def fetch_vulns_from_test_run(self, test_run_id):
        url = "https://api.wallarm.com/v1/objects/vuln"
        payload = {
            "filter": {"testrun_id": [int(test_run_id)]},
            "offset": 0,
            "limit": 1000,
            "order_desc": False,
        }

        try:
            response = requests.post(url, headers=self.wallarm_headers, json=payload)
        except RequestException as e:
            console.error("Request issue:\n{}".format(e))

        if response.status_code != 200:
            raise FASTError(f"Unable to fetch vulnerabilities:\n{response.json()}")

        return json.dumps(response.json()["body"])

    def get_test_policy_by_name(self, client_id, name):
        url = "https://api.wallarm.com/v1/test_policy"
        payload = {
            "filter[name]": name,
            "order_by": "updated_at",
            "order_desc": True,
            "limit": 10,
            "clientid": client_id,
        }

        try:
            response = requests.get(url, params=payload, headers=self.wallarm_headers)
        except RequestException as e:
            console.error("Request issue:\n{}".format(e))

        if response.status_code == 200:
            try:
                policy_id = response.json()["body"]["objects"][0]["id"]
            except:
                raise FASTError(f"Unable to fetch policy:\n{response.json()}")
        else:
            raise FASTError(f"Unable to fetch policy:\n{response.json()}")

        return policy_id

    def get_node_id_by_name(self, client_id, node_name):
        url = "https://api.wallarm.com/v2/node"
        payload = {
            "order_by": "hostname",
            "limit": 1000,
            "filter[clientid][]": client_id,
            "filter[type]": "fast_node",
            "filter[hostname]": node_name,
        }

        try:
            response = requests.get(url, params=payload, headers=self.wallarm_headers)
        except RequestException as e:
            console.error("Request issue:\n{}".format(e))

        if response.status_code == 200:
            try:
                node_id = response.json()["body"][0]["id"]
            except:
                raise FASTError(f"Unable to find FAST node:\n{response.json()}")
        else:
            raise FASTError(f"Unable to find FAST node:\n{response.json()}")

        return node_id

    def get_client_id(self):
        url = "https://api.wallarm.com/v1/user"

        try:
            response = requests.post(url, headers=self.wallarm_headers)
        except RequestException as e:
            console.error("Request issue:\n{}".format(e))

        if response.status_code == 200:
            try:
                client_id = response.json()["body"]["clientid"]
            except:
                raise FASTError(f"Unable to get client id:\n{response.json()}")
        else:
            raise FASTError(f"Unable to get client id:\n{response.json()}")

        return client_id

