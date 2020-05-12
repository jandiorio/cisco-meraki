#!/usr/bin/env python
import os
import time
from pprint import pprint
from meraki.meraki_api import meraki_api

def main():
    pass

if __name__=="__main__":
    """ main entry point to application """

    # Instantiate the meraki api object
    meraki = meraki_api("https://dashboard.meraki.com")

    # Set Organization Id
    org_id = os.environ.get("MERAKI_ORG_ID")
    # Get the list of orgs
    orgs = meraki.get_organizations().json()

    # ----------------------------------------
    # Get details of the org
    # ----------------------------------------
    # org_details = meraki.get_organization(org_id)
    # print(org_details)
    # print(org_details.json())
    # pprint(orgs)
    # for org in orgs:
    #     if org["id"] == org_id:
    #         my_org = org

    # org = [ org for org in orgs if org["id"] == org_id ][0]

    # pprint(org)
    # pprint(meraki.get_organization(org_id).json())

    # ----------------------------------------
    # Add a network
    # ----------------------------------------
    # payload = [
    #     {
    #         "name": "jeff_a_network",
    #         "timeZone": "America/Denver",
    #         "organizationId": org_id,
    #         "type": "appliance",
    #     },
    #     {
    #         "name": "jeff_s_network",
    #         "timeZone": "America/Denver",
    #         "organizationId": org_id,
    #         "type": "appliance",
    #     },
    #     {
    #         "name": "tafsir_network",
    #         "timeZone": "America/Denver",
    #         "organizationId": org_id,
    #         "type": "appliance",
    #     },
    # ]
    # body = [
    #     {"resource": f"/networks/{net['id']}", "operation": "update", "body": net}
    #     for net in payload
    # ]
    # pprint(body)

    # networks = meraki.get_networks(org_id).json()

    # actions = []

    # for network in networks:
    #     # Get Body from payload
    #     body = [net for net in payload if network["name"] == net["name"]][0]

    #     # Build Action for Updating this network
    #     action = {
    #         "resource": f"/networks/{network['id']}",
    #         "operation": "update",
    #         "body": body,
    #     }
    #     # Add action to list of actions
    #     actions.append(action)
    # pprint(actions)
    # results = meraki.batch_action(org_id, actions)

    # for network in payload:
    # results = meraki.create_network(org_id, net)
    # use get networks to obtain the network-id matching the current name
    # net_id = [ net["id"] for net in networks if net["name"] == network["name"] ][0]
    # results = meraki.update_network(net_id, network)

    # pprint(results)

    # ----------------------------------------
    # Get Networks
    # ----------------------------------------
    # for org in orgs:
    #     print(f"getting networks for {org['id']}")
    #     networks = meraki.get_networks(org["id"])
    #     print()
    #     pprint(
    #         f"There are {len(networks.json())} networks associated with this org: {org['id']}"
    #     )

    # ----------------------------------------
    # Delete network
    # ----------------------------------------
    # results = meraki.delete_networks("N_609674799555341683")
    # time.sleep(5)

    # networks = meraki.get_networks(org_id)
    # print("Printing list")
    # print(networks.status_code)
    # pprint(networks.json())

    # for network in networks.json():
    #     devices = meraki.get_devices(network["id"])
    #     pprint(
    #         f"There are {len(devices.json())} devices associated with network: {network['id']}"
    #     )

    # ----------------------------------------
    # get some api details
    # ----------------------------------------
    # api_calls = meraki.get_api_requests(org_id)
    # pprint(api_calls)
    # pprint(api_calls.json())

    # ----------------------------------------
    # get clients on network
    # ----------------------------------------
    networks = meraki.get_networks(org_id).json()
    for network in networks:
        network_id = network["id"]
        clients = meraki.get_network_clients(network_id).json()
        pprint(clients)