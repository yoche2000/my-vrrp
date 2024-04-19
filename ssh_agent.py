from hadb import *

flag = False

while not flag:
    path = 'ssh_hadb.csv'
    ha_list = []
    results = []
    with open(path) as file_obj:
        reader_obj = csv.reader(file_obj)
        for p in reader_obj:
            ha_list.append(p)

    #sudo option. When ssh controlling, allow the use of sudo by making it True
    sudo = False

    # action(192.168.1.3, 192.168.1.2, '10.10.10.101/24', 'eth2', 'root', 'root', sudo)
    for p in ha_list:
        s = s_action(p[1], p[2], p[3], p[4], p[5], p[6], sudo)
        if s == 'active':
            current = p[1]
        elif s == 'standby':
            current = p[2]
        else:
            current = 'NA'

        d = {'name': p[0],
             'current': current,
             'state': s}
        results.append(d)

    for item in results:
        print(item)

    flag = True
