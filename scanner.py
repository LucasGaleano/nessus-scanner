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

    port = 8888
    
    try:
        print('[+] Starting thread with ips:', ','.join(ipsGroup))
        container  = docker.start(port) #run a container
        print(f'[+] Container ID: {container.id}')
        nessus = NessusClient(port)
    except Exception as e:
        print(e)

    time.sleep(10) #wait for nessus

    while True:
        try:
            nessus.start_session('nessus', 'nessus')
            print(f'[+] Connected')
            break
        except Exception as e:
            print(f"[-] {e}, retry in 30 seconds")
            time.sleep(30)

    
    print(f'[+] Start Scan')
    response = nessus.scan(ipsGroup) #run scan
    print(response)

    while not nessus.is_finish():  #wait for the scan to end
        time.sleep(60)
        print(nessus.status())

    nessus.export() #download report

            

def divide_groups(ips, large):
    while ips:
      yield ips[:large]
      del ips[:large]



ips = [line.strip() for line in args.ips.readlines()]

executor = ThreadPoolExecutor(max_workers=4,thread_name_prefix="nessus")
for ipsGroup in divide_groups(ips,2):
    executor.submit(scanning,ipsGroup)


# client = DockerClient(args.image,args.replicas)
