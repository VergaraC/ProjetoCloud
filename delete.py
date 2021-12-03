from logs import logging

def deleteInstance(ec2, waiter,keyName):
  try:
    delete_instances_ids = []
    existing_instances = ec2.describe_instances(Filters=[
        {
            'Name': 'key-name',
            'Values': [
                keyName,
            ]
        },
        {
            'Name': 'instance-state-name',
            'Values': [
                "pending","running","stopping","stopped"
            ]
        },
    ],) 
    existing_instances = existing_instances["Reservations"]
    for instance in existing_instances:
      for i in instance["Instances"]:
        delete_instances_ids.append(i["InstanceId"])
    if len(delete_instances_ids) > 0:
      ec2.terminate_instances(InstanceIds=delete_instances_ids)

      print("Deleting instances...")
      waiter.wait(InstanceIds=delete_instances_ids)
      print("Instances deleted")
      logging.info("Instances deleted")
    else:

      print("No instances")
      logging.info("No instances")
      return
  except Exception as e:
    print("Error: ")
    print(e)
    logging.info("Error: ")
    logging.info(e)    

def deleteSG(ec2, security_group_names):
  try:
    existing_security_groups = ec2.describe_security_groups()
    for security_group in existing_security_groups["SecurityGroups"]:
      if security_group["GroupName"] in security_group_names:
  
        print("Deleting SG")
        ec2.delete_security_group(GroupId=security_group["GroupId"])
        print("SG deleted")
        logging.info("SG deleted")
  except Exception as e:
    print("Error :")
    print(e)
    logging.info("Error: ")
    logging.info(e)

def deleteImages(ec2, NameAMI):
  try:
    existingImages = ec2.describe_images(Owners=["self"])
    if len(existingImages["Images"]) > 0:
      for image in existingImages["Images"]:
        if image["Name"]== NameAMI:
    
          ec2.deregister_image(ImageId=image["ImageId"])
          print("AMI deleted")
          logging.info("AMI deleted")
    else:

      print("No AMI with that name")
      logging.info("No AMI with that name")
      return
  except Exception as e:
    print("Error")
    print(e)
    logging.info("Error: ")
    logging.info(e)