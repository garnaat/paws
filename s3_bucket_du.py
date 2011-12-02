import boto

def bucket_du(bucket_name):
    """
    Compute the total bytes used by a bucket.
    NOTE: This iterates over every key in the bucket.  If you have millions of
          keys this could take a while.
    """
    s3 = boto.connect_s3()

    total_bytes = 0
    bucket = s3.lookup(bucket_name)
    if bucket:
        for key in bucket:
            total_bytes += key.size
    else:
        print 'Warning: bucket %s was not found!' % bucket_name
    return total_bytes

