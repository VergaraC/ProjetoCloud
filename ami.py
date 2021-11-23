from utils import print_errors, print_successes, print_lines

def launchAmi(ec2, image_id, security_group):
  try:
    print_lines("")
    print_lines("Launching AMI...")
    ec2.create_launch_configuration(
      LaunchConfigurationName='amidjango',
      ImageId=image_id,
      SecurityGroups=[
        security_group.group_id
      ],
      InstanceType='t2.micro'
    )
    print_successes("AMI Launched")
  except Exception as e:
    print_lines("")
    print_errors("Error launching AMI")
    print(e)

def createAmiDjango(ec2, DJANGO_INSTANCE_ID, waiter):
  try:
    instance = ec2.create_image(
      Name="django_AMI",
      InstanceId=DJANGO_INSTANCE_ID,
      NoReboot=False,
      TagSpecifications=[
        {
          "ResourceType": "image",
          "Tags": [
            {
              "Key": "Name",
              "Value": "django_image"
            }
          ]
        }
      ]
    )
    print_lines("")
    print_lines("Creating Django AMI...")
    waiter.wait(ImageIds=[ami_instance['ImageId']])
    print_successes("Djando AMI Created")

    return instance, instance['ImageId']
  except Exception as e:
    print_lines("")
    print_errors("Error")
    print(e)
    return False

def deleteAmi(ec2):
  try:
    print_lines("")
    print_lines("Deleting Launch")
    ec2.delete_launch_configuration(LaunchConfigurationName="amidjango")
    print_successes("Launch Deleted")
  except Exception as e:
    print_lines("")
    print_errors("Error deleting Launch")
    print(e)