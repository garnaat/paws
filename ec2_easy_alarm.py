import os
import boto

def easy_alarm(instance_id,
               alarm_name,
               email_addresses,
               metric_name,
               comparison,
               threshold,
               period,
               eval_periods,
               statistics):
    """
    Create a CloudWatch alarm for a given instance.  You can choose
    the metric and dimension you want to associate with the alarm
    and you can provide a list of email addresses that will be
    notified when the alarm fires.

    instance_id     The unique identifier of the instance you wish to
                    monitoring.

    alarm_name      A short but meaningful name for your alarm.

    email_addresses A list of email addresses that you want to
                    have notified when the alarm fires.

    metric_name     The name of the Metric you want to be notified
                    about.  Valid values are:
                    DiskReadBytes|DiskWriteBytes|
                    DiskReadOps|DiskWriteOps|
                    NetworkIn|NetworkOut|
                    CPUUtilization

    comparison      The comparison operator.  Valid values are:
                    >= | > | < | <=

    threshold       The threshold value that the metric will
                    be compared against.

    period          The granularity of the returned data.
                    Minimum value is 60 (seconds) and valid values
                    must be multiples of 60.

    eval_periods    The number of periods over which the alarm
                    must be measured before triggering notification.

    statistics      The statistic to apply.  Valid values are:
                    SampleCount | Average | Sum | Minimum | Maximum

    """
    # Create a connection to the required services
    ec2 = boto.connect_ec2()
    sns = boto.connect_sns()
    cw = boto.connect_cloudwatch()

    # Make sure the instance in question exists and
    # is being monitored with CloudWatch.
    rs = ec2.get_all_instances(filters={'instance-id', instance_id})
    if len(rs) != 1:
        raise ValueError('Unable to find instance: %s' % instance_id)

    instance = rs[0].instances[0]
    instance.monitor()
    
    # Create the SNS Topic
    topic_name = 'CWAlarm-%s' % alarm_name
    print 'Creating SNS topic: %s' % topic_name
    response = sns.create_topic(topic_name)
    topic_arn = response['CreateTopicResponse']['CreateTopicResult']['TopicArn']
    print 'Topic ARN: %s' % topic_arn

    # Subscribe the email addresses to SNS Topic
    for addr in email_addresses:
        print 'Subscribing %s to Topic %s' % (addr, topic_arn)
        sns.subscribe(topic_arn, 'email', addr)

    # Now find the Metric we want to be notified about
    metric = cw.list_metrics(dimensions={'InstanceId':instance_id},
                             metric_name=metric_name)[0]
    print 'Found: %s' % metric

    # Now create Alarm for the metric
    print 'Creating alarm'
    alarm = metric.create_alarm(name=alarm_name, comparison=comparison,
                                threshold=threshold, period=period,
                                evaluationn_periods=eval_periods,
                                statistics=statistics,
                                alarm_actions=[topic_arn],
                                ok_actions=[topic_arn])
