def createAutoScalling(ec2_auto_scalling, ec2_north_virginia, target_group_arns):
  try:
    print("")
    print("Launching auto scalling group...")
    list_all_zones = []
    all_zones = ec2_north_virginia.describe_availability_zones()
    for i in all_zones["AvailabilityZones"]:
      list_all_zones.append(i["ZoneName"])

    ec2_auto_scalling.create_auto_scaling_group(
      AutoScalingGroupName="auto_scaling_django",
      LaunchConfigurationName="ami_launched",
      MinSize=1,
      MaxSize=3,
      TargetGroupARNs=[target_group_arns],
      AvailabilityZones=list_all_zones
    )
    print("Auto scalling group created")

  except Exception as e:
    print("")
    print("Error creating Auto scalling group")
    print(e)

def deleteAutoScalling(ec2):
  try:
    print("")
    print("Deleting auto scalling group...")

    ec2.delete_auto_scaling_group(
      AutoScalingGroupName="auto_scaling_django",
      ForceDelete=True
    )
    print("Auto scalling group deleted")

  except:
    print("")
    print("Auto Scalling Group does not exist")
