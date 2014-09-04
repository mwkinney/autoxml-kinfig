#! /usr/bin/env python

from __future__ import print_function
import re
from time import time
from glob import glob
from shutil import move
from sys import exit
from os import remove
from tempfile import NamedTemporaryFile as namedtemporaryfile

GREETING = ("""'autoxml-kinfig' v1.1 - bulk file update utility
Conception, design and programming by Mark Kinney
Use at your own peril, no warranty or support provided 
Ctrl-C to exit at any time\n""")

END = ("\nPress ENTER to exit") #testing only

def snapshothandler():
    start = time() 
    dir_list = [] 
    #dir_list += glob(rootdir + '/*/*/???????????????/???????/???.??????')
    #dir_list += glob(rootdir + '/*/*/???????????????/???.??????')  
    dir_list += glob(rootdir + '/*/???????????????/???????/???.??????') 
    dir_list += glob(rootdir + '/*/???????????????/???.??????')  
    errors = []
    for d in dir_list: 
        try:
            with open (d) as input:
                with namedtemporaryfile('w+', delete=False) as output:
                    for line in input:
                        if 'aspnet_isapi.dll" resourceType="Unspecified"' in line:
                            break #this should go the next file in dir_list
                        output.write(re.sub ('</handlers>', '  <add name="SnapshotHandler2" path="*.snapshot" verb="*" modules="IsapiModule" scriptProcessor="C:\Windows\Microsoft.NET\Framework64\\\\v2.0.50727\\\\aspnet_isapi.dll" resourceType="Unspecified" preCondition="classicMode,runtimeVersionv2.0,bitness64" />\n    </handlers>', text,
                        flags=re.IGNORECASE | re.MULTILINE))
            move(output.name, input.name)
        except EnvironmentError as e:
            errors.append(e.filename)
        try:
            remove(output.name)
        except EnvironmentError:
            pass
    end = time()
    if len(errors) > 0:
        print ("\nPermission errors for the following (check for read-only)"
            "\n", "\n".join(errors), sep="", end="\n")
    print ("\nAll done-\n",len(dir_list)," files found\n",
    "{0:.2f}".format(end - start)," seconds elapsed", sep="")
    raw_input(END) #testing only

def update(rootdir, old_string, new_string):
    start = time() 
    dir_list = [] 
    dir_list += glob(rootdir + '/*/*/???????????????/???????/???.??????') 
    dir_list += glob(rootdir + '/*/*/???????????????/???.??????')  
    errors = []
    for d in dir_list: 
        try:
            with open (d) as input:
                with namedtemporaryfile('w+', delete=False) as output:
                    for text in input:
                        output.write(re.sub (old_string, new_string, text,
                        flags=re.IGNORECASE | re.MULTILINE))
            move(output.name, input.name)
        except EnvironmentError as e:
            errors.append(e.filename)
        try:
            remove(output.name)
        except EnvironmentError:
            pass
    end = time()
    if len(errors) > 0:
        print ("\nPermission errors for the following (check for read-only)"
            "\n", "\n".join(errors), sep="", end="\n")
    print ("\nAll done-\n",len(dir_list)," files found\n",
    "{0:.2f}".format(end - start)," seconds elapsed", sep="")
    raw_input(END)



# Need to build a list with all servers in one
print (GREETING)
server = "home/yenic"
rootdir = r'/' + server 
#server = "h1-chdevws13/www/mark"
#rootdir = r'//' + server 

# Adds snapshot handler if not in the file already
#snapshothandler()

# Old dev wordservice to new
old_string = 'http://chqapt2:9102/wordservice.asmx' 
new_string = 'http://h1-bds-wordservice-dev.int.thomsonreuters.com:8040/wordservice.asmx'
update (rootdir, old_string, new_string)

# Prod wordservice to new
old_string = 'http://ecomhawordservice.h1ecom.com:8040/wordservice.asmx' 
new_string = 'http://h1-bds-wordservice-dev.int.thomsonreuters.com:8040/wordservice.asmx'
update (rootdir, old_string, new_string)

# Old dev SMTP server to new
old_string = 'internal.hubbardone.net' 
new_string = 'h1-chdevws13.tlr.thomson.com'
update (rootdir, old_string, new_string)

# Prod smtpserver setting to new
old_string = 'smtpserver="localhost"' 
new_string = 'SMTPServer="h1-chdevws13.tlr.thomson.com"'
update (rootdir, old_string, new_string)

# ONI smtpserver to our new 
old_string = 'internal.onenorthhost.com' 
new_string = 'h1-chdevws13.tlr.thomson.com'
update (rootdir, old_string, new_string)

# Internal hostname to FQDN 
old_string = 'h1-chdevws13' 
new_string = 'h1-chdevws13.tlr.thomson.com'
update (rootdir, old_string, new_string)

# Prod environment to dev
old_string = 'Environment="prod"' 
new_string = 'Environment="dev"'
update (rootdir, old_string, new_string)

# Prod license server to dev
old_string = 'http://license60.firmconnect.com/WebService/LicenseServer.asmx' 
new_string = 'http://eg-ebdbuild-02.int.thomsonreuters.com/LicenseServer/WebService/LicenseServer.asmx'
update (rootdir, old_string, new_string)

# Old dev license server to new
old_string = 'http://h1-chbuildpt3/LicenseServer/WebService/LicenseServer.asmx' 
new_string = 'http://eg-ebdbuild-02.int.thomsonreuters.com/LicenseServer/WebService/LicenseServer.asmx'
update (rootdir, old_string, new_string)

# Prod proxy to dev
old_string = 'webproxy.westlan.com' 
new_string = 'webproxy.int.westgroup.com'
update (rootdir, old_string, new_string)

# Prod https setting to dev
old_string = 'Protocol="https"' 
new_string = 'Protocol="http"'
update (rootdir, old_string, new_string)

# Prod MatterDataService to dev
old_string = 'http://localhost/MatterDataService/MatterDataService.asmx?op=GetMatterDataByMatterNumber' 
new_string = 'http://chqapt2.tlr.thomson.com:9098/MatterDataService.asmx?op=GetMatterDataByMatterNumber'
update (rootdir, old_string, new_string)

# New site deployment MatterDataService to dev
old_string = 'MatterDataWebService="http://"' 
new_string = 'MatterDataWebService="http://chqapt2.tlr.thomson.com:9098/MatterDataService.asmx?op=GetMatterDataByMatterNumber"'
update (rootdir, old_string, new_string)

# Prod SMTP Network Delivery to dev
old_string = 'SMTPUseNetworkDelivery="false"' 
new_string = 'SMTPUseNetworkDelivery="true"'
update (rootdir, old_string, new_string)

# Prod directory key name to dev
old_string = 'Directory key="H1ECOM"' 
new_string = 'Directory key="TLR"'
update (rootdir, old_string, new_string)

# Prod directory key name to dev
old_string = 'directoryName="H1ECOM"' 
new_string = 'directoryName="TLR"'
update (rootdir, old_string, new_string)

# Prod LDAP to dev
old_string = 'LDAP://EG-H1DC-A01.H1ECOM.COM' 
new_string = 'LDAP://chopsut1.hubbardone.net'
update (rootdir, old_string, new_string)

# Prod Webfarm to dev
old_string = '<WebFarmInfo loadBalanced="true">' 
new_string = '<WebFarmInfo loadBalanced="false">'
update (rootdir, old_string, new_string)
