import os
import csv
import subprocess

def sshcmd(host, command, user=None, stdin=None, check=False):
    host = host.strip()
    where = user+"@"+ host
    print("sssssssssssssssssssssssssssssssssssssss", where)
    result = subprocess.run(["ssh", where, command],
                           shell=False,
                           stdin=stdin,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           check=check)
    return result

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


def d_action(r1, r2, c1, c2, vip, dev, h1, h2):
    #h1 = active router IP, h2 = standby router IP
    #h3 = active container name, h4 = standby container name
    #h5 = virtual ip (endpoint), h6 = endpoint interface name
    active = health_check(r1)
    standby = health_check(r2)
    arptarget= vip.split('/')[0]
    if active:
        cmd = "sudo docker exec "+c1+" ip addr add "+vip+" dev "+dev
        garp = "sudo docker exec "+c1+" arping -c 1 -A "+arptarget
        sshcmd(h1, cmd, user='vmadm')
        m = sshcmd(h2, garp, user='vmadm')
        print(m)

        cmd = "sudo docker exec "+c2+" ip addr del "+vip+" dev "+dev
        sshcmd(h2, cmd, user='vmadm')
        return "active"

    elif standby:
        cmd = "sudo docker exec "+c2+" ip addr add "+vip+" dev "+dev
        sshcmd(h2, cmd, user='vmadm')
        garp = "sudo docker exec "+c2+" arping -c 1 -A "+arptarget
        m = sshcmd(h2, garp, user='vmadm')
        print(m)

        return "standby"
    else:
        return "failed"

def s_action(r1, r2, vip, dev, u1, u2, sudo):
    active = health_check(r1)
    standby = health_check(r2)
    arptarget= vip.split('/')[0]
    if active:
        if sudo:
            cmd = "sudo ip addr add "+vip+" dev "+dev
        else:
            cmd = "ip addr add "+vip+" dev "+dev

        if sudo:
            garp = "sudo arping -c 1 -A "+arptarget
        else:
            garp = "arping -c 1 -A "+arptarget
        sshcmd(r1, cmd, user=u1.strip())
        m = sshcmd(r1, garp, user=u1.strip())
        print(m)
        
        if sudo:
            cmd = "sudo ip addr del "+vip+" dev "+dev
        else:
            cmd = "ip addr del "+vip+" dev "+dev
        sshcmd(r2, cmd, user=u2.strip())
        return "active"

    elif standby:
        if sudo:
            cmd = "sudo ip addr add "+vip+" dev "+dev
        else:
            cmd = "ip addr add "+vip+" dev "+dev
        sshcmd(r2, cmd, user=u2.strip())

        if sudo:
            garp = "sudo arping -c 1 -A "+arptarget
        else:
            garp = "arping -c 1 -A "+arptarget
        m = sshcmd(r2, garp, user=u2.strip())
        print(m)

        return "standby"
    else:
        return "failed"


