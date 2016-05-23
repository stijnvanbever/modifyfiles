# import the modules that we need. (re is for regex)
import os, re

# define the directory constants
dirToProcess = 'C:/Stipad/projects/'
fileExt = [".sql",".SQL"]
ignoredDir = os.sep + 'target' + os.sep
makeBackup = False

#regular expression with 4 groups:
# group 1: insert into statement until just before closing bracket
# group 2: closing bracket + 0...* whitespace characters
# group 3: values statement until just before closing bracket
# group 4: closing bracket + 0...* characters
patternStr = r'(?i)(INSERT INTO MUT_MUTATION\s?\([^\)]*)(\)[\r\n\t\s]*)(values\s?\([^\)]*)(\).*)' 
#replacement string containing what to do with the groups and what to append
repStr = '\\1, C_CODE_MUTVALTYPE_IDF_TECH\\2\\3, \'EVOL\'\\4'

#search if the file contains the pattern we search for
def containsPattern(filePath):
	inputFile = open(filePath)
	fContent = inputFile.read()
	containsPattern = re.search(patternStr, fContent)
	if containsPattern:
		inputFile.close()
		return True
	else:
		inputFile.close()
		return False

def replaceStringInFile(filePath):
	# open the source file and read it, cannot directly write to file, so first read and close
	readFile = open(filePath)
	fContent = readFile.read()
	readFile.close()

	replacedText = re.sub(patternStr, repStr, fContent)

	oriFile = open(filePath, 'w')
	oriFile.write(replacedText)
	oriFile.close()

	if makeBackup:
		backupName = filePath+'.rep_backup'
		backupFile = open(backupName,'w')	
		backupFile.write(replacedText)
		backupFile.close()

	print("processed {}".format(filePath))

#walk through the directory and process all files with the given fileExtension that contain the regular expression in which we are interested
#if the file is inside the ignoredDir it will not be processed
def walkThroughDirAndProcess(dir):
	for subdir, dirs, files in os.walk(dir):
	    for file in files:
	        filepath = subdir + os.sep + file
	        if filepath.endswith(tuple(fileExt)) and containsPattern(filepath) and not ignoredDir in subdir:
	            replaceStringInFile(filepath)

#program
walkThroughDirAndProcess(dirToProcess)