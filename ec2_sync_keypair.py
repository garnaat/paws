import boto.ec2

def sync_keypairs(keypair_name, public_key_file):
    """
    Synchronize SSH keypairs across all EC2 regions.

    keypair_name    The name of the keypair.
    public_key_file The path to the file containing the
                    public key portion of the keypair.
    """
    fp = open(public_key_file)
    material = fp.read()
    fp.close()
    
    for region in boto.ec2.regions():
        ec2 = region.connect()
        # Try to list the keypair.  If it doesn't exist
        # in this region, then import it.
        try:
            key = ec2.get_all_key_pairs(keynames=[keypair_name])[0]
            print 'Keypair(%s) already exists in %s' % (keypair_name,
                                                        region.name)
        except ec2.ResponseError, e:
            if e.code == 'InvalidKeyPair.NotFound':
                print 'Importing keypair(%s) to %s' % (keypair_name,
                                                       region.name)
                ec2.import_key_pair(keypair_name, material)
        
