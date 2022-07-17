import ctypes
import random, requests
from threading import Thread, Lock, active_count

threadc = 100
clear_file = False
exclude_banned = True

if clear_file:
    open('usernames.txt', 'w')

lock = Lock()
usernames = []
proxies = open('proxies.txt','r').read().splitlines()
proxies = [{'https':'http://'+proxy} for proxy in proxies]
       

def thread():
    while idlists:
        idlist = idlists.pop()
        try:
            r = requests.post('https://users.roblox.com/v1/users', data={'userIds': idlist, 'excludeBannedUsers': exclude_banned}, proxies=random.choice(proxies), timeout=5).json()['data']
            usernames.extend([f['name']+'\n' for f in r])
        except Exception as e:
            idlists.append(idlist)

min = int(input('Minimum ID: ')) #1894000
max = int(input('Maximum ID: ')) #1994000

ids = list(range(min,max))
idlists = [ids[x:x+200] for x in range(0, len(ids), 200)]
print(f'\nLoaded {len(idlists)} ID lists for {len(ids)} IDs')

for i in range(threadc):
    Thread(target=thread).start()

while active_count() > 1:
    ctypes.windll.kernel32.SetConsoleTitleW(f'ID Scraper | Remaining ID lists: {len(idlists)}')

with open(f'usernames.txt', 'a') as f:
    f.writelines(usernames)

input('Finished!')
