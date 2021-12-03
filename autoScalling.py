from logs import logging

def createAutoScalling(ec2_auto_scalling, ec2_north_virginia, targetGroupArns):
  try:
    print("Creating AS")
    listRegions = []
    regions = ec2_north_virginia.describe_availability_zones()
    for i in regions["AvailabilityZones"]:
      listRegions.append(i["ZoneName"])

    ec2_auto_scalling.create_auto_scaling_group(
      AutoScalingGroupName="asDjango",
      LaunchConfigurationName="amiDjango",
      MinSize=1,
      MaxSize=3,
      TargetGroupARNs=[targetGroupArns],
      AvailabilityZones=listRegions
    )
    print("AS created")
    logging.info("AS created")

  except Exception as e:
    print("Error: ")
    print(e)
    logging.info("Error: ")
    logging.info(e)

def deleteAutoScalling(ec2):
  try:
    print("Deleting AS ")

    ec2.delete_auto_scaling_group(
      AutoScalingGroupName="asDjango",
      ForceDelete=True
    )
    print("AS deleted")
    logging.info("AS deleted")

  except:
    print("AS does not exist")
    logging.info("AS does not exist")

def createAutoScallingPolicy(ec2, targetGroupArn, loadBalancerArn):
  try: 
    print("Creating Policy")
    loadBalancerName = loadBalancerArn[loadBalancerArn.find("app"):]
    targetGroupName = targetGroupArn[targetGroupArn.find("targetgroup"):]
    
    ec2.put_scaling_policy(
      AutoScalingGroupName="asDjango",
      PolicyName="TargetTrackingScaling",
      PolicyType="TargetTrackingScaling",
      TargetTrackingConfiguration={
        "PredefinedMetricSpecification": {
          "PredefinedMetricType": "ALBRequestCountPerTarget",
          "ResourceLabel": f"{loadBalancerName}/{targetGroupName}"
        },
        "TargetValue": 50
      }
    )
    print("Policy created")
    logging.info("Policy created")
  except:
    print("Failed to create policy")
    logging.info("Failed to create policy")
