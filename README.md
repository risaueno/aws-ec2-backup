# aws-ec2-backup
# AWS Lambda Snippet to create scheduled back ups of EC2 Instances

- This lambda snippet gets all instances tagged "backup" or "Backup" and saves the snapshot
- Snapshot are named "AUTOBACKUP: " + Name tag
- This Lambda snippet can be scheduled to run, for example, once a day
- 'AWS EC2 backup Lambda snippet 2' deletes old snapshots created with this code
