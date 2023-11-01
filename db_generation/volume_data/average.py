import re


def get_millis(x):
    x = re.split(r'[:.]', x[9:])
    return 3600000 * int(x[0]) + 60000 * int(x[1]) + 1000 * int(x[2]) + 10 * int(x[3])


with open('clear_res.txt') as f:
    res = f.read()

res_array = list(map(lambda x: list(map(get_millis, re.findall(r'E.*', x))), res.split('-----')[:-1]))
average = [sum(x) / len(x) for x in zip(*res_array)]
print(average)
print(sum(average) / len(average))
