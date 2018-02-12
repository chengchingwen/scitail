import json as jn
from numpy import argmax

ifile = "SciTailV1/dgem_format/input.jsonl"
ofile = "SciTailV1/dgem_format/output.jsonl"
eafile = input("filename(default = result.jsonl): ")
eafile = eafile if eafile != "" else "result.jsonl"

flag = False
pre_cmd = ''
count = 1
jump = 0

def print_sample(js):
    for key in ("premise", "hypothesis", "label", "predict" ):
        print("\t⋆{}: {}".format(key, js[key]))


def prompt(js):
    global flag
    global pre_cmd
    global count
    global jump

    edit = False

    r = input("?> ").strip()
    while True:
        if r == 'n':
            if edit:
                a = input("edited: keep without save?[y/N]:").strip()
                if a != 'y':
                    r = input("?> ").strip()
                    continue

            pre_cmd = r
            flag = False
            return True
        elif r == 'q':
            if edit:
                a = input("edited: keep without save?:[y/N]").strip()
                if a != 'y':
                    r = input("?> ").strip()
                    continue

            count = 0
            return False
        elif r == 'nw':
            if edit:
                a = input("edited: keep without save?:[y/N]").strip()
                if a != 'y':
                    r = input("?> ").strip()
                    continue

            pre_cmd = r
            flag = True
            return True
        elif len(r) > 2 and r[0] =='j':
            if edit:
                a = input("edited: keep without save?:[y/N]").strip()
                if a != 'y':
                    r = input("?> ").strip()
                    continue

            _, num = r.split()
            jump = int(num)
            flag = False
            return True
        elif r == 'w':
            ff.write(jn.dumps(js))
            ff.write("\n")
            edit = False
        elif r == 'e':
            description = input("description: ")
            js['description'] = description
            edit = True
        elif r == '' and (pre_cmd == 'n' or pre_cmd == 'nw'):
            r = pre_cmd
            continue
        elif r == 'hps':
            print(js.get("hypothesis_structure"))
        elif r == 'd':
            print(js)
        elif len(r) > 2 and r[0] == 's':
            _, key = r.split()
            v = js.get(key)
            if v:
                print(key,": ", v)
        else:
            print("\ntry again",
                  "h: help",
                  "n: next",
                  "q: quit",
                  "nw: next wrong",
                  "j + #: jump to number",
                  "e: add error description",
                  "w: write sample",
                  "hps: print hypothesis_structure",
                  "d: dump json",
                  "s + key: print value (opt: ['premise', 'hypothesis', 'label', 'hypothesis_structure', 'label_logits', 'label_probs', 'loss', 'predict'])\n", sep="\n")
        pre_cmd = r
        r = input("?> ").strip()


with open(ifile, "r") as fi, open(ofile, "r") as fo, open(eafile, "w+") as ff:
    label = ['neutral', 'entails']
    while count:
        fi.seek(0)
        fo.seek(0)
        for i, (il, ol) in enumerate(zip(fi, fo)):
            if jump > i:
                continue
            elif jump < i:
                break
            else:
                jump += 1
            ji,jo = jn.loads(il),jn.loads(ol)
            ji.update(jo)


            pred = label[argmax(ji["label_probs"])]
            ans = pred == ji["label"]
            ji["predict"] = pred

            if flag == True and ans == True:
                continue

            js = jn.dumps(ji)
            print(i,":", end="")
            print_sample(ji)
            # print(js)
            # print("predict: ", pred)
            print("correct" if ans else "wrong")

            keep = prompt(ji)
            if not keep:
                exit("[Exist]")
        

