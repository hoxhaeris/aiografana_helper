import asyncio
import base64
import concurrent.futures
import json
from getpass import getpass

from src.connector import get


class GrafanaAPI:
    base_url = None
    auth_bearer = None
    username = None
    password = None

    def __init__(self,
                 base_url: str = None,
                 auth_bearer: str = None,
                 username: str = None,
                 password: str = None,
                 ):
        self.base_url = base_url
        self.auth_bearer = auth_bearer
        self.username = username
        self.password = password
        self.token = base64.b64encode(f"{self.username}:{self.password}".encode('utf-8')).decode()

    def dashboard_dict(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(get(url=f"{self.base_url}/api/search",
                                           token=base64.b64encode(
                                               f"{self.username}:{self.password}".encode('utf-8')).decode()))

    def dashboard_uri(self, filter_group: list = None) -> list:
        dash_list = self.dashboard_dict()
        uri_list = []
        for dashboard_json in json.loads(dash_list):
            if dashboard_json['type'] == 'dash-db':
                try:
                    if filter_group is not None:
                        if dashboard_json['folderTitle'] in filter_group:
                            uri_list.append(dashboard_json['uri'])
                    else:
                        uri_list.append(dashboard_json['uri'])
                except KeyError:
                    pass
        return uri_list

    def dashboard_json(self, filter_group: list = None) -> dict:
        list_to_fetch = self.dashboard_uri(filter_group)
        loop = asyncio.get_event_loop()
        tasks_dict = {}
        for dashboard in list_to_fetch:
            tasks_dict.setdefault(dashboard)
            tasks_dict[dashboard] = loop.create_task(get(f"{self.base_url}/api/dashboards/{dashboard}", self.token))
        end_result = {}
        for pending_task in tasks_dict:
            end_result.setdefault(pending_task.replace('db/', ''))
            end_result[pending_task.replace('db/', '')] = json.loads(loop.run_until_complete(tasks_dict[pending_task]))
        return end_result

    @staticmethod
    def write_to_file(path: str, file_name: str, content: dict) -> None:
        if not path.endswith('/'):
            path = f"{path}/"
        with open(f"{path}{file_name}.json", "w") as f:
            f.write(json.dumps(content, indent=4))

    def save(self, content: dict, path: str = None) -> None:
        if path is None:
            path = ''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            [executor.submit(self.write_to_file, path, file_name, value) for file_name, value in content.items()]

