import boto
from boto.s3.connection import Location

def create_bucket(bucket_name, location=Location.DEFAULT):
    """
    Create a bucket.  If the bucket already exists and you have
    access to it, no error will be returned by AWS.
    Note that bucket names are global to a S3 region or location
    so you need to choose a unique name.

    bucket_name - The name of the bucket to be created.
    
    location - The location in which the bucket should be
               created.  The Location class is a simple
               enum-like static class that has the following attributes:

               DEFAULT|EU|USWest|APNortheast|APSoutheast
    """
    s3 = boto.connect_s3()

    # First let's see if we already have a bucket of this name.
    # The lookup method will return a Bucket object if the
    # bucket exists and we have access to it or None.
    bucket = s3.lookup(bucket_name)
    if bucket:
        print 'Bucket (%s) already exists' % bucket_name
    else:
        # Let's try to create the bucket.  This will fail if
        # the bucket has already been created by someone else.
        try:
            bucket = s3.create_bucket(bucket_name, location=location)
        except s3.provider.storage_create_error, e:
            print 'Bucket (%s) is owned by another user' % bucket_name
    return bucket

