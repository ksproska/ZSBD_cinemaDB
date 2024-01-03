import re
import sys

names = ['q1', 'q2', 'q3', 'q4', 'update', 'insert', 'delete']
pattern_find = r'(?s)SQL_ID.*?selected\.'
pattern_delete = r'\nPLAN_TABLE_OUTPUT.*\n-*\n'

res = ''.join(sys.stdin.readlines())

raport_list = re.findall(pattern_find, res)
raport = '\n\n'.join(['\n\n'.join(i) for i in zip(names, raport_list)])

print(re.sub(pattern_delete, '', raport))