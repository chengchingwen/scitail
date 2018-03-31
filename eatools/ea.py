import json as jn
from numpy import argmax

models = ['dgem', 'decompatt', 'overlap']
while True:
    model = input(f"analyze model ({', '.join(models)}[or index]): ").strip()
    if model in models:
        break
    else:
        try:
            idx = int(model)
            model = models[idx]
            break
        except ValueError:
            print(f"{model} model not exist.")


predict_file = f"predictions/scitail_1.0_{model}_predictions_dev.jsonl"
eafile = input("filename(default = result.jsonl): ")
eafile = eafile if eafile != "" else "result.jsonl"

def get_legal_key(filename):
    with open(filename, "r") as f:
        l = f.readline()
        d = jn.loads(l)
        return list(d.keys())

key_descri = {'gold_label(label)' : 'Final entailment label for the premise=KB Sentence and hypothesis=Q+A as Sentence from {entails, neutral}',
              'predict' : 'final prediction',
              'sentence1(premise)' : 'the premise',
              'sentence2(hypothesis)' : 'the hypothesis',
              'sentence2_structure(hypothesis_structure)':'structure from the hypothesis in the same format as described in dgem_format/README.txt',
              'question' : 'Original question',
              'answer' : 'Answer to the original question',
              'score' : 'entailment probs',
              'label_probs' : 'probs of labels {neutral, entails}',
              'label_logits' : 'logits of labels {neutral, entails}',
              }
legal_keys = get_legal_key(predict_file)
added_keys = ["premise", "hypothesis", "label", "predict", "hypothesis_structure"]
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
        elif r == 'kd':
            for k in key_descri:
                print(f"{k}: {key_descri[k]}")
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
                  "kd: print key description",
                  "hps: print hypothesis_structure",
                  "d: dump json",
                  f"s + key: print value (opt: ({', '.join(legal_keys+added_keys)}))\n", sep="\n")
        pre_cmd = r
        r = input("?> ").strip()


with open(predict_file, "r") as fp, open(eafile, "w+") as ff:
    label = ['neutral', 'entails']
    while count:
        fp.seek(0)
        for i, lp in enumerate(fp):
            if jump > i:
                continue
            elif jump < i:
                break
            else:
                jump += 1
            jp = jn.loads(lp)
            jp["premise"] = jp["sentence1"]
            jp["hypothesis"] = jp["sentence2"]
            jp["hypothesis_structure"] = jp["sentence2_structure"]
            jp["label"] = jp["gold_label"]

            pred = label[argmax(jp["label_probs"])]
            ans = pred == jp["label"]
            jp["predict"] = pred

            if flag == True and ans == True:
                continue

            js = jn.dumps(jp)
            print(i,":", end="")
            print_sample(jp)
            print("correct" if ans else "wrong")

            keep = prompt(jp)
            if not keep:
                exit("[Exist]")
        

#"""
