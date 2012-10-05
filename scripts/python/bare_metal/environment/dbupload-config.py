#!/usr/bin/python

import MySQLdb, sys, json, socket
import traceback


len(sys.argv) 
if (len(sys.argv) < 2):
    print "Need at least 1 argument (zodiac.conf) and an optional argument of the hardware info text file"
    sys.exit()


#Hostname
hostname = socket.gethostname()

#Ip address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
ipaddress = s.getsockname()[0]
s.close()


fname1 = sys.argv[1]

if (len(sys.argv) >= 3):
    hwInfo = sys.argv[2]
if (len(sys.argv) >= 4):
    novaVersiontxt = sys.argv[3]


try:
    zodiacConfig = open(fname1, 'r').read().replace("'","\\'") 
    novaVersion = ""
    hardware = ""
    try:
        hardware = open(hwInfo, 'r').read().replace("'","\\'")          
    except NameError:
        pass
    try:
        novaVersion = open(novaVersiontxt, 'r').read().replace("'","\\'") 
    except NameError, e:
        print e
        pass

except Exception, e:
    print "Couldn't open that file. %s" % e
    sys.exit()
        
try:
    conn = MySQLdb.connect(host="174.143.186.41", # your host, usually localhost
                         user="zodiac", # your username
                          passwd="zodiac", # your password
                          db="pc_testing") # name of the data base
    
    
    query = " INSERT INTO openstack_hosts (host_name, ip_address, zodiacConfig, hardware, nova_version) " \
            + " VALUES ('%s','%s','%s','%s','%s') ON DUPLICATE KEY UPDATE zodiacConfig='%s' , hardware='%s' , nova_version='%s' ;" % ( hostname, ipaddress, zodiacConfig, hardware, novaVersion, zodiacConfig, hardware, novaVersion )
 
    x = conn.cursor()
    try:
       result = x.execute(query) 
       conn.commit()
    except Exception, err:
        print query
        print "error: %s \n\n " % (err)
        conn.rollback()
       
       
           
    conn.close()    

       
except Exception as e:
    print "Error uploading to database :   %s  " % e
    sys.exit()






    

