import subprocess
import re

cmd_op = subprocess.run(["netsh","wlan","show","profiles"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode()

profiles = (re.findall("All User Profile     : (.*)\r", cmd_op))

list_wifi = list()

if len(profiles) != 0:
    for name in profiles:
        each_profile = dict()

        profile_info = subprocess.run(["netsh", "wlan", "show", "profiles", name],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode()

        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            each_profile["ssid"] = name
            password_profile = subprocess.run(
                ["netsh", "wlan", "show", "profiles", name, "key=clear"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode()
            password = re.search("Key Content            : (.*)\r", password_profile)

            if password == None:
                each_profile["password"] = None
            else:
                each_profile["password"] = password[1]

            list_wifi.append(each_profile)

for wifis in list_wifi:
    print(wifis)
            

