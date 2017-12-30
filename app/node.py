import requests

NODE_URL = 'http://localhost:14685'


def get_node_info():
    return requests.post(NODE_URL,
                         headers={'X-IOTA-API-VERSION': '1.4.1'},
                         json={'command': 'getNodeInfo'}).json()
