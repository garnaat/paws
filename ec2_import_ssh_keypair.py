import boto

ec2 = boto.connect_ec2()

# Read the public key material from the file
fp = open('mykey.pub')
material = fp.read()
fp.close()
key_pair = ec2.import_key_pair('mykey', material)

