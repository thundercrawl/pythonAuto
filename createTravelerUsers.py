print 'Generarting user list start-------------------->'

mail_user_prefix = 'mail'
mail_user_start_Num = '2501'
mail_user_total = '2500'
mail_password = 'passw0rd'
mail_serverDomain = 'icssvtbv55013/ibm'

mail_folder = 'mail'
mail_domain = 'ibm'
mail_template = 'mail9.ntf'


fHandle = open('c:\\userList'+mail_user_start_Num+'.txt','w+')
for each in range( int(mail_user_start_Num),int(mail_user_total)+int(mail_user_start_Num)):
    fHandle.write(mail_user_prefix+str(each)+';;;;'+mail_password+';;;'+mail_serverDomain+';'+mail_folder+
                  ';;;;;;'+mail_user_prefix+str(each)+'@'+mail_domain+';;;;'+mail_template+'\n')
fHandle.close()
print 'done!'


