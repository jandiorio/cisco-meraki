#!/usr/bin/env python

import os
import sys
import json
import time
from pprint import pprint
import requests


class meraki_api:

    def __init__(self, dashboard, api_key=None):

        self.dashboard = dashboard
        self.api_key = api_key
        self.base_url = f"{self.dashboard}/api/v0"

        if not self.api_key:
            self.api_key = os.environ.get("X_CISCO_MERAKI_API_KEY")
            if not self.api_key:
                print(
                    "API key not found.  Please provide an API Key either \
                    through the contructor or environment varaible"
                )
                sys.exit(1)

        self.session = self.create_session()

    def create_session(self):
        """ build reusable session object """

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": self.api_key,
        }

        session = requests.session()
        session.headers = headers

        return session

    def get_organizations(self,):
        """ Obtain a list of organization the user with the api_key has access to"""

        _url = f"{self.base_url}/organizations"

        results = self.session.get(_url)

        if results.ok:
            return results
        else:
            print(f"Failed to get organizations:  {results.text}")
            sys.exit(1)

    def get_organization(self, org_id):
        """ get a specific org by org_id """

        _url = f"{self.base_url}/organizations/{org_id}"

        results = self.session.get(_url)

        if results.ok:
            return results
        else:
            print(f"Failed to retrieve org with org_id:  {org_id}")
            sys.exit(1)

    def get_networks(self, org_id):
        """ obtain all networks in the org """

        _url = f"{self.base_url}/organizations/{org_id}/networks"

        results = self.session.get(_url)

        if results.ok:
            return results
        else:
            print(
                f"Unable to retrieve a list of networks for org: {org_id}. \
            The status_code was: {results.status_code}. \
            The error text was:  {results.text}"
            )
            # sys.exit(1)
            return results

    def create_network(self, org_id, payload):
        """ create a new network """

        print(f"Creating new network:  {payload['name']}")

        # check if a network by that name exists.
        # 1. Get networks
        networks = self.get_networks(org_id).json()
        # 2. if network name already exists exit
        if payload["name"] in [net["name"] for net in networks]:
            print(f"A network with the name: {payload['name']} already exists.")
            sys.exit(1)

        _url = f"{self.base_url}/organizations/{org_id}/networks"

        results = self.session.post(_url, json=payload)

        if results.ok:
            return results
        else:
            print(
                f"Failed to create new network in org: {org_id} with this payload: {payload} \
                \nThe status code was: {results.status_code}"
            )

    def get_devices(self, network_id):
        """
        retrieve a list of the devices associated with the provided network_id
        """

        print(f"retrieving network devices for network id: {network_id}")

        _url = f"{self.base_url}/networks/{network_id}/devices"

        results = self.session.get(_url)

        if results.ok:
            return results
        else:
            print(
                f"Failed to retrieve network devices.  {results.status_code}\
                \n{results.text}"
            )

    def delete_networks(self, network_id):
        """ delete a network"""

        _url = f"{self.base_url}/networks/{network_id}"

        results = self.session.delete(_url)

        if results.ok:
            return results
        else:
            print(
                f"Failed to delete network.  {results.status_code}\
                \n{results.text}"
            )

    def update_network(self, network_id, payload):
        """ update a network"""

        print(f"Updating network:  {network_id}")

        _url = f"{self.base_url}/networks/{network_id}"

        results = self.session.put(_url, json=payload)

        if results.ok:
            return results
        else:
            print(f"Failed to update network: {network_id}")
            print(f"Status Code: {results.status_code}")
            print(f"Text Message: {results.text}")

    def get_api_requests(self, org_id):
        """ retrieve the api request logs for the org"""

        _url = f"{self.base_url}/organizations/{org_id}/apiRequests"

        results = self.session.get(_url)

        if results.ok:
            return results
        else:
            print("failed to get the API requests...")
            return results

    def batch_action(self, org_id, actions):

        _url = f"{self.base_url}/organizations/{org_id}/actionBatches"
        payload = {"confirmed": "true", "synchronous": "true", "actions": actions}
        results = self.session.post(_url, json=payload)
        if results.ok:
            print("batch update successful")
            return results
        else:
            print("batch update unsuccessful")
            return results


    def get_network_clients(self, network_id):
        """ get network clients """

        _url = f"{self.base_url}/networks/{network_id}/clients"

        results = self.session.get(_url)
        if results.ok:
            return results
        else:
            print(f"failed to get clients for network: {network_id}")
            return results


# if __name__ == "__main__":
#     """ main entry point to application """

#     # Instantiate the meraki api object
#     meraki = meraki_api("https://dashboard.meraki.com")

#     # Set Organization Id
#     org_id = os.environ.get("MERAKI_ORG_ID")
#     # Get the list of orgs
#     orgs = meraki.get_organizations().json()

#     # ----------------------------------------
#     # Get details of the org
#     # ----------------------------------------
#     # org_details = meraki.get_organization(org_id)
#     # print(org_details)
#     # print(org_details.json())
#     # pprint(orgs)
#     # for org in orgs:
#     #     if org["id"] == org_id:
#     #         my_org = org

#     # org = [ org for org in orgs if org["id"] == org_id ][0]

#     # pprint(org)
#     # pprint(meraki.get_organization(org_id).json())

#     # ----------------------------------------
#     # Add a network
#     # ----------------------------------------
#     payload = [
#         {
#             "name": "jeff_a_network",
#             "timeZone": "America/Denver",
#             "organizationId": org_id,
#             "type": "appliance",
#         },
#         {
#             "name": "jeff_s_network",
#             "timeZone": "America/Denver",
#             "organizationId": org_id,
#             "type": "appliance",
#         },
#         {
#             "name": "tafsir_network",
#             "timeZone": "America/Denver",
#             "organizationId": org_id,
#             "type": "appliance",
#         },
#     ]
#     body = [
#         {"resource": f"/networks/{net['id']}", "operation": "update", "body": net}
#         for net in payload
#     ]
#     # pprint(body)

#     networks = meraki.get_networks(org_id).json()

#     actions = []

#     for network in networks:
#         # Get Body from payload
#         body = [net for net in payload if network["name"] == net["name"]][0]

#         # Build Action for Updating this network
#         action = {
#             "resource": f"/networks/{network['id']}",
#             "operation": "update",
#             "body": body,
#         }
#         # Add action to list of actions
#         actions.append(action)
#     pprint(actions)
#     results = meraki.batch_action(org_id, actions)

#     # for network in payload:
#     # results = meraki.create_network(org_id, net)
#     # use get networks to obtain the network-id matching the current name
#     # net_id = [ net["id"] for net in networks if net["name"] == network["name"] ][0]
#     # results = meraki.update_network(net_id, network)

#     # pprint(results)

#     # ----------------------------------------
#     # Get Networks
#     # ----------------------------------------
#     for org in orgs:
#         print(f"getting networks for {org['id']}")
#         networks = meraki.get_networks(org["id"])
#         print()
#         pprint(
#             f"There are {len(networks.json())} networks associated with this org: {org['id']}"
#         )

#     # ----------------------------------------
#     # Delete network
#     # ----------------------------------------
#     results = meraki.delete_networks("N_609674799555341683")
#     time.sleep(5)

#     networks = meraki.get_networks(org_id)
#     print("Printing list")
#     print(networks.status_code)
#     pprint(networks.json())

#     for network in networks.json():
#         devices = meraki.get_devices(network["id"])
#         pprint(
#             f"There are {len(devices.json())} devices associated with network: {network['id']}"
#         )

#     # ----------------------------------------
#     # get some api details
#     # ----------------------------------------
#     api_calls = meraki.get_api_requests(org_id)
#     pprint(api_calls)
#     pprint(api_calls.json())
