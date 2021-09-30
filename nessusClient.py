import requests
from urllib3.exceptions import InsecureRequestWarning
from dataclasses import dataclass, field
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

url = 'https://localhost'
s = requests.Session()

@dataclass
class NessusClient:
    _token: str = field(init=False)
    _port: int
    _scanId: str = field(init=False)

    def make_post_request(self, path, data):
        return s.post(f'{url}:{self._port}{path}', data=data, verify=False)

    def make_get_request(self, path):
        return s.get(f'{url}:{self._port}{path}', verify=False)
        

    def start_session(self, username, password):
        response = self.make_post_request('/session', {'username':username,'password':password})
        if response.ok:
            self._token = response.json()['token']
            print(f'[+] {self._token}')
            return True
        raise Exception(response.text)
        
    def scan(self, ips: list):
        response = self.make_post_request('/scans', {
            "settings": {
                "name": "test",
                "description": "description test",
                "settings.text_targets":','.join(ips),
                "launch": "ON_DEMAND",
                "policy_id": 4,
            }
        })

        if response.ok:
            self._scanId = response.json().id
            return response.text
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

