from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import gzip
import cStringIO
import os

script = """#!/bin/sh
echo "Installing boto..."
cd /root
git clone git://github.com/boto/boto.git
cd boto
python setup.py install
echo "...done"
"""

cloud_config = """
packages:
 - python-setuptools

runcmd:
 - [ easy_install, boto ]                            
"""

def create_txt_part(path, subtype, filename=None):
    fp = open(path)
    s = fp.read()
    fp.close()
    txt = MIMEText(s, _subtype=subtype)
    if filename:
        txt.add_header('Content-Disposition',
                       'attachment', filename=filename)
    return txt

def build_userdata(metric_dir):
    mp = MIMEMultipart()
    # Add our part handler
    path = os.path.join(metric_dir, 'metric_part_handler.py')
    txt = create_txt_part(path, 'part-handler', 'metric_part_handler.py')
    mp.attach(txt)
    # Add the boto config file
    path = os.path.join(metric_dir, 'boto.cfg')
    txt = create_txt_part(path, 'x-config', 'boto.cfg')
    mp.attach(txt)
    # Add the cloud-config
    txt = MIMEText(cloud_config, _subtype='cloud-config')
    mp.attach(txt)
    # Add disk metric
    path = os.path.join(metric_dir, 'metric_disk_usage')
    txt = create_txt_part(path, 'x-metric', 'metric_disk_usage')
    mp.attach(txt)
    
    gfileobj = cStringIO.StringIO()
    gfile = gzip.GzipFile(fileobj=gfileobj, mode='wb')
    gfile.write(mp.as_string())
    gfile.close()

    return gfileobj.getvalue()
