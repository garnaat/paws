import boto

def copy_object(src_bucket_name,
                src_key_name,
                dst_bucket_name,
                dst_key_name,
                preserve_metadata=True):
    """
    Copy an existing object to another location.

    src_bucket_name   Bucket containing the existing object.
    src_key_name      Name of the existing object.
    dst_bucket_name   Bucket to which the object is being copied.
    dst_key_name      The name of the new object.
    preserve_metadata If True, all metadata on the original object
                      will be preserved on the new object.  If False
                      the new object will have the default metadata.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(src_bucket_name)

    # Lookup the existing object in S3
    key = bucket.lookup(src_key_name)

    # Copy the key back on to itself, with new metadata
    return key.copy(dst_bucket_name, dst_key_name, preserve_acl=preserve_acl)

                       

