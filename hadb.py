import os
import csv
import subprocess

def sshcmd(host, command, user=None, stdin=None, check=False):

    where = "%s" % host if user is None else "%s@%s" %(user, host)
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

def action(r1, r2, c1, c2, vip, dev, h1, h2):
    #h1 = active router IP, h2 = standby router IP
    #h3 = active container name, h4 = standby container name
    #h5 = virtual ip (endpoint), h6 = endpoint interface name
    active = health_check(r1)
    standby = health_check(r2)
    if active:
        cmd = "sudo docker exec "+c1+" ip addr add "+vip+" dev "+dev
        sshcmd(h1, cmd, user='vmadm')

        cmd = "sudo docker exec "+c2+" ip addr del "+vip+" dev "+dev
        sshcmd(h2, cmd, user='vmadm')
        return "active"

    elif standby:
        cmd = "sudo docker exec "+c2+" ip addr add "+vip+" dev "+dev
        sshcmd(h2, cmd, user='vmadm')
        return "standby"
    else:
        return "failed"
