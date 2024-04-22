from hadb import *
from time import time

flag = False

while not flag:
    path = 'docker_hadb.csv'
    ha_list = []
    results = []
    with open(path) as file_obj:
        reader_obj = csv.reader(file_obj)
        for p in reader_obj:
            if not "#" in str(p):
                ha_list.append(p)

    if not ha_list:
        exit()

    for p in ha_list:
        print(p)
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
