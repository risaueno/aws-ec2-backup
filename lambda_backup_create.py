#!/usr/bin/python

import boto3
import collections

def lambda_handler(event, context):
    
    regions = ['eu-west-1','eu-west-2','eu-west-3'] # set regions here
    
    for r in regions: 
        ec = boto3.client('ec2',region_name=r)

        reservations = ec.describe_instances(
                Filters=[
                    {'Name': 'tag-key', 'Values': ['backup', 'Backup']},
                ]
            )['Reservations']

        instances = sum(
            [
                [i for i in r['Instances']]
                for r in reservations
            ], [])

        print "Found %d instances that need backing up" % len(instances)

        for instance in instances:
            ins_id = instance['InstanceId']
            try:
                ins_name = [str(t.get('Value')) for t in instance['Tags'] if t['Key'] == 'Name'][0]
            except IndexError:
                ins_name = "Unnamed"

            for dev in instance['BlockDeviceMappings']:
                if dev.get('Ebs', None) is None:
                    continue
                vol_id = dev['Ebs']['VolumeId']
                print "Found EBS volume %s on instance %s ..." % (vol_id, ins_id)
                snap = ec.create_snapshot(VolumeId=vol_id, Description = "%s/%s" % ("AUTO-BACKUP: "+ins_name,ins_id),)
                print "Snapshot created"
