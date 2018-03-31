import json

rsfile = input('filename(default = result.jsonl): ')
rsfile = "result.jsonl" if rsfile == "" else rsfile

with open(rsfile, "r") as f:
    l = [json.loads(i) for i in f.readlines()]

d = {}
for j in l:
    c = d.get(j["description"])
    if c:
        c.append(j)
    else:
        d[j["description"]] = [j]

#print(d)
for key, val in d.items():
    print("type: ",key)
    print("percentage: {}\n".format(len(val)/ len(l)))

def pp(r):
    while True:
        s = input("\ne:{}> ".format(r)).strip()
        if s == 'n':
            return True
        elif s == 'q':
            return False
        else:
            print("n: next\nq: quit")

def print_sample(js):
    for key in ("premise", "hypothesis", "label", "predict" ,"hypothesis_structure"):
        print("\t⋆{}: {}".format(key, js[key]))

while True:
    r = input("?> ").strip()
    if r == "h":
        print("legal key: ")
        print(list(d.keys()))
    elif r == "q":
        exit("[Exit]")
    else:
        ok = d.get(r)
        if ok:
            for i in ok:
                if pp(r):
                    print_sample(i)
                else:
                    break
            else:
                print("That's all")
