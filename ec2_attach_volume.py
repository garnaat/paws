import boto
import time

def create_and_attach_volume(instance, volume_size, device_name):
    """
    Create a new EBS volume and attach it to the instance.

    instance    The instance object representing the instance to which
                the volume will be attached.

    volume_size The size (in GB) of the new volume.

    device_name The device name to which the new volume will be
                referred to on the instance.
    """
    ec2 = instance.connection
    # Determine the Availability Zone of the instance
    azone = instance.placement
    
    volume = ec2.create_volume(volume_size, azone)

    # Wait for the volume to be created.
    while volume.status != 'available':
        time.sleep(5)
        volume.update()

    volume.attach(instance.id, device_name)
    return volume
    
