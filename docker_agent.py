from hadb import *

flag = False

while not flag:
    path = 'docker_hadb.csv'
    ha_list = []
    results = []
    with open(path) as file_obj:
        reader_obj = csv.reader(file_obj)
        for p in reader_obj:
            ha_list.append(p)

    # action(h1, h2, 'clab-HALB-LB1',  'clab-HALB-LB2', '10.10.10.101/24', 'eth2')
    for p in ha_list:
        s = d_action(p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8])
        if s == 'active':
            current = p[3]
        elif s == 'standby':
            current = p[4]
        else:
            current = 'NA'

        d = {'name': p[0],
             'current': current,
             'state': s}
        results.append(d)

    for item in results:
        print(item)

    flag = True
