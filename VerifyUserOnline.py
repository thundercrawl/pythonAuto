import urllib2, base64,os,re,tarfile
import platform


g_traveler_url="https://traveler3.notes.collabservsvt1.swg.usma.ibm.com/traveler"
g_supportOS=['Linux','Windows']
g_basepath="d:/"# use /SVT/controler/tmp
g_result_path=g_basepath+"/verifyUserOnline/"
g_logMode="debug";
def logConsole(msg=str):
    global g_logMode;
    if g_logMode=="debug":
        print msg+"\n";
def logFinest(response,filename):
    global g_logMode;
    if g_logMode=="debug":
        f=open(g_result_path+'/'+filename,"w+")
        f.write(response)
        f.close()
		
def loginProcess(username,password):
    try:
	    login_logIndex=0
        request = urllib2.Request(g_traveler_url)
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        result = urllib2.urlopen(request)	
        
		
        logFinest(result.read(),g_username+"_login_"+login_logIndex)
        logFinest(result.info().dict.__str__,"_login_headers"+login_logIndex)
        result.close();
    except urllib2.HTTPError, e:
	    logFinest("Error as: "+e.message,);

#main process    
if platform.system() not in g_supportOS:
    print "Your system not support in this script "+platform.system()
    sys.exit()
else:
    print "System "+platform.system()+" Supported by scripts copyright sujj@cn.ibm.com"
#check dir ready
if not os.path.exists(g_basepath):
    print "g_basepath cannot found : "+g_basepath
    print "exit with error"
    exit(-1);
if not os.path.exists(g_result_path):
    logConsole("create folder "+g_result_path);
    os.mkdir(g_result_path)

username="Abbas_1710522_Cary@travelversebundle.svtrel.org"
password="Pa88w0rd"
#login process
logConsole("login process start for user "+username);
loginProcess("Abbas_1710522_Cary@travelversebundle.svtrel.org","Pa88w0rd");