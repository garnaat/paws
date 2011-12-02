import boto

ec2 = boto.connect_ec2()

# Let's assume the instance we are interested in has already been started
# in the previous examples and is tagged with "paws".  This little
# incantation will retrieve it for us.

instance = ec2.get_all_instances(filters={'paws' : None})[0].instances[0]
co = instance.get_console_output()
print co.output
