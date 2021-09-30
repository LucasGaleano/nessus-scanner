import argparse
from concurrent.futures import ThreadPoolExecutor
import time
import threading
from nessusClient import NessusClient
from dockerClient import DockerClient


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--replicas', type=int, default=1)
parser.add_argument('-m', '--image', type=str)
parser.add_argument('ips', type=argparse.FileType('r'))
args = parser.parse_args()

docker = DockerClient(args.image)

def scanning(ipsGroup):
    print('[+] Starting thread with ips:', ','.join(ipsGroup))
    container  = docker.start(8888)
    print(f'[+] Container ID: {container.id}')
    try:
        nessus = NessusClient(8888)
    except Exception as e:
        print(e)

    time.sleep(10)

    while True:
        try:
            nessus.start_session('nessus', 'nessus')
            print(f'[+] Connected')
            break
        except Exception as e:
            print(f"[-] {e}, retry in 30 seconds")
            time.sleep(30)

    
    print(f'[+] Start Scan')
    response = nessus.scan(ipsGroup)
    print(response)
    while True:
        time.sleep(60)
        if nessus.is_finish():
            nessus.export()
            break
        else:
            print(nessus.status())

def divide_groups(ips, large):
    while ips:
      yield ips[:large]
      del ips[:large]



ips = [line.strip() for line in args.ips.readlines()]

executor = ThreadPoolExecutor(max_workers=4,thread_name_prefix="nessus")
for ipsGroup in divide_groups(ips,2):
    executor.submit(scanning,ipsGroup)


# client = DockerClient(args.image,args.replicas)
