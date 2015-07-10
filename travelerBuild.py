import urllib2, base64,os,re
username="hejjun"
password="Connect8ons"
logMode="debug"
baseURI = "https://rtpmsa.raleigh.ibm.com/msa/projects/b/build.topsail/drivers/NTS20.0/"
currentURI = "";
labelURI = baseURI+"currentBuildLabel.txt"

class DownloadITEM:
	def __init__(self,relativeURI=str,fullURI=str):
		self.FullURL=fullURI;
		self.RelativeURL=relativeURI;

def logConsole(msg=str):
	global logMode;
	if logMode=="debug":
		print msg+"\n";

def BasicAuthRequest(url=str):
	global username;
	global password;
	request = urllib2.Request(url);
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)
	return request
#use the root path 
#skip the . .. folder and other no used files
def DownloadByURI(URI=str):
	global baseURI;
	global currentURI;
	regStr="<A HREF=.*?>"
	
	#result = urllib2.urlopen(BasicAuthRequest(buildURL))
	stageResult = re.findall(regStr,result.read())
	
	

	print result.read().strip();
def CreateStack(stackStage=list):
	global baseURI;
	global currentURI;
	skipRegList="^\.\./$|^/.*|.*;.*"
	
	tmp=[]
	for item in stackStage:
		itemSelf = item.split('\"')[1]
		if re.match(skipRegList,itemSelf) == None:
			itemSelf=itemSelf.split(';')[0];
			logConsole("matched uri: " + itemSelf);
			tmp.append(DownloadITEM(currentURI,baseURI+currentURI+itemSelf))
			
			
'''
buildFileLocationRelative=""
request = urllib2.Request(labelURI)
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
logConsole("Open the build folder");   
result = urllib2.urlopen(request)
labelName = result.read().strip();
logConsole("Get the build file lable "+labelName);
buildURL = baseURI+labelName;


if not os.path.exists(labelName):
	logConsole("Create folder "+labelName);
	os.makedirs(labelName)
else:
	logConsole("Folder alreay exist "+labelName);

logConsole("build URL is: "  + buildURL);
DownloadByURI(buildURL)
'''
f=open("d:\\test.htm");
result=f;
regStr="<A HREF=.*?>"
	

stageResult = re.findall(regStr,result.read())
CreateStack(stageResult);