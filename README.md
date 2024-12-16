# AWS Cloud Cost Optimization: Automated EBS Snapshot Cleanup

## Overview
This project includes a Lambda function designed to optimize your AWS cloud costs by automatically deleting unnecessary EBS snapshots. The function identifies snapshots that are either:
- Not connected to any volume, or
- Associated with a volume not attached to a running EC2 instance.

By removing such snapshots, you can reduce your AWS storage costs.

## Features
- Identifies and deletes unused EBS snapshots.
- Handles edge cases, such as missing volumes.
- Ensures snapshots attached to active EC2 instances remain intact.

## Prerequisites
Before you begin, ensure the following:

1. **AWS Account**:
   - Access to an AWS account with sufficient permissions to manage EC2 snapshots and volumes.

2. **AWS IAM Role**:
   - Attach the following managed policies to the Lambda execution role:
     - `AmazonEC2ReadOnlyAccess`
     - `AmazonEC2FullAccess`

3. **Python Environment**:
   - Python 3.7 or higher installed on your local machine.

4. **Boto3 Library**:
   - Install the AWS SDK for Python (boto3) using the following command:
     ```bash
     pip install boto3
     ```

## File Structure
- `script.py`: Contains the Lambda function code.

## Lambda Function Code
The function logic is encapsulated in the `lambda_function()` defined in `script.py`.

### Key Functions
1. **Retrieve Snapshots**:
   Uses `describe_snapshots` to fetch all snapshots owned by the account.
2. **Identify Active EC2 Instances**:
   Retrieves all running EC2 instance IDs.
3. **Delete Unnecessary Snapshots**:
   Iterates through snapshots and deletes those not connected to active resources.

## Usage Instructions

1. **Setup Environment**:
   - Clone the project repository to your local machine.
   - Ensure your AWS credentials are configured. Run:
     ```bash
     aws configure
     ```
   - Install dependencies:
     ```bash
     pip install boto3
     ```

2. **Upload to AWS Lambda**:
   - Compress `script.py` into a `.zip` file.
   - Create a new Lambda function in the AWS Management Console.
   - Upload the `.zip` file.

3. **Test the Function**:
   - Use the AWS Lambda Console to create a test event.
   - Invoke the function and review logs for deleted snapshots.

4. **Schedule the Function**:
   - Use Amazon EventBridge (CloudWatch Events) to trigger the Lambda function periodically.
     Example: Schedule the function to run weekly.

## Example Logs
```
Deleted EBS Snapshot snap-0123456789abcdef0 as it was not connected with a volume
Deleted EBS Snapshot snap-0abcdef0123456789 as it was taken from a volume not attached to any running instance.
```

## Error Handling
- **InvalidVolume.NotFound**:
  Handles the case where a snapshot references a volume that no longer exists.

## Notes
- Test the function in a non-production environment before deployment.
- Review AWS Billing and Cost Management reports to measure the cost savings after implementing this solution.

## Future Enhancements
- Add support for excluding snapshots based on tags.
- Generate a report of deleted snapshots for auditing purposes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

