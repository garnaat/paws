import boto

ec2 = boto.connect_ec2()

# Get a list of all current instances.  We will assume that the only
# instance running is the one we started in the previous recipe.

reservations = ec2.get_all_instances()

# Despite the name, get_all_instances does not return Instance
# objects directly.  What it returns are Reservation objects
# as returned by run_instances.  This is a confusing aspect of
# the EC2 API that we have decided to be consistent with in boto.
# The following incantation will return the actual Instance
# object embedded within the Reservation.  We are assuming we
# have a single Reservation which launched a single Instance.

instance = reservations[0].instances[0]

# We could call create_tags directly here but boto provides
# some nice convenience methods to make it even easier.
# We are going to store a single tag on this instance.

instance.add_tag('paws')

# We can now ask for all instances that have the tag name "paws"
# and get our instance back again.

reservations = ec2.get_all_instances(filters={'paws' : None})
new_instance = reservations[0].instances[0]
assert new_instance.id == instance.id

