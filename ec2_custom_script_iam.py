import boto

# Create a restricted user using IAM

# The following JSON policy was generated using the
# AWS Policy Generator app.
# http://awspolicygen.s3.amazonaws.com/policygen.html

policy_json = """{
  "Statement": [
    {
      "Sid": "Stmt1316576423630",
      "Action": [
        "cloudwatch:PutMetricData"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}"""

def create_restricted_user(user_name):
    """
    Create a new user in this account.  The user will be
    restricted by the JSON policy document above.
    This function returns a tuple containing the access key
    and secret key for the new account.

    user_name The name of the new user.
    """
    iam = boto.connect_iam()
    user = iam.create_user(user_name)
    keys = iam.create_access_key(user_name)
    response = iam.put_user_policy(user_name,
                                   'CloudWatchPutMetricData',
                                   policy_json)
    fp = open('boto.cfg', 'w')
    fp.write('[Credentials]\n')
    fp.write('aws_access_key_id = %s\n' % keys.access_key_id)
    fp.write('aws_secret_access_key = %s\n' % keys.secret_access_key)
    fp.close()
             
    
