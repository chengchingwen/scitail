import os


inputfile = "SciTailV1/dgem_format/input.jsonl"
if os.path.exists(inputfile):
    print("exist")
else:
    with open(inputfile, "w+") as fw:
        with open("SciTailV1/dgem_format/scitail_1.0_structure_test.tsv", "r") as fr:
            for line in fr:
                pre,hyp,lab,hyp_str = line.rstrip().split("\t")
                fw.write("{{ \"premise\": \"{0}\", \"hypothesis\": \"{1}\", \"label\": \"{2}\", \"hypothesis_structure\": \"{3}\" }}\n".format(pre,hyp,lab,hyp_str))



