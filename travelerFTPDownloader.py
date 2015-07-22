import sys
import ftplib
import urllib2, base64,os,re,tarfile
import platform
from ftplib import FTP
supportOS=['Linux','Windows']

if platform.system() not in supportOS:
    print "Your system not support in this script "+platform.system()
    sys.exit()
else:
    print "System "+platform.system()+" Supported by scripts copyright sujj@cn.ibm.com"
#gsa user pwd
username="hejjun"
password="Connect8ons"
#root uri of the build
baseURI = "https://rtpmsa.raleigh.ibm.com/msa/projects/b/build.topsail/builds/NTS20.0/"

#labelURI can be current build or other bvtpassed txt
labelURI = baseURI+"BVTPassedBuilds.txt"
localLabelFile="downloadLabel.txt"
logMode="debug";
debugLevel=2



def logConsole(msg=str):
    global logMode;
    if logMode=="debug":
        print msg+"\n";
	
		
def downloadFiles(path,destination):
#path & destination are str of the form "/dir/folder/something/"
#path should be the abs path to the root FOLDER of the file tree to download
    try:
        ftp.cwd(path)
        #clone path to destination
        
        os.mkdir(destination[0:len(destination)]+path)
        os.chdir(destination+path)
        
    except OSError:
        #folder already exists at destination
        pass
    except ftplib.error_perm:
        #invalid entry (ensure input form: "/dir/folder/something/")
        print "error: could not change to "+path
        sys.exit("ending session")

    #list children:
    filelist=ftp.nlst()
    logConsole(filelist.__str__());
    for file in filelist:
        if(re.match("^\..*",file)==None):
            try:
                #this will check if file is folder:
                ftp.cwd(path+file+"/")
                #if so, explore it:
                logConsole("change dir : " + path+file+"/")
                downloadFiles(path+file+"/",destination)
            except ftplib.error_perm:
                #not a folder with accessible content
                #download & return
                os.chdir(destination[0:len(destination)]+path)
                #possibly need a permission exception catch:
                ftp.cwd(path)
                logConsole("change server directory as : " +path);
                logConsole( os.path.join(destination+path,file) + " downloaded")
                try:
                    rt  = ftp.retrbinary("RETR "+file, open(os.path.join(destination+path,file),"wb").write)
                    logConsole(rt)
                except:
				    print "Unexpected error:", sys.exc_info()[0]
                    
            
    return

#get the label

request = urllib2.Request(labelURI)
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)   
result = urllib2.urlopen(request)
labelName = result.read().strip().split("\r\n");


buildURL = baseURI+labelName[labelName.__len__()-1].strip()+"/";
logConsole("Get the build directory  path  as \n"+buildURL);

#check local download record
baseSource="/projects/b/build.topsail/builds/NTS20.0/"
source=baseSource+labelName[labelName.__len__()-1].strip()+"/"
dest="D:/build/traveler/builds"

#add path initialized function
checkpth=''
for pth in baseSource.split('/'):
    checkpth = checkpth+'/'+ pth
    if not os.path.exists(dest+"/"+checkpth):
        os.mkdir(dest+checkpth)
		
if not os.path.exists(dest+"/"+localLabelFile):
	logConsole("Create local label "+localLabelFile);
	file = open(dest+"/"+localLabelFile,"w+")
	file.close()
else:
	logConsole("local lable file exist "+dest+"/"+localLabelFile);
localLabelfile_h=open(dest+"/"+localLabelFile,"a+")
downLoadReady = localLabelfile_h.read().strip().find(labelName[labelName.__len__()-1].strip());
logConsole("Search Label in label file as : "+str(downLoadReady) );
localLabelfile_h.close()
#download the build from start point
relativePath="Build_Output/webkit/"  #change to your relative path
startPoint=labelName[labelName.__len__()-1].strip()+"/"+relativePath
checkpth=''
for pth in startPoint.split('/'):
    checkpth = checkpth+'/'+ pth
    if not os.path.exists(dest+"/"+baseSource+"/"+checkpth):
        os.mkdir(dest+"/"+baseSource+"/"+checkpth)
#download the build by the label set
if downLoadReady == -1:	
    ftp=FTP("rtpmsa.raleigh.ibm.com")
    #ftp.set_debuglevel(2)
    rt = ftp.login(username,password)
    logConsole(rt);
    logConsole("ftp source path \n"+source);
    downloadFiles(source+relativePath,dest)
	#add label file build number information
    localLabelfile_h=open(dest+"/"+localLabelFile,"a+")
    localLabelfile_h.write(labelName[labelName.__len__()-1].strip()+"\r\n")
    localLabelfile_h.close()
    ftp.quit()
else:
    logConsole("build already downloaded");

'''
#tar gz file
if not os.path.exists(dest+"/"+baseSource+labelName[labelName.__len__()-1].strip()+".tar.gz"):
    logConsole("Gzip file not exist,  create "+labelName[labelName.__len__()-1].strip()+".tar.gz")
    tar=tarfile.open(dest+"/"+baseSource+labelName[labelName.__len__()-1].strip()+".tar.gz","w:gz")
    tar.add(dest+"/"+baseSource+labelName[labelName.__len__()-1].strip()+"/",arcname="bar")
    tar.close()
else:
    logConsole("Upload gzip file exists");
	
#ftp upload
logConsole("upload bvt passed build to ftp server")
ftp=FTP("10.0.1.9")
#ftp.set_debuglevel(2)
ftp.login("ICSUser","Passw0rd")
ftp.cwd("/Projects/Traveler/builds")
rt=[]
line=ftp.retrlines('NLST',rt.append)

logConsole(rt.__str__())

# Init ftp uploader progress
class FtpUploadTracker:
    sizeWritten = 0
    totalSize = 0
    lastShownPercent = 0
    

    def __init__(self, totalSize):
        self.totalSize = totalSize
        self.percentComplete = 0
    def handle(self, block):
        #self.sizeWritten += block
        self.percentComplete += 1
        
        print(str(self.percentComplete) + "% percent complete")
			
sizeWritten = 0
totalSize = os.path.getsize(dest+baseSource+labelName[labelName.__len__()-1].strip()+".tar.gz")
logConsole('Total file size : ' + str(round(totalSize / 1024 / 1024 ,1)) + ' Mb')

uploadTracker = FtpUploadTracker(int(totalSize))
blockSize=totalSize/100;
	
if rt.__str__().find(labelName[labelName.__len__()-1].strip()) == -1 :
    logConsole("uploading file"+dest+baseSource+labelName[labelName.__len__()-1].strip()+".tar.gz")
    os.chdir(dest+baseSource)
    uploadFile=open(dest+baseSource+labelName[labelName.__len__()-1].strip()+".tar.gz", 'rb')
    ftp.storbinary("STOR " + labelName[labelName.__len__()-1].strip()+".tar.gz",uploadFile,blockSize,uploadTracker.handle)
    uploadFile.close()
    ftp.quit()
else:
    logConsole("File already uploaded, skip upload")
'''
print "Done!"