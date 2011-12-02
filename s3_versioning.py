import boto

def configure_versioning(bucket_name, enable=True):
    """
    Enable versioning on a bucket.

    bucket_name  Bucket to be configured.
    enable       A boolean flag to indicate whether we are enabling
                 or disabling versioning for the bucket.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)

    # Get the current status of versioning on the bucket
    # and print the value out.
    config = bucket.get_versioning_status()
    print 'Current Versioning Status: ', config

    # Now enable versioning on the bucket.
    bucket.configure_versioning(enable)

    # Update the status of versioning and print the new value.
    config = bucket.get_versioning_status()
    print 'New Versioning Status: ', config


