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

if __name__ == '__main__':
    # will work on if you have a host named ubly with ssh configuration
    out = sshcmd("192.168.20.16", "cat ~/.bashrc", check=False).stdout.decode()
    print(out)
