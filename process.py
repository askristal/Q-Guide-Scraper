# Pandas makes working with data tables easier
import pandas as pd
#BeautifulSoup is a library to parse HTML and XML documents
#import seaborn as sns #sets up styles and gives us more plotting options
from bs4 import BeautifulSoup as bs
import csv
import os
import glob


def getFloatIfPossible(value):
  try:
    junk = float(value)
    return junk
  except ValueError:
    return value
  except TypeError: #usually None
    return None
def getIntIfPossible(value):
  try:
    junk = int(value)
    return junk
  except ValueError:
    return value
  except TypeError: #usually None
    return None

def getScoreFromRow(row, checkIfFloat=True):
    ourdata = row.find_all('td', limit=4)[3].string
    if ourdata != None and checkIfFloat:
        ourdata = getFloatIfPossible(ourdata)
    return ourdata
def concatCSVs():
	fout=open('allyears.csv','a')
	first = True
	for cs in glob.glob('* Term *.csv'):
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
def extractCourseInfoToCSV(folder):
	columns = [\
	        'Course Category',\
	        'Course Number',\
	        'Course Title',\
	        'Overall Q',\
	        'Workload Q',\
	        'Would Recommend Q',\
	        'Enrollment',\
	        'Evaluations',\
	        'Response Rate',\
	        'Materials Q',\
	        'Assignments Q',\
	        'Feedback Q',\
	        'Section Q',\
	        'Elective Reason',\
	        'Concentration Req Reason',\
	        'Secondary Field or Language Req Reason',\
	        'Undergrad Core or Gen Ed Req Reason',\
	        'Expos Req Reason',\
	        'Foreign Lang Req Reason',\
	        'Pre-Med Req Reason',\
	        ] # Mispelled undergrad as undeergrad previously

	totaldata = []
	#testdata=[['123','abc',4,3.2,3.7,40,38],['num','title',4.9,1,1,2,2]]
	#df = pd.DataFrame(testdata, columns=columns)
	#df = df.append(pd.Series(['123','abc',4,3.2,3.7,40,38]), ignore_index=True)
	onlyfiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
	if '.DS_Store' in onlyfiles: onlyfiles.remove('.DS_Store')

	for course in onlyfiles:
	    path = folder + '/' + course
	    print path
	    with open(path, "r+") as f:
	        if 2 > 1:#try: TRUE
	            soup = bs(f, 'lxml')
	            warn = soup.find(attrs={'class': 'warning'})
	        
	            if not warn:
	                summstats = soup.find(id='summaryStats').string.strip().split(u'\xa0\xa0\xa0\n      ')
	                enrollment = getIntIfPossible(summstats[0].rsplit(' ',1)[1])
	                evaluations = getIntIfPossible(summstats[1].rsplit(' ',1)[1])
	                responserate = getFloatIfPossible(summstats[2][-7:-1].strip()) #-7 b/c percent never goes about 100.00%, -1 to cut off percentage sign
	            
	                toph1 = soup.find('h1').string.split(':', 1)
	                coursenum = toph1[0]
	                coursetitle = toph1[1].lstrip() #get rid of leading space
	                coursecategory = coursenum.split(' ', 1)[0]
	            
	                tbodies = soup.find_all('tbody')
	                if len(tbodies) >= 4:
	                    firsttablerows = tbodies[0].find_all('tr')
	                    overall = getScoreFromRow(firsttablerows[1])
	                    materials = getScoreFromRow(firsttablerows[2])
	                    assignments = getScoreFromRow(firsttablerows[3])
	                    feedback = getScoreFromRow(firsttablerows[4])
	                    section = getScoreFromRow(firsttablerows[5])
	                    
	                    workloadrow = tbodies[1].find_all('tr', limit=2)[1]
	                    workload = getScoreFromRow(workloadrow)
	                    recommendrow = tbodies[2].find_all('tr', limit=2)[1]
	                    recommend= getScoreFromRow(recommendrow)
	                    
	                    data = [coursecategory,\
	                            coursenum,\
	                            coursetitle,\
	                            overall,\
	                            workload,\
	                            recommend,\
	                            enrollment,\
	                            evaluations,\
	                            responserate,\
	                            materials,\
	                            assignments,\
	                            feedback,\
	                            section,\
	                            ] # if add another one, also modify else case of no tbodies
	                    reasonstablerows = tbodies[-1].find_all('tr')[1:]
	                    if len(reasonstablerows) == 7:
	                        reasons = []
	                        for reason in reasonstablerows:
	                            data.append(getIntIfPossible(\
	                                reason.find('img')\
	                                .get('alt')\
	                                .rsplit(' ', 1)[1][:-1] #truncate the % sign
	                            ))
                            elif len(reasonstablerows) == 4: # F2006
                                reasons = []
                                okaytopost = [0,1,3,6]
                                columnind = 0
                                for reason in reasonstablerows:
                                    while columnind not in okaytopost:
                                        data.append(0)
                                        columnind += 1
                                    data.append(getIntIfPossible(\
                                        reason.find('img')\
                                        .get('alt')\
                                        .rsplit(' ', 1)[1][:-1] #truncate the % sign
                                    ))
                                    columnind += 1
                            else:
	                        zeroes = [None] * 7
	                        data = data + zeroes

	                else:
	                    data = [coursecategory,\
	                            coursenum,\
	                            coursetitle]
	                    data = data + [None] * 17

	                        
	                totaldata.append(data)
	        f.close()

	df = pd.DataFrame(totaldata, columns=columns)
	df.to_csv(folder + '.csv', encoding='utf-8')

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
	extractCourseInfoToCSV(folder)
	#concatCSVs() #special just cuz bs spring 2015
else:
	folders = [f for f in os.listdir('.') if os.path.isdir(os.path.join('.', f))]
	if '.DS_Store' in folders: folders.remove('.DS_Store')
	if '.git' in folders: folders.remove('.git')
	if '.ipynb_checkpoints' in folders: folders.remove('.ipynb_checkpoints')
	for folder in folders:
		extractCourseInfoToCSV(folder)

	# concat into one big .csv
	concatCSVs()

print "Done" 


