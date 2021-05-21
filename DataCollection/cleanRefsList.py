import bz2
import pickle
import re

# read the uncleaned refsList
sfile = bz2.BZ2File('refsList.bz2', 'rb')
refs = pickle.load(sfile)

print(len(refs))

newRefs = []

# remove non job posting refs and postings with extra text in them
for ref in refs:
	if re.search("^.*jobposting.*$", ref) != None and len(ref) == 76:
		newRefs.append(ref)

print(len(newRefs))

# convert to set for duplicates
mySet = set(newRefs)
print(len(mySet))

# convert back to list
newRefs = list(mySet)
print(len(newRefs))

# save to file
outputFileName = 'refsListCleaned.bz2'
sfile = bz2.BZ2File(outputFileName, 'w')
pickle.dump(newRefs, sfile)


