import boto3

from postgresOhio.postgresOhio import createPostgres
from django.django import createDjango
from securityGroups import createDjangoSG, createPostgresSG
from ami import createAmiDjango, deleteAmi, launchAmi
from delete import deleteImages, deleteInstance, deleteSG

NA_REGION = "us-east-1"
OHIO_REGION = "us-east-2"

# ubuntu 20 us-east-1 e us-east-2
UbuntuNA="ami-083654bd07b5da81d"
UbuntuOHIO="ami-0629230e074c580f2"
SGLists = ["djangoSG", "postgresSg"]

AMIS = ["django_AMI"]

#clients
ec2Ohio = boto3.client('ec2', region_name=OHIO_REGION)
ec2NorthVirginia = boto3.client('ec2', region_name=NA_REGION)

'''
# deleting all images
deleteImages(
  ec2NorthVirginia, 
  AMIS
) 
'''

# deleting all that already exists from previous run

WAITER_NA_INSTANCE = ec2NorthVirginia.get_waiter('instance_terminated')
WAITER_OHIO_INSTANCE = ec2Ohio.get_waiter('instance_terminated')

deleteInstance(
  ec2NorthVirginia, 
  WAITER_NA_INSTANCE
)
deleteInstance(
  ec2Ohio, 
  WAITER_OHIO_INSTANCE
)

# deleting all security-groups
deleteSG(
  ec2NorthVirginia, 
  SGLists
)
deleteSG(
  ec2Ohio, 
  SGLists
)
deleteSG(
  ec2NorthVirginia, 
  SGLists
)

# Creating postgres
postgresSG = createPostgresSG(OHIO_REGION)
postgres_instance, postgresPublicIP = createPostgres(
  OHIO_REGION, 
  UbuntuOHIO, 
  postgresSG
)
if postgresPublicIP:
  print(f"postgresPublicIP: {postgresPublicIP}")

# Creating Django
DjangoSG = createDjangoSG(NA_REGION)
django_instance, DJANGO_ID, djangoPublicIp = createDjango(
  NA_REGION, 
  UbuntuNA, 
  postgresPublicIP, 
  DjangoSG, 
  ec2NorthVirginia
)
if djangoPublicIp:
  print(f"djangoPublicIp: {djangoPublicIp}")
'''
# creating django AMI (IMAGE)
django_AMI, DJANGO_AMI_ID = createAmiDjango(
  ec2NorthVirginia, 
  DJANGO_ID, 
  WAITER_AMI
)
if DJANGO_AMI_ID:
  print(f"DJANGO_AMI_ID: {DJANGO_AMI_ID}")

# delete django instance after AMI creation
deleteInstance(
  ec2NorthVirginia, 
  WAITER_NA_INSTANCE
)
'''
