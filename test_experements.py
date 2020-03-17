import re


# raw = 'Что (искали) со словом «"!клавиатура !для !дома"» — 2 показа в месяц'
# pattern = 'Что искали со словом «"!клавиатура !для !дома"» — (\d+) показа в месяц'
# p = re.compile(pattern)
# m = p.match(raw)
# print(m)
#
import sys
p = re.compile('Что искали со словом .+ — ([0-9 ]+) пока\w+')

p = re.compile('Что искали со словом .* — ([0-9 ]+) пока\w+')
m = p.match('Что искали со словом «"!ноутбук"» — 50 693 показа в месяц')
print(m)
# sys.exit()
print(m.group())
# 'ab'
print(m.group(0))
# 'ab'
print(m.group(1))
#print(m.group(2))