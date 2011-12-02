import boto
from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType
import os
import base64

def clone_instance(instance):
    """
    Make an clone of an existing Instance object.

    instance      The Instance object to clone.
    """
    new_bdm = None
    ec2 = instance.connection

    if instance.block_device_mapping:
        root_device_name = instance.get_attribute('rootDeviceName')['rootDeviceName']
        user_data = instance.get_attribute('userData')['userData']
        # user_data comes back base64 encoded.  Need to decode it so it
        # can get re-encoded by run_instance !
        user_data = base64.b64decode(user_data)
        new_bdm = BlockDeviceMapping()
        for dev in instance.block_device_mapping:
            # if this entry is about the root device, skip it
            if dev != root_device_name:
                bdt = instance.block_device_mapping[dev]
                if bdt.volume_id:
                    volume = ec2.get_all_volumes([bdt.volume_id])[0]
                    snaps = volume.snapshots()
                    if len(snaps) == 0:
                        print 'No snapshots available for %s' % volume.id
                    else:
                        # sort the list of snapshots, newest is at the end now
                        snaps.sort(key=lambda snap: snap.start_time)
                        latest_snap = snaps[-1]
                        new_bdt = BlockDeviceType()
                        new_bdt.snapshot_id = latest_snap.id
                        new_bdm[dev] = new_bdt
                    
    return ec2.run_instances(instance.image_id,
                             key_name=instance.key_name,
                             security_groups=[g.name for g in instance.groups],
                             user_data=user_data,
                             instance_type=instance.instance_type,
                             kernel_id=instance.kernel,
                             ramdisk_id=instance.ramdisk,
                             monitoring_enabled=instance.monitored,
                             placement=instance.placement,
                             block_device_map=new_bdm).instances[0]
