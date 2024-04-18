import os
import csv

def get_ha_list(path):
    with open(path) as file_obj:
        reader_obj = csv.reader(file_obj)
        return reader_obj


def health_check(ip):
    hostname = ip
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False

    return pingstatus

def action(h1, h2, c1, c2, vip, dev):
    active = health_check(h1)
    standby = health_check(h2)
    if active:
        os.system("sudo docker exec "+c1+" ip addr add "+vip+" dev "+dev)
        os.system("sudo docker exec "+c2+" ip addr del "+vip+" dev "+dev)
        return "active"
    elif standby:
        os.system("sudo docker exec "+c2+" ip addr add "+vip+" dev "+dev)
        return "standby"
    else:
        return "failed"
