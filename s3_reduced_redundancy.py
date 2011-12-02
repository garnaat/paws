import boto
import os

def upload_file_rrs(local_file,
                    bucket_name,
                    key_name=None):
    """
    Upload a local file to S3 and store is using Reduced Redundancy Storage.

    local_file  Path to local file.
    bucket_name Bucket to which the file will be uploaded.
    key_name    Name of the new object in S3.  If not provided, the basename
                of the local file will be used.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)

    # Expand common shell vars in filename.
    local_file = os.path.expanduser(local_file)
    local_file = os.path.expandvars(local_file)

    # If key_name was not provided, use basename of file.
    if not key_name:
        key_name = os.path.basename(local_file)

    # Create a new local key object.
    key = bucket.new_key(key_name)

    # Now upload file to S3
    key.set_contents_from_filename(local_file, reduced_redundancy=True)

def copy_object_to_rrs(bucket_name,
                       key_name):
    """
    Will change an existing standard storage class object to a
    Reduced Redundancy storage class object.
    
    bucket_name Bucket in which the existing key is located.
    key_name    Name of the existing, standard storage key.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)
    key = bucket.lookup(key_name)
    
    return key.copy(bucket_name, key_name, reduced_redundancy=True,
                    preserve_acl=True)
    
