import sys
import socket
import threading
from datetime import datetime

# Just trying to make a nice banner, lol
print(r"""
    ____                  __   ____            
   / __ \___ _   ______ _/ /  / __ \____  _____
  / / / / _ \ | / / __ `/ /  / / / / __ \/ ___/
 / /_/ /  __/ |/ / /_/ / /  / /_/ / /_/ (__  ) 
/_____/\___/|___/\__,_/_/   \____/ .___/____/  
                                /_/            
""")

print(r"""
 ______________    ___           __    ____                          
/_  __/ ___/ _ \  / _ \___  ____/ /_  / __/______ ____  ___  ___ ____
 / / / /__/ ___/ / ___/ _ \/ __/ __/ _\ \/ __/ _ `/ _ \/ _ \/ -_) __/
/_/  \___/_/    /_/   \___/_/  \__/ /___/\__/\_,_/_//_/_//_/\__/_/   
                                                                     
""")

choice = input("Do you want to scan IPv4 or IPv6 address? (4/6): ")
min_choice = input("Enter the Minimum Port Number: ")
max_choice = input("Enter the Maximum Port Number: ")
target = input("Target IP: ")

p_min = int(min_choice)
p_max = int(max_choice)

# Making it pretty
print("_" * 50)
print("\nScanning Target: " + target)
print("Scanning started at: " + str(datetime.now()))
print("_" * 50)

# Setting number of threads allowed at a time
thread_limit = 100
print_lock = threading.Lock()

def scan_port(ip_version, port):
    try:
        if ip_version == 4:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif ip_version == 6:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = s.connect_ex((target, port))
        if result == 0:  # If successful
            with print_lock:
                print(f"[*] Port {port} is open")
        s.close()
    except:
        pass # So you don't have to see every closed port, lol

def run_scan(ip_version):
    try:
        threads = []
        for port in range(p_min, p_max):
            while threading.active_count() > thread_limit:
                pass

            t = threading.Thread(target=scan_port, args=(ip_version, port))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    except KeyboardInterrupt:
        print("\nExiting! ")
        sys.exit()
    except socket.error:
        print("\nHost NOT responding! ")
        sys.exit()

if choice == '4':
    run_scan(4)
elif choice == '6':
    run_scan(6)
else:
    print("\nInvalid input! ")
