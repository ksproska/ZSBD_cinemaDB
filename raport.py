import re
import sys

names = ['q1', 'q2', 'q3', 'q4', 'update', 'insert', 'delete']

res = ''.join(sys.stdin.readlines())

raport_list = re.findall(r'(?s)SQL_ID.*?selected\.', res)
raport = '\n\n'.join(['\n\n'.join(i) for i in zip(names, raport_list)])

print(re.sub(r'\nPLAN_TABLE_OUTPUT.*\n-*\n', '', raport))