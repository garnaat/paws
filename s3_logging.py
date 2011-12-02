import boto

def enable_logging(bucket_name,
                   log_bucket_name,
                   log_prefix=None):
    """
    Enable logging on a bucket.

    bucket_name     Bucket to be logged.
    log_bucket_name Bucket where logs will be written.
    log_prefix      A string which will be prepended to all log file names.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)
    log_bucket = s3.lookup(log_bucket_name)

    # First configure log bucket as a log target.
    # This sets permissions on the bucket to allow S3 to write logs.
    log_bucket.set_as_logging_target()

    # Now enable logging on the bucket and tell S3
    # where to deliver the logs.
    bucket.enable_logging(log_bucket, target_prefix=log_prefix)

def disable_logging(bucket_name):
    """
    Disable logging on a bucket.

    bucket_name     Bucket that will no longer be logged.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)
    bucket.disable_logging()
    
