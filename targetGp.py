

def createTargetDp(ec2_north_virginia, ec2_load_balancer):
  try:
    target_groups = ec2_north_virginia.describe_vpcs()
    vpc_id = target_groups["Vpcs"][0]["VpcId"]

    print("")
    print("Creating Target Group")

    target_group_created = ec2_load_balancer.create_target_group(
      Name="Django-Manager",
      Protocol="HTTP",
      Port=8080,
      HealthCheckProtocol='HTTP',
      HealthCheckPort='8080',
      HealthCheckPath='/admin/',
      Matcher={
        'HttpCode': '200,302,301,404,403',
      },
      TargetType="instance",
      VpcId=vpc_id
    )

    new_target_group = target_group_created["TargetGroups"][0]["TargetGroupArn"]

    print("")
    print("Target Group created")
    
    return new_target_group

  except Exception as e:
    print("")
    print("ERROR:")
    print(e)
    return False

def deleteTargetGp(ec2_load_balancer):
  try:
    target_groups = ec2_load_balancer.describe_target_groups()
    if len(target_groups["TargetGroups"]) > 0:
      for target_group in target_groups["TargetGroups"]:
        if target_group["TargetGroupName"] == "Django-Manager":
            ec2_load_balancer.delete_target_group(TargetGroupArn=target_group["TargetGroupArn"])
            print("")
            print("Target Group deleted")
        else:
            print("No Django-Manager Targer GP")

    else:
      print("")
      print("No Target Groups Available")
      return

  except Exception as e:
    print("")
    print("Error:")
    print(e)
    return False