#part-handler

import os

def list_types():
    """
    Return a list of mime-types that are handled by this module.
    """
    return(['text/x-config', 'text/x-metric'])

def handle_part(data, ctype, filename, payload):
    """
    data:     the cloudinit object
    ctype:    '__begin__', '__end__', or the specific mime-type of the part
    filename: the filename for the part, or dynamically generated part if
              no filename is given attribute is present
    payload:  the content of the part (empty for begin or end)
    """
    if ctype == 'text/x-config':
        path = os.path.join('/etc', filename)
        fp = open(path, 'w')
        fp.write(payload)
        fp.close()
        print '==== wrote %s payload to %s ====' % (ctype, path)
    elif ctype == 'text/x-metric':
        # Save metric command as an executable
        path = os.path.join('/usr/local/sbin', filename)
        fp = open(path, 'w')
        fp.write(payload)
        fp.close()
        os.chmod(path, 0755)
        # Add an entry to tell cron to run this every minute
        path = os.path.join('/etc/cron.d', filename)
        fp = open(path, 'w')
        fp.write('root /usr/local/sbin/%s' % filename)
        fp.close()
