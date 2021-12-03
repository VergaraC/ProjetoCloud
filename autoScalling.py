def createAutoScalling(ec2_auto_scalling, ec2_north_virginia, targetGroupArns):
  try:
    print("")
    print("Launching auto scalling group...")
    listRegions = []
    all_zones = ec2_north_virginia.describe_availability_zones()
    for i in all_zones["AvailabilityZones"]:
      listRegions.append(i["ZoneName"])

    ec2_auto_scalling.create_auto_scaling_group(
      AutoScalingGroupName="asDjango",
      LaunchConfigurationName="ami_launched",
      MinSize=1,
      MaxSize=3,
      TargetGroupARNs=[targetGroupArns],
      AvailabilityZones=listRegions
    )
    print("AS created")

  except Exception as e:
    print("Failed to creat AS ")
    print(e)

def deleteAutoScalling(ec2):
  try:
    print("Deleting AS ")

    ec2.delete_auto_scaling_group(
      AutoScalingGroupName="asDjango",
      ForceDelete=True
    )
    print("Auto scalling group deleted")

  except:
    print("Auto Scalling Group does not exist")

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
  except:
    print("Failed to create policy")
