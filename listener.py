from logs import logging

def createListener(ec2, target_group_arn, load_balancer_arn):
  try:
    print("Creating Listener")
    ec2.create_listener(
      LoadBalancerArn=load_balancer_arn,
      Protocol='HTTP',
      Port=80,
      DefaultActions=[
        {
          'Type': 'forward',
          'TargetGroupArn': target_group_arn
        }
      ]
    )
    print("Listener Created")
    logging.info("Listener Created")
  except Exception as e:
    print("Error: ")
    logging.info("Error?")
    logging.info(e)
    print(e)