
def launchAmi(ec2, image_id, security_group):
  try:
    print("")
    print("Launching AMI")
    ec2.create_launch_configuration(
      LaunchConfigurationName='amiDjango',
      ImageId=image_id,
      SecurityGroups=[
        security_group.group_id
      ],
      InstanceType='t2.micro',
      KeyName="H0-Vergara"
    )
    print("AMI Launched")
  except Exception as e:
    print("Error launching AMI")
    print(e)

  
def deleteLaunchAmi(ec2):
  try:
    print("Deleting Launch Configuration")

    ec2.delete_launch_configuration(LaunchConfigurationName="amiDjango")
    
    print("Launch AMI Deleted")
    
  except:
    print("No Launch AMI found")

def createAmiDjango(ec2, DJANGO_INSTANCE_ID, waiter):
  try:
    instance = ec2.create_image(
      Name="ImageDjango",
      InstanceId=DJANGO_INSTANCE_ID,
      NoReboot=False,
    )
    print("Creating Django AMI...")
    waiter.wait(ImageIds=[instance['ImageId']])
    print("Djando AMI Created")

    return instance, instance['ImageId']
  except Exception as e:
    print("Error: ")
    print(e)
    return False

def deleteAmi(ec2):
  try:
    print("Deleting Launch")
    ec2.delete_launch_configuration(LaunchConfigurationName="amidjango")
    print("Launch Deleted")
  except Exception as e:
    print("Error :")
    print(e)

