import re
import sys

names = ['q1', 'q2', 'q3', 'q4', 'update', 'insert1', 'insert2', 'delete']


def get_millis(x):
    x = re.split(r'[:.]', x[9:])
    return 3600000 * int(x[0]) + 60000 * int(x[1]) + 1000 * int(x[2]) + 10 * int(x[3])


res = ''.join(sys.stdin.readlines())

res_array = list(map(lambda x: list(map(get_millis, re.findall(r'E.*', x))), res.split('-----')[:-1]))
average = [round(sum(x) / len(x)) for x in zip(*res_array)]

print(f'Average from {len(res_array)} tests')
for name, avg in dict(zip(names, average)).items():
    print(f'{name}: {avg} ms')
