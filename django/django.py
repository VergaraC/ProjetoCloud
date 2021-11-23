import boto3
from botocore.config import Config

from utils import print_errors, print_successes, print_lines

def createDjango(region, machine_id ,postgresPublicIp, security_group, ec2):
  try:
    with open("django.sh", "r") as f:
      djangoSh = f.read()
      djangoSh2 = djangoSh.replace("s/node1/postgres_ip/g", f"s/node1/{postgresPublicIp}/g", 1)

    django_region = Config(region_name=region)
    django_resource = boto3.resource("ec2", config=django_region)

    instanceDjango = django_resource.create_instances(
      ImageId=machine_id,
      MinCount=1,
      MaxCount=1,
      InstanceType="t2.micro",
      KeyName="PostGres-Projeto1-Vergara",
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
    print_lines("")
    print_lines("Creating Django")
    instanceDjango[0].wait_until_running()
    instanceDjango[0].reload()
    print_successes("Djando Created")

    all_north_virginia_instances = ec2.describe_instances()
    instances = all_north_virginia_instances["Reservations"]
    for instance in instances:
      for i in instance["Instances"]:
        if i["State"]["Name"] == "running":
          for tag in i["Tags"]:
            if tag["Value"] == "django":
              idInstance = i["InstanceId"]
              print_successes(f"Id Instancia Django: {idInstance}")

    return instanceDjango, idInstance, instanceDjango[0].public_ip_address
  except Exception as e:
    print_lines("")
    print_errors("ERROR")
    print(e)
    return False