import glob
import csv
import os
import glob

def getFloatIfPossible(value):
  try:
    junk = float(value)
    return junk
  except:# ValueError:
    return False

stdworkints = {1:1.5, 2:4.5, 3:8.5, 4:12.5, 5:16.5}
stdworkdecs = {1:3, 2:4, 3:4, 4:4, 5:0} #just make it 4 diff for std
# will need exceptionc ase for 1.5<x<2 cuz stdworkdecs slightly off

def stdwork(work):
    proc = getFloatIfPossible(work)
    if proc == False:
        return work
    # 1 matches [1-3) hours, 2 matches [3-7) hours, 3 matches [7-11) hours, 4 matches [11-14) hours, 5 matches 14+ hours
    # count 1 as 1 hours, 2 as 5 hours, 3 as 9 hours, 4 as 12.5 hours, 5 as 17.
    # take the int, map it to a number. then take the decimal, multiply it by the range to next mean (1 matches 3, 2 matches 4, 3 matches 3.5, 4 matches 3, 5 matches nothing cuz nothing above 5)
    # but 1.5 must match 3, 2.5 must match 6.5, 3.5 must match 10.5, 4.5 must match ??
    
    baseint = int(proc)
    gg = stdworkints[baseint] + (proc-baseint)*stdworkdecs[baseint]
    return int((gg * 100) + 0.5) / 100.0


print "All Folders in Directory or One Folder in Directory? (0 for all folders, 1 for one folder)"
trigger = int(raw_input())
if trigger:
        print "Year?"
        year = raw_input()
        print "term (0 for spring, 1 for fall)"
        term = int(raw_input())
        if term == 0:
            folder = "Spring Term " + year + '.csv'
        elif term == 1:
            folder = "Fall Term " + year + '.csv'
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
    if term != 'Fall' and term != 'Spring':
        for i in sp:
            if i == 'Fall' or i == 'Spring':
                term = i
                break
    
    year = sp[-1][:4]
    print term, year
    
    with open(cs,'r') as csvinput:
        with open('Std '+cs,'w') as csvoutput:
            writer = csv.writer(csvoutput,lineterminator='\n')
            r = csv.reader(csvinput)
            am = []
            row0 = r.next()
            row0.insert(6, 'Std Workload Q')
            am.append(row0)
            if int(year) >= 2015 or (int(year) == 2014 and term == 'Fall'):
                for line in r:
                    line.insert(6, line[5]) # already standardized
                    am.append(line)
            else:
                for line in r:
                    line.insert(6, stdwork(line[5]))
                    am.append(line)
            writer.writerows(am)
print 'DELETED'
for cs in originals:
    os.remove(cs)
