import boto
import os
import time

def upload_website(bucket_name,
                   website_dir,
                   index_file,
                   error_file=None):
    """
    Upload a static website contained in a local directory to
    a bucket in S3.

    bucket_name The name of the bucket to upload website to.
    website_dir Fully-qualified path to directory containing
                website.
    index_file  The name of the index file (e.g. index.html)
    error_file  The name of the error file.  If not provided
                the default S3 error page will be used.
    """
    s3 = boto.connect_s3()
    bucket = s3.lookup(bucket_name)

    # Make sure bucket is publicly readable
    bucket.set_canned_acl('public-read')

    for root, dirs, files in os.walk(website_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, website_dir)
            print 'Uploading %s as %s' % (full_path, rel_path)
            key = bucket.new_key(rel_path)
            key.content_type = 'text/html'
            key.set_contents_from_filename(full_path, policy='public-read')

    # Now configure the website
    bucket.configure_website(index_file, error_file)

    # A short delay, just to let things become consistent.
    time.sleep(5)

    print 'You can access your website at:'
    print bucket.get_website_endpoint()
