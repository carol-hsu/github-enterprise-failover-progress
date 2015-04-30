#! /usr/local/bin/python3

import sys, os

PrimaryIP = sys.argv[1]
ReplicaIP = sys.argv[2]
LicenseFile = sys.argv[3]

SSHKeyFile = "/Users/carol/Carol_key_California.pem"

SSHPrimary = "ssh -i "+SSHKeyFile+" -p 122 admin@"+PrimaryIP
SSHReplica = "ssh -i "+SSHKeyFile+" -p 122 admin@"+ReplicaIP

#----- set hostname ----- 
os.system(SSHReplica + " \"echo '127.0.0.1 ip-" + "-".join(ReplicaIP.split("."))+"' | sudo tee -a /etc/hosts\"")
os.system(SSHReplica + " \"echo '"+PrimaryIP+" ip-" + "-".join(PrimaryIP.split("."))+"' | sudo tee -a /etc/hosts\"")
os.system(SSHPrimary + " \"echo '127.0.0.1 ip-" + "-".join(PrimaryIP.split("."))+"' | sudo tee -a /etc/hosts\"")
os.system(SSHPrimary + " \"echo '"+ReplicaIP+" ip-" + "-".join(ReplicaIP.split("."))+"' | sudo tee -a /etc/hosts\"")

#----- start github service on primary node -----
#import license, set configuration password, and apply setting
os.system("cat "+LicenseFile+" | "+SSHPrimary+" -- ghe-import-license")
os.system(SSHPrimary+" \"ghe-set-password\"")
os.system(SSHPrimary+" \"openssl x509 -fingerprint -in /etc/haproxy/ssl.crt -noout\"")
os.system(SSHPrimary+" \"ghe-ssl-certificate-setup -r\"")

#os.system(SSHPrimary+" \"ghe-config-apply\"")
###Wait for screen click
status = "N"
while not (status == "y" or status == "Y" or status==""):
	status = input("Clicked Save Setting? (y/Y)")

os.system("./ghe_replica_setup.py "+PrimaryIP+" "+ReplicaIP)
