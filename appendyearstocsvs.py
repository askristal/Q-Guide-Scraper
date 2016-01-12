import glob
import csv
import os

print "All Folders in Directory or One Folder in Directory? (0 for all folders, 1 for one folder)"
trigger = int(raw_input())
if trigger:
        print "Year?"
        yearz = raw_input()
        print "term (0 for spring, 1 for fall)"
        term = int(raw_input())
        if term == 0:
            folder = "Spring Term " + yearz + '.csv'
        elif term == 1:
            folder = "Fall Term " + yearz + '.csv'
        else:
            print "wtf"
            folder = None
            raise Exception
        originals = glob.glob('*' + folder)
else:
        originals = glob.glob('* Term *.csv')
for cs in originals:
    sp = cs.split(' ')
    term = sp[0]
    ssss = 1
    while term != 'Spring' and term != 'Fall':
        term = sp[ssss]
        ssss += 1
    year = sp[-1][:4]
    print term, year
    with open(cs,'r') as csvinput:
        with open('Post '+cs,'w') as csvoutput:
            writer = csv.writer(csvoutput,lineterminator='\n')
            r = csv.reader(csvinput)
            am = []
            row0 = r.next()
            row0.append('Year')
            row0.append('Term')
            am.append(row0)
            for line in r:
                line.append(year)
                line.append(term)
                am.append(line)
            writer.writerows(am)
print 'DELETED'
for cs in originals:
    os.remove(cs)
