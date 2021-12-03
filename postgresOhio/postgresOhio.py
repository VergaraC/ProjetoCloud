import boto3
from botocore.config import Config
from logs import logging

def createPostgres(region, machine_id, security_group):
  try:

    with open("postgresOhio/postgresOhio.sh", "r") as f:
      postgres_sh = f.read()

    database_region = Config(region_name=region)
    database_resource = boto3.resource("ec2", config=database_region)

    database_instance = database_resource.create_instances(
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
              "Value": "postgres"
            }
          ]
        }
      ],
      UserData=postgres_sh
    )
    print("Creating PostGres")
    database_instance[0].wait_until_running()
    database_instance[0].reload()
    print("PostGres Created")
    logging.info("PostGres Done")

    return database_instance, database_instance[0].public_ip_address
  except Exception as e:
    print("Error: ")
    print(e)
    logging.info("Error: ")
    logging.info(e)
    return False