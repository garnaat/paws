import boto
import boto.ec2

def print_running_instances(running_instances):
    print 'The following running instances were found'
    for account_name in running_instances:
        print '\tAccount: %s' % account_name
        d = running_instances[account_name]
        for region_name in d:
            print '\t\tRegion: %s' % region_name
            for instance in d[region_name]:
                print '\t\t\tAn %s instance: %s' % (instance.instance_type,
                                                    instance.id)
                print '\t\t\t\tTags=%s' % instance.tags
    
def find_all_running_instances(accounts=None, quiet=False):
    """
    Will find all running instances across all EC2 regions for all of the
    accounts supplied.

    :type accounts: dict
    :param accounts: A dictionary contain account information.  The key is
                     a string identifying the account (e.g. "dev") and the
                     value is a tuple or list containing the access key
                     and secret key, in that order.
                     If this value is None, the credentials in the boto
                     config will be used.
    """
    if not accounts:
        creds = (boto.config.get('Credentials', 'aws_access_key_id'),
                 boto.config.get('Credentials', 'aws_secret_access_key'))
        accounts = {'main' : creds}
    running_instances = {}
    for account_name in accounts:
        running_instances[account_name] = {}
        ak, sk = accounts[account_name]
        for region in boto.ec2.regions():
            conn = region.connect(aws_access_key_id=ak,
                                  aws_secret_access_key=sk)
            filters={'instance-state-name' : 'running'}
            instances = []
            reservations = conn.get_all_instances(filters=filters)
            for r in reservations:
                instances += r.instances
            if instances:
                running_instances[account_name][region.name] = instances
    if not quiet:
        print_running_instances(running_instances)
    return running_instances
    
if __name__ == '__main__':
    find_all_running_instances()
