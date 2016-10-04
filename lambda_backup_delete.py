#! /usr/bin/python

import boto3
import re
import datetime

iam = boto3.client('iam')
account_id = ['000000000000'] #Set your account ID here
regloop = ['eu-west-1','eu-west-2'] #Set your regions here

def lambda_handler(event, context):
    
    for r in regloop: 
        ec = boto3.client('ec2',region_name=r)
        ec2 = boto3.resource('ec2',region_name=r)
        
        def findTagValue(tags, tagName):
            for i in tags:
                if i['Key'] == tagName:
                    return i['Value']
            return 5
    
        snapshot_response = ec.describe_snapshots(OwnerIds=account_id)
    
        for snap in snapshot_response['Snapshots']:
            if not snap['Description'].startswith('AUTO-BACKUP'):
                continue
            print snap['Description']
            try:
                retention = findTagValue(ec2.Instance(ec2.Volume(snap['VolumeId']).attachments[0]['InstanceId']).tags, 'Retention')
            except:
                retention = 0
            d = ec2.Snapshot(snap['SnapshotId']).start_time + datetime.timedelta(days=int(retention))
            if datetime.datetime.now() > d.replace(tzinfo=None):
                print "DELETING..."
                ec.delete_snapshot(SnapshotId=snap['SnapshotId'])
                print "Deleted snapshot %s" % snap['SnapshotId']
            else: 
                print "Not deleting"
