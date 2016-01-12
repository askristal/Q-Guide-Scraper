import glob
def concatCSVs():
        fout=open('allyears.csv','a')
        first = True
        for cs in glob.glob('* Term *.csv'):
                print cs # IT SEES SPRING 2015 BUT DOESN'T ADD IT TO THE ALLYEARS CSV WTFFFFFF WHY IT WAS WORKING JUST A BIT AGO
                if first:
                        for line in open(cs):
                                fout.write(line)
                        first = False
                else:
                        hh = open(cs)
                        hh.next() #skip header
                        for line in hh:
                                fout.write(line)
                        hh.close()
        fout.close()
concatCSVs()
