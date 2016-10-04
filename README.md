# aws-ec2-backup

# lambda_backup_create.py
# AWS Lambda snippet to create back-up snapshots of EC2 Instances 
- This lambda snippet gets all instances tagged "backup" or "Backup" and saves the snapshot
- Snapshot are named "AUTOBACKUP: " + Name tag
- This Lambda snippet can be scheduled to run, for example, once a day

# lambda_backup_delete.py
# AWS Lambda snippet to delete old back-up snapshots of EC2 Instances 
- Deletes old EC2 snapshots created with 'lambda_backup_create.py'
- Instance must have "Retention" tag with number of days you want to retain the snapshot, otherwise defaults to 5 days
- This Lambda snippet can be scheduled to run, for example, once a day
