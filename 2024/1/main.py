from typing import List, Tuple
import collections
import re


def parse_locations_file() -> Tuple[List, List]:
    l1 = []
    l2 = []
    with open('lists.txt', 'r') as f:
        while line := f.readline():
            line = line.strip()

            match = re.match('([\d]+)   ([\d]+)', line)

            l1_value = int(match.groups()[0])
            l2_value = int(match.groups()[1])

            l1.append(l1_value)
            l2.append(l2_value)
    assert len(l1) == len(l2), 'Lists of location ids are not of the same length.'

    return l1, l2

l1, l2 = parse_locations_file()

l1.sort()
l2.sort()
distance_sum = sum([abs(v1 - v2) for v1, v2 in zip(l1, l2)])

right_dict = collections.defaultdict(lambda: 0)
for v in l2:
    right_dict[v] += 1

sscore = 0
for v in l1:
    if v in right_dict:
        sscore += v * right_dict[v]


print(f'Distance sum: {distance_sum}')
print(f'Simmilarity score: {sscore}')