import re
import gzip
import shutil

# Get image from content
def getImageFromContent(content):
    matches = re.search('src="([^"]+)"', content)
    if matches != None :
        return matches.group(1)
    return None

# Make Gz file compress
def makeGzFile(filePath):
    filePathGzip = filePath + '.gz'
    with open(filePath , 'rb') as f_in, gzip.open(filePathGzip, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)