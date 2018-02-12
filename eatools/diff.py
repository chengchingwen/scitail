from difflib import SequenceMatcher
import json


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


with open("input.jsonl", "r") as f:
    l = [json.loads(i) for i in f.readlines()]

seem = [False] * len(l)
flag = False
for i in range(len(l)):
    if seem[i]:
        continue
    seem[i] = True
    for j in range(i+1, len(l)):
        if not seem[j] and i != j:
            ps = similar(l[i]["premise"],l[j]["premise"])
            hs = similar(l[i]["hypothesis"], l[j]["hypothesis"])
            if ps > 0.7 and hs > 0.7:
                flag = True
                seem[j] = True
                print("premise similarity: {}".format(ps), "hypothesis similarity: {}".format(hs),l[j], sep="\n", end="\n\n")
    if not flag:
        continue
    print("base: ",l[i], sep="\n")
    print("======================================")
    #input(">")
    flag = False
