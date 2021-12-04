from logs import logging
import time
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

    print("Creating LB")
    waiter.wait(LoadBalancerArns=[loadBalancerArn])
    print("LB Created")
    logging.info("LB created")


    return load_balancer, loadBalancerArn
  except Exception as e:
    print("Error: ")
    print(e)
    logging.info("Error?")
    logging.error(e)
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
          print("LB Deleted")
          logging.info("LB Deleted")
          time.sleep(60)
          return balancer["LoadBalancerArn"]
        else:
          print("LB Found and not deleted: ",balancer["LoadBalancerName"])
    else:
      print("There are no LBs")
      logging.info("There are no LBs")
      return
  except Exception as e:
    print("Error: ")
    print(e)
    logging.info("Error: ")
    logging.error(e)
    return False

def useLoadBalancer(ec2_auto_scalling, target_group_arn):
  try:
    
    print("Attaching LB")
    ec2_auto_scalling.attach_load_balancer_target_groups(
      AutoScalingGroupName='asDjango',
      TargetGroupARNs=[
        target_group_arn
      ]
    )
    print("LB Attached")
    logging.info("LB Attached")
    return
  except Exception as e:
    print("Error:")
    print(e)
    logging.info("Error:")
    logging.error(e)
    return False