import requests
from urllib3.exceptions import InsecureRequestWarning
from dataclasses import dataclass, field
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = 'https://localhost'
s = requests.Session()

@dataclass
class NessusClient:
    _port: int
    _token: str = ""
    _scanId: str = ''

    def make_post_request(self, path, data):
        return s.post(f'{url}:{self._port}{path}', headers={"X-Cookie":f'token={self._token}'}, data=data, verify=False)

    def make_get_request(self, path):
        return s.get(f'{url}:{self._port}{path}', headers={"X-Cookie":f'token={self._token}'}, verify=False)

    def start_session(self, username, password):
        response = self.make_post_request('/session', {'username':username,'password':password})
        if response.ok:
            self._token = response.json()['token']
            print(f'[+] {self._token}')
            return True
        raise Exception(response.text)
        
    def scan(self, ips: list):
        response = self.make_post_request('/scans', {
            "uuid": "ad629e16-03b6-8c1d-cef6-ef8c9dd3c658d24bd260ef5f9e66",
            "settings": {
                "name": "test",
                "enabled": "true",
                "description": "description test",
                "settings.text_targets":','.join(ips),
                "launch": "ON_DEMAND",
                "policy_id": 4,
                "agent_group_id": []
            }
        })

        if response.ok:
            self._scanId = response.json().id
        return response.text


    def status(self):
        return self.make_get_request('/scans/'+self._scanId).text


    def is_finish(self):
        return self.make_get_request('/'+self._scanId+'/latest-status').text

    def export(self):
        print('[+] Exporting')
        

# X-Cookie: token={token};
# print(session('nessus', 'nessus'))
#start_scan([1])
#print(s.cookies)

