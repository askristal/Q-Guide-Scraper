import shutil
import os
import time

print "All Folders in Directory or One Folder in Directory? (0 for all folders, 1 for one folder)"
trigger = int(raw_input())
if trigger:
        print "Year?"
        year = raw_input()
        print "term (0 for spring, 1 for fall)"
        term = int(raw_input())
        if term == 0:
            folder = "Spring Term " + year
        elif term == 1:
            folder = "Fall Term " + year
        else:
            print "wtf"
            folder = None
            raise Exception
        terms = [folder]
else:
        terms = [f for f in os.listdir('.') if os.path.isdir(os.path.join('.', f))]
        if '.git' in terms: terms.remove('.git')
        if '.ipynb_checkpoints' in terms: terms.remove('.ipynb_checkpoints')


for term in terms:
    wronged = [f for f in os.listdir(term) if os.path.isdir(os.path.join(term, f))]
    print wronged
    for folder in wronged:
        path = term + '/' + folder
        actualpath = term + '/' + folder
        insideitems = None
        insideitem = None
        while os.path.isdir(actualpath):
            # find next insideitem
            insideitems = os.listdir(actualpath)
            if '.DS_Store' in insideitems: insideitems.remove('.DS_Store')
            insideitem = insideitems[0]
            path = path + ' ' + insideitem
            actualpath = actualpath + '/' + insideitem
        # insideitem is html
        with open(path, "w") as f:
            f.write(' ')
        f.close()
        shutil.copyfile(actualpath, path)

