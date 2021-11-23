import boto3

from postgresOhio.postgresOhio import createPostgres
from django.django import createDjango
from securityGroups import createDjangoSG, createPostgresSG
from ami import createAmiDjango, deleteAmi, launchAmi
from delete import deleteImages, deleteInstances, deleteSG

# AWS regions
NA_REGION = "us-east-1"
OHIO_REGION = "us-east-2"

# ubuntu 20 us-east-1 e us-east-2
AMI_ID_NA="ami-083654bd07b5da81d"
AMI_ID_OHIO="ami-0629230e074c580f2"

# name from all images name
AMIS = ["django_AMI"]

# getting ec2 client
ec2Ohio = boto3.client('ec2', region_name=OHIO_REGION)
ec2NorthVirginia = boto3.client('ec2', region_name=NA_REGION)

# deleting all images
deleteImages(
  ec2NorthVirginia, 
  AMIS
) 

# deleting all instances
WAITER_NA_INSTANCE = ec2NorthVirginia.get_waiter('instance_terminated')
WAITER_OHIO_INSTANCE = ec2Ohio.get_waiter('instance_terminated')

deleteInstances(
  ec2NorthVirginia, 
  WAITER_NA_INSTANCE
)
deleteInstances(
  ec2Ohio, 
  WAITER_OHIO_INSTANCE
)

# deleting all security-groups
deleteSG(
  ec2NorthVirginia, 
  SECURITY_GROUP_NAMES
)
deleteSG(
  ec2Ohio, 
  SECURITY_GROUP_NAMES
)
deleteSG(
  ec2NorthVirginia, 
  SECURITY_GROUP_NAMES
)

# Creating postgres
POSTGRES_SECURITY_GROUP = createPostgresSG(OHIO_REGION)
postgres_instance, postgresPublicIP = createPostgres(
  OHIO_REGION, 
  AMI_ID_OHIO, 
  POSTGRES_SECURITY_GROUP
)
if postgresPublicIP:
  print(f"postgresPublicIP: {postgresPublicIP}")

# Creating Django
DJANGO_SECURITY_GROUP = createDjangoSG(NA_REGION)
django_instance, DJANGO_ID, djangoPublicIp = createDjango(
  NA_REGION, 
  AMI_ID_NA, 
  postgresPublicIP, 
  DJANGO_SECURITY_GROUP, 
  ec2NorthVirginia
)
if djangoPublicIp:
  print(f"djangoPublicIp: {djangoPublicIp}")

# creating django AMI (IMAGE)
django_AMI, DJANGO_AMI_ID = createAmiDjango(
  ec2NorthVirginia, 
  DJANGO_ID, 
  WAITER_AMI
)
if DJANGO_AMI_ID:
  print(f"DJANGO_AMI_ID: {DJANGO_AMI_ID}")

# delete django instance after AMI creation
deleteInstances(
  ec2NorthVirginia, 
  WAITER_NA_INSTANCE
)

