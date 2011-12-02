import boto

def store_metadata_with_key(bucket_name,
                            key_name,
                            path_to_file,
                            metadata):
    """
    Write the contents of a local file to S3 and also store custom
    metadata with the object.

    bucket_name   The name of the S3 Bucket.
    key_name      The name of the object containing the data in S3.
    path_to_file  Fully qualified path to local file.
    metadata      A Python dict object containing key/value
                  data you would like associated with the object.
                  For example: {'key1':'value1', 'key2':'value2'}
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)

    # Get a new, blank Key object from the bucket.  This Key object only
    # exists locally until we actually store data in it.
    key = bucket.new_key(key_name)

    # Add the metadata to the Key object
    key.metadata.update(metadata)
    
    # Now, write the data and metadata to S3
    key.set_contents_from_filename(path_to_file)

    return key

def print_key_metadata(bucket_name, key_name):
    """
    Print the metadata associated with an S3 Key object.
    
    bucket_name   The name of the S3 Bucket.
    key_name      The name of the object containing the data in S3.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)
    key = bucket.lookup(key_name)
    print key.metadata
                       

