#! /usr/bin/env python

from __future__ import print_function
from time import time
from glob import glob
from shutil import move
from os import remove
from tempfile import NamedTemporaryFile as namedtemporaryfile
import lxml.etree

GREETING = ("""'autoxml-kinfig' v1.0 - bulk XML file update utility
Conception, design and programming by Mark Kinney
Use at your own peril, no warranty or support provided\n""")

def update(func_name, dir_list, element, attribute, attribute_setting):
    try:
        remove('ReadOnly_XML_files.txt')
    except EnvironmentError:
        pass
    errors = []
    xpath_namespaces = dict(re='http://schemas.microsoft.com/.NetConfiguration/v2.0')
    for d in dir_list: 
        try:
            with open (d) as input:
                with namedtemporaryfile('w+', delete=False) as output:
                    doc = lxml.etree.parse(input)
                    for item in doc.xpath('//re:{0}'.format(element), namespaces = xpath_namespaces):
                        if attribute not in item.attrib:
                            with open('Malformed_XML_files.txt', 'a+') as f1:
                                print (func_name,'\n',d,'\n',sep="", file=f1)
                            continue
                        else:
                            item.attrib[attribute] = attribute_setting
                    output.write(lxml.etree.tostring(doc))
            move(output.name, input.name)
        except EnvironmentError as e:
            errors.append(e.filename)
        try:
            remove(output.name)
        except EnvironmentError:
            pass
    if len(errors) > 0:
        with open('ReadOnly_XML_files.txt', 'a+') as f2:
            print (errors,'\n', sep="", file=f2)

print ('\n',GREETING, 'Ctrl-C to exit at any time\n',sep="")

start = time() 

#rootdir = ['/home/yenic'] #test

rootdir = ['//h1-chdevws13/www', '//h1-chdevws12/www', '//h1-chdevws12/www2',
        '//h1chdevws11/www', '//h1-chdevws13/qa', '//h1-chqaws12/www',
        '//h1-chqaws11/www']

try:
    remove('Malformed_XML_files.txt')
    remove('FilesFound_TimeToComplete.txt')
except EnvironmentError:
    pass

dir_list = [] 
[dir_list.extend(glob(''.join(rootdir) + '/*/*/???????????????/???????/???.??????')) for dir in rootdir]
[dir_list.extend(glob(''.join(rootdir) + '/*/*/???????????????/???.??????')) for dir in rootdir]

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

end = time()

with open('FilesFound_TimeToComplete.txt', 'a+') as f3:
    print (GREETING,"\nLast run-\n",len(dir_list)," files found\n",
    "{0:.2f}".format(end - start)," seconds elapsed", sep="", file=f3)

print ("All done-\n",len(dir_list)," files found\n",
"{0:.2f}".format(end - start)," seconds elapsed\n", sep="")
