import boto

ec2 = boto.connect_ec2()

# Let's assume the instance we are interested in has already been started
# in the previous examples and is tagged with "paws".  This little
# incantation will retrieve it for us.

instance = ec2.get_all_instances(filters={'paws' : None})[0].instances[0]

# Allocate an Elastic IP Address.  This will be associated with your
# account until you explicitly release it.

address = ec2.allocate_address()

# Associate our new Elastic IP Address with our instance.

ec2.associate_address(instance.id, address.public_ip)

# Alternatively, you could do this.

instance.use_ip(address)
