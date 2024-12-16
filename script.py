import boto3

def lambda_function():
    ec2 = boto3.client("ec2")

    # Get all Snapshots
    response = ec2.describe_snapshots(OwnerIds=['self'])

    # Get all ec2 instance IDS
    instance_resposne = ec2.describe_instances(filter=[{'Name': 'instance-state-name', 'values': 'running'}])
    active_instance_ids = set()

    for reservation in instance_resposne['Reservations:']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])
    
    # Iterate through each snapshot and delete if it's not attached to any volume or the volume is not attached to a running instance
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        if not volume_id:
            # Deleting the Snapshot because it is not connnected to a volume
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted EBS Snapshot {snapshot_id} as it was not connected with a volume")
        else:
            try:
                volume_response = ec2.describe_volumes(VolumeId=[volume_id])
                if not volume_response['Volumes']['0']['Attachments']:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Deleted EBS Snapshot {snapshot_id} as it was taken from a volume not attached to any running instance.")
            except ec2.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "InvalidVolume.NotFound":
                    ec2.delete_snapshot(snapshot_id)
                    print(f"Deleted EBS Snapshot {snapshot_id} as it's associated Volume was not found")



