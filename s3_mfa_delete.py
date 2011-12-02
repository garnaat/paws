import boto

def configure_mfa_delete(bucket_name,
                         mfa_serial_number,
                         mfa_token,
                         enable=True):
    """
    Enable versioning on a bucket.

    bucket_name        Bucket to be configured.
    mfa_serial_number  The serial number of the MFA device associated
                       with your account.
    mfa_token          The current token displayed on the MFA device.
    enable             A boolean value to indicate whether MFA Delete
                       is being enabled or disabled.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)

    # Get the current status of versioning on the bucket
    # and print the value out.
    config = bucket.get_versioning_status()
    print 'Current Versioning Status: ', config

    if 'Versioning' in config and config['Versioning'] == 'Enabled':
        versioning = True
    else:
        versioning = False
        
    # Make change to configuration.  This method takes a tuple
    # consisting of the mfa serial # and token.
    bucket.configure_versioning(versioning=versioning, mfa_delete=enable,
                                (mfa_serial_number, mfa_token))

    # Update the status of versioning and print the new value.
    config = bucket.get_versioning_status()
    print 'New Versioning Status: ', config

