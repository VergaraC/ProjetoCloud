import boto3
import time
from botocore.config import Config
from logs import logging

def createDjango(region, machine_id ,postgresPublicIp, security_group, ec2):
  try:
    with open("djangoF/django.sh", "r") as f:
      djangoSh = f.read()
      djangoSh2 = djangoSh.replace("s/node1/postgres_ip/g", f"s/node1/{postgresPublicIp}/g", 1)
    print("SH editado")
    logging.info(".sh edited")
    django_region = Config(region_name=region)
    django_resource = boto3.resource("ec2", config=django_region)

    instanceDjango = django_resource.create_instances(
      ImageId=machine_id,
      MinCount=1,
      MaxCount=1,
      InstanceType="t2.micro",
      KeyName="H0-Vergara",
      SecurityGroupIds=[
        security_group.group_id
      ],
      TagSpecifications=[
        {
          "ResourceType": "instance",
          "Tags": [
            {
              "Key": "Name",
              "Value": "django"
            }
          ]
        }
      ],
      UserData=djangoSh2
    )    
    print("Creating Django")
    instanceDjango[0].wait_until_running()
    instanceDjango[0].reload()

    print("Waiting for install.sh")
    time.sleep(120)
    print("Djando Done")
    logging.info("Django Sone")

    all_north_virginia_instances = ec2.describe_instances()
    instances = all_north_virginia_instances["Reservations"]
    for instance in instances:
      for i in instance["Instances"]:
        if i["State"]["Name"] == "running":
          if i["KeyName"] == "H0-Vergara":
            idInstance = i["InstanceId"]
            print(f"Id Instancia Django: {idInstance}")

    return instanceDjango, idInstance, instanceDjango[0].public_ip_address
  except Exception as e:
    print("Error: ")
    print(e)
    logging.info("error:")
    logging.info(e)
    return False