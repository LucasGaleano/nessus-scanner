import argparse
from concurrent.futures import ThreadPoolExecutor
import time
import threading


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--replicas', type=int, default=1)
parser.add_argument('-m', '--image', type=str)
parser.add_argument('ips', type=argparse.FileType('r'))
args = parser.parse_args()


def scanning(ipsGroup):
    threadName = threading.get_native_id()
    print(f'i\'m Mr. meeseeks number {threadName} look at me!!!! i\'m going to scan this {ipsGroup}')
    time.sleep(10)
    print(f'finish, bye. atte Mr. meeseeks number {threadName}')

def divideGroups(ips, large):
    while ips:
      yield ips[:large]
      del ips[:large]



ips = [line.strip() for line in args.ips.readlines()]

executor = ThreadPoolExecutor(max_workers=4,thread_name_prefix="nessus")
for ipsGroup in divideGroups(ips,2):
    executor.submit(scanning,ipsGroup)


# client = DockerClient(args.image,args.replicas)
