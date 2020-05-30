with open("wiki.vi.model.txt", "r") as files:
    with open("vocab.txt", "w") as files_w:
        for x in files:
             files_w.write(x.split()[0])
             files_w.write("\n")