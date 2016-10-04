#!/usr/bin/python

import boto3
import re
import datetime
iam = boto3.client('iam')

default_retention = 5 #Set default in case of empty retention tag
account_id = ['000000000000'] #Set account ID
regions = ['eu-west-1','eu-west-2'] #Set regions used

def lambda_handler(event, context):
    
    def findTagValue(tags, tagName):
        for i in tags:
            if i['Key'] == tagName:
                if i['Value'] == '':
                    return default_retention
                return i['Value']
        return default_retention
    
    for r in regions: 
        ec = boto3.client('ec2',region_name=r)
        ec2 = boto3.resource('ec2',region_name=r)
    
        snapshot_response = ec.describe_snapshots(OwnerIds=account_id)
    
        for snap in snapshot_response['Snapshots']:
            if not snap['Description'].startswith('AUTO-BACKUP'):
                continue
            print snap['Description']
            try:
                retention = findTagValue(ec2.Instance(ec2.Volume(snap['VolumeId']).attachments[0]['InstanceId']).tags, 'Retention')
            except:
                retention = 0
                
            print retention
            
            d = ec2.Snapshot(snap['SnapshotId']).start_time + datetime.timedelta(days=int(retention))
            if datetime.datetime.now() > d.replace(tzinfo=None):
                print "DELETING..."
                ec.delete_snapshot(SnapshotId=snap['SnapshotId'])
                print "Deleted snapshot %s" % snap['SnapshotId']
            else: 
                print "Not deleting"
                
