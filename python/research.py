from scapy.all import *
from scapy.layers.inet import *
import requests


def ping(): # Funkcja ma za zadanie wyciągnąć adres IP mojej maszyny
    import os
    output = os.popen('hostname -I').read()
    # print(output)
    return output

def network_addr(): # Funkcja ma za zadanie wyodrębnić trzy pierwsze oktety z pozyskanego adresu z funkcji ping()
    ping_addr = ping()
    ping_addr_bezSpacji = ping_addr.strip()
    network = []
    dot_counter = 0

    for i in ping_addr_bezSpacji:
        if i == ".":
            dot_counter += 1
            if dot_counter == 3:
                break
        network.append(i)
    string_network = "".join(network)
    # print(string_network)
    return string_network


def vm_ping(): # Funkcja ma za zadanie przeskanować sieć w zakresie ostatniego oktetu, wyszukać aktywne adresy IP i wrzucić je do listy
    vm_UP = []
    adres = f"{str(network_addr())}."
    for ip in range(20, 30):
        vms = f"{adres}{str(ip)}"
        packet = IP(dst=vms, ttl=20) / ICMP()
        reply = sr1(packet, timeout=2)
        # print(vms)
        if reply:
            # print(vms, "IS ONLINE")
            vm_UP.append(vms)
        else:
            # print(vms, "DOWN")
            continue
    # print(f"Znalezione aktywne adresy: {vm_UP}")
    return vm_UP


def port_scanner(): # Funkcja skanuje porty na znalezionych maszynach i prezentuje je w formie słownika
    open_ports = {}
    for addr in vm_ping():
        port_list = []
        for port in range(20, 81):
            pakiet = IP(dst=addr) / TCP(dport=port, sport=random.randint(10000, 30000), flags="S")
            response = sr1(pakiet)
            if (str(response.getlayer(TCP).flags)) == "SA":
                port_list.append(port)
                # print(f"Port: {port}")
            open_ports[addr] = port_list
            # print(str(response.getlayer(TCP).flags))
    print(f"Znaleziono otwarte porty na aktywnych maszynach w sieci: {open_ports}")
    print()
    return open_ports
