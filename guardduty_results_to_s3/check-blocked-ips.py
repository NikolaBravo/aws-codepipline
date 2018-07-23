#!/usr/local/bin/python3.6
#Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
#
#    http://aws.amazon.com/apache2.0/

#or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

import boto3
import json
import os
import datetime
import pycurl
from time import gmtime, strftime
from dateutil import parser
import MySQLdb

gd = boto3.client('guardduty')
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
ec2 = boto3.client('ec2')
ddb = boto3.client('dynamodb')

bucket = "nk-gd-findings"
file_path = "/tmp/"
file_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime()) + "-findings.csv"
config_bucket = "nk-gd-config"
config_file = "gd-config.json"
date = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
network_connection_violation = 1
port_probe_violation = 1
db_name = "gd_findings"

get_db_config = s3.meta.client.download_file(config_bucket, config_file, config_file)

def get_db_config():
    content_loads = json.load(open(config_file))
    global db_user
    global db_password
    global db_host
    global db_port

    db_user = content_loads['databaseconfig']['dbusername']
    db_password = content_loads['databaseconfig']["dbpassword"]
    db_host = content_loads['databaseconfig']["dbhost"]
    db_port = int(content_loads['databaseconfig']["dbport"])
    return(db_user)

get_db_config()


conn = MySQLdb.connect(db_host, user=db_user,port=db_port,
                           passwd=db_password, db=db_name)

c = conn.cursor()
ips = c.execute("SELECT offender_ip FROM attacks;")

for ip in c.fetchall():
    timestamp = c.execute("SELECT last_seen FROM attacks WHERE offender_ip=\"%s\";" % (ip[0]))
    for time in c.fetchall():
        print("%s %s" % (time[0], ip[0]))
    #print("c.execute(SELECT last_seen FROM attacks WHERE offender_ip=\"%s\";" % (ip[0]))
print(ips)



#Used to parse the JSON Serialization for time - REQUIRED
def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def block_ip():
    if offender_ip in current_ips:
        print("%s is already blocked in the NACL %s" % (offender_ip, nacl_id))
        write_db()
    else:
       # ec2.create_network_acl_entry(CidrBlock=(offender_ip + "/32"), Egress=False, NetworkAclId=nacl_id, Protocol="-1", RuleAction='deny', RuleNumber=current_rule_numbers[-1] + 1)
        print("Blocked IP %s/32 for attacking %s on port %s" %(offender_ip, instance_id, attacked_port))
        write_db()