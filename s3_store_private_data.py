import boto

def store_private_data(bucket_name, key_name, path_to_file):
    """
    Write the contents of a local file to S3 and also store custom
    metadata with the object.

    bucket_name   The name of the S3 Bucket.
    key_name      The name of the object containing the data in S3.
    path_to_file  Fully qualified path to local file.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)

    # Get a new, blank Key object from the bucket.  This Key object only
    # exists locally until we actually store data in it.
    key = bucket.new_key(key_name)

    # First let's demonstrate how to write string data to the Key
    data = 'This is the content of my key'
    key.set_contents_from_string(data)

    # Now fetch the data from S3 and compare
    stored_key = bucket.lookup(key_name)
    stored_data = stored_key.get_contents_as_string()
    assert stored_data == data

    # Now, overwrite the data with the contents of the file
    key.set_contents_from_filename(path_to_file)

    return key

