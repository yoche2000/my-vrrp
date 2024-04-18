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

    # action(h1, h2, '10.10.10.101/24', 'eth2', 'user1', 'user2')
    for p in ha_list:
        s = s_action(p[1], p[2], p[3], p[4], p[5], p[6])
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
