#! /usr/bin/env python

from __future__ import print_function
from time import time
from glob import glob
from shutil import move
from os import remove
from tempfile import NamedTemporaryFile as namedtemporaryfile
from pprint import pprint
import lxml.etree

GREETING = ("""'autoxml-kinfig' v1.0 - bulk XML file update utility
Conception, design and programming by Mark Kinney
Use at your own peril, no warranty or support provided\n""")

def update(func_name, dir_list, element, attribute, attribute_setting):
    errors = []
    xpath_namespaces = dict(re='http://schemas.microsoft.com/.NetConfiguration/v2.0')
    for d in dir_list: 
        try:
            with open (d) as input:
                with namedtemporaryfile('w+', delete=False) as output:
                    print (input.name)
                    input.flush()
                    with open ('AsProcessed_TimeToComplete.txt', 'a+') as f2:
                            print (input.name, file = f2)
                    try:
                        doc = lxml.etree.parse(input)
                    except lxml.etree.XMLSyntaxError as s:
                        print ('\n',d,'\n',s,'\n',sep="")
                        with open('Malformed_XML_files.txt', 'a+') as f3:
                            print ('\n',d,'\n',s,'\n',sep="", file=f3)
                        continue
                    for item in doc.xpath('//re:{0}'.format(element), namespaces = xpath_namespaces):
                        if attribute not in item.attrib:
                            print (func_name,'\n',d,'\n',sep="")
                            with open('Malformed_XML_files.txt', 'a+') as f3:
                                print (func_name,'\n',d,'\n',sep="", file=f3)
                            continue
                        else:
                            item.attrib[attribute] = attribute_setting
                    output.write(lxml.etree.tostring(doc))
            move(output.name, input.name)
        except EnvironmentError as e:
            print ('\n',d,'\n',e,'\n',sep="")
            errors.append(e.filename)
        try:
            remove(output.name)
        except EnvironmentError:
            pass
    if len(errors) > 0:
        global error_list
        error_list = errors

print ('\n',GREETING, 'Ctrl-C to exit at any time\n',sep="")

start = time() 

rootdir = ['//h1-chdevws13/www', '//h1-chdevws12/www', '//h1-chdevws12/www2',
        '//h1chdevws11/www', '//h1-chdevws13/qa', '//h1-chqaws12/www',
        '//h1-chqaws11/www']

dir_list = [] 
for d in rootdir:
    dir_list.extend(glob(d + '/*/*/???????????????/???????/???.??????'))
for d in rootdir:
    dir_list.extend(glob(d + '/*/*/???????????????/???.??????'))
dir_list.sort(key=str.lower)

with open('FileList.txt', 'w+') as f1:
    print (GREETING,"\nAll files found.\n", sep="", file=f1)
    pprint (dir_list, stream=f1)

with open('AsProcessed_TimeToComplete.txt', 'w+') as f2:
    print (GREETING,"\nFiles as processed. See the bottom of the file for statistics.\n", sep="", file=f2)

with open('Malformed_XML_files.txt', 'w+') as f3:
    print (GREETING,"\nCorrupted XML files that will be skipped until fixed.\n", sep="", file=f3)

with open('AccessError_files.txt', 'w+') as f4:
    print (GREETING,"\nFiles with access errors, check them for read-only access. They will be skipped until fixed.",'\n', sep="", file=f4)

func_name = 'Webfarm'
element = 'WebFarmInfo'
attribute = 'loadBalanced'
attribute_setting = 'false'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'WordService'
element = 'ApplicationInfo'
attribute = 'WordWebService'
attribute_setting = 'http://h1-bds-wordservice-dev.int.thomsonreuters.com:8040/wordservice.asmx'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'Application SMTP'
element = 'ApplicationInfo'
attribute = 'SMTPServer'
attribute_setting = 'h1-chdevws13.tlr.thomson.com'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'ExceptionManager SMTP - ignore this unless the same file is listed twice (2 publisher elements, 1 has SMTPServer)'
element = 'publisher'
attribute = 'SMTPServer'
attribute_setting = 'h1-chdevws13.tlr.thomson.com'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'Environment'
element = 'ApplicationInfo'
attribute = 'Environment'
attribute_setting = 'dev'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'License server'
element = 'ApplicationInfo'
attribute = 'LicenseServer'
attribute_setting = 'http://eg-ebdbuild-02.int.thomsonreuters.com/LicenseServer/WebService/LicenseServer.asmx'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'Proxy'
element = 'ApplicationInfo'
attribute = 'ProxyAddress'
attribute_setting = 'webproxy.int.westgroup.com'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'HTTP protocol'
element = 'ApplicationInfo'
attribute = 'Protocol'
attribute_setting = 'http'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'MatterDataService'
element = 'ApplicationInfo'
attribute = 'MatterDataWebService'
attribute_setting = 'http://chqapt2.tlr.thomson.com:9098/MatterDataService.asmx?op=GetMatterDataByMatterNumber'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'SMTP NetworkDelivery'
element = 'ApplicationInfo'
attribute = 'SMTPUseNetworkDelivery'
attribute_setting = 'true'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'Directory key'
element = 'Directory'
attribute = 'key'
attribute_setting = 'TLR'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'Directory name'
element = 'Directory'
attribute = 'directoryName'
attribute_setting = 'TLR'
update (func_name, dir_list, element, attribute, attribute_setting)

func_name = 'LDAP'
element = 'parameter'
attribute = 'value'
attribute_setting = 'LDAP://chopsut1.hubbardone.net'
update (func_name, dir_list, element, attribute, attribute_setting)

with open('AccessError_files.txt', 'a+') as f4:
    pprint (error_list, stream=f4)

end = time()

with open('AsProcessed_TimeToComplete.txt', 'a+') as f2:
    print ("\nLast run-\n",len(dir_list)," files found\n",
    "{0:.2f}".format(end - start)," seconds elapsed", sep="", file=f2)

print ("All done-\n",len(dir_list)," files found\n",
"{0:.2f}".format(end - start)," seconds elapsed\n", sep="")
