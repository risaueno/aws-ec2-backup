# lambda_backup_create.py
## AWS Lambda script to create back-up snapshots of EC2 Instances 
- Gets all instances tagged "backup" or "Backup" and saves the snapshot
- Snapshot are named "AUTO-BACKUP: " + Name tag
- Lambda script can be scheduled to run using AWS CloudWatch

# lambda_backup_delete.py
## AWS Lambda script to delete old back-up snapshots of EC2 Instances 
- Deletes old EC2 snapshots created with 'lambda_backup_create.py'
- Instance must have "Retention" tag with number of days you want to retain the snapshot, otherwise defaults to 5 days
- Lambda script can be scheduled to run using AWS CloudWatch
