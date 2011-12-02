import boto

def modify_metadata(bucket_name,
                    key_name,
                    metadata):
    """
    Update the metadata with an existing object.

    bucket_name   The name of the S3 Bucket.
    key_name      The name of the object containing the data in S3.
    metadata      A Python dict object containing the new metadata.
                  For example: {'key1':'value1', 'key2':'value2'}
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)

    # Lookup the existing object in S3
    key = bucket.lookup(key_name)

    # Copy the key back on to itself, with new metadata
    key.copy(bucket.name, key.name, metadata, preserve_acl=True)

    return key

                       

