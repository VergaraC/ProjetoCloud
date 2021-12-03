
def getSubnets(ec2):
  subnets = ec2.describe_subnets()
  subnetsId = []
  for i in subnets["Subnets"]:
    subnetsId.append(i["SubnetId"])
  return subnetsId

def createLoadBalancer(ec2_north_virginia, ec2LoadBalancer, security_group, waiter):
  try:
    subnets = getSubnets(ec2_north_virginia)
    load_balancer = ec2LoadBalancer.create_load_balancer(
      SecurityGroups=[
        security_group.group_id
      ],
      IpAddressType='ipv4',
      Name='lbDjango',
      Subnets=subnets
    )
    loadBalancerArn = load_balancer['LoadBalancers'][0]['LoadBalancerArn']

    print("Creating Load Balancer")
    waiter.wait(LoadBalancerArns=[loadBalancerArn])
    print("Load Balancer Created")

    return load_balancer, loadBalancerArn
  except Exception as e:
    print("")
    print("Error: ")
    print(e)
    return False

def deleteLoadBalancer(ec2LoadBalancer, waiter):
  try:
    loadBalancer = ec2LoadBalancer.describe_load_balancers()
    if len(loadBalancer['LoadBalancers']) > 0:
      for balancer in loadBalancer['LoadBalancers']:
        if balancer["LoadBalancerName"] == "lbDjango":
          ec2LoadBalancer.delete_load_balancer(LoadBalancerArn=balancer["LoadBalancerArn"])
          print("Deleting Load Balancer")
          
          waiter.wait(LoadBalancerArns=[balancer["LoadBalancerArn"]])
          print("Load Balancer Deleted")
          return balancer["LoadBalancerArn"]
    else:
      print("There are no Load Balancers")
      return
  except Exception as e:
    print("Error: ")
    print(e)
    return False

def useLoadBalancer(ec2_auto_scalling, target_group_arn):
  try:
    
    print("Attaching load balancer")
    ec2_auto_scalling.attach_load_balancer_target_groups(
      AutoScalingGroupName='asDjango',
      TargetGroupARNs=[
        target_group_arn
      ]
    )
    print("Load Balancer Attached")
    return
  except Exception as e:
    print("Error:")
    print(e)
    return False