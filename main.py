import boto3
import os
import time

from postgresOhio.postgresOhio import createPostgres
from django.django import createDjango
from securityGroups import createDjangoSG, createPostgresSG
from ami import createAmiDjango, deleteAmi, launchAmi
from delete import deleteImages, deleteInstance, deleteSG
from targetGp import createTargetDp, deleteTargetGp
from autoScalling import createAutoScalling, deleteAutoScalling


NA_REGION = "us-east-1"
OHIO_REGION = "us-east-2"

# ubuntu 20 us-east-1 e us-east-2
UbuntuNA="ami-083654bd07b5da81d"
UbuntuOHIO="ami-0629230e074c580f2"
SGLists = ["djangoSG", "postgresSg"]


#clients
ec2Ohio = boto3.client('ec2', region_name=OHIO_REGION)
ec2NorthVirginia = boto3.client('ec2', region_name=NA_REGION)
ec2LoadBalencer_NA = boto3.client('elbv2', region_name=NA_REGION)
ec2AutoScallingNA = boto3.client('autoscaling', region_name=NA_REGION)

waiterAMI = ec2NorthVirginia.get_waiter('image_available')
'''
waiterCreateLoadBalancer = ec2LoadBalencer_NA.get_waiter('load_balancer_available')
waiterDeleteLoadBalencer = ec2LoadBalencer_NA.get_waiter('load_balancers_deleted')
deleteTargetGp(ec2LoadBalencer_NA)
deleteAutoScalling(ec2AutoScallingNA)
'''

# deletando antigos
print("Deleting Images")

deleteImages(
  ec2NorthVirginia, 
  "ImageDjango"
) 

waiterNA = ec2NorthVirginia.get_waiter('instance_terminated')
waiterOhio = ec2Ohio.get_waiter('instance_terminated')

deleteInstance(
  ec2NorthVirginia, 
  waiterNA,
  "H0-Vergara"

)
deleteInstance(
  ec2Ohio, 
  waiterOhio,
  "PostGres-Projeto1-Vergara"
)
print("Instances Deleted")
# deleting all security-group

deleteSG(
  ec2NorthVirginia, 
  SGLists
)
deleteSG(
  ec2Ohio, 
  SGLists
)
print("SGs Deleted")


# Creating postgres
postgresSG = createPostgresSG(OHIO_REGION)
print("oi ",postgresSG)
postgres_instance, postgresPublicIP = createPostgres(OHIO_REGION, UbuntuOHIO, postgresSG)

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
  print("djangoPublicIp: ", djangoPublicIp)
  print(DJANGO_ID)

print("Criando AMI doD jango")
django_AMI, DJANGO_AMI_ID = createAmiDjango(
  ec2NorthVirginia, 
  DJANGO_ID, 
  waiterAMI
)
if DJANGO_AMI_ID:
  print(f"DJANGO_AMI_ID: {DJANGO_AMI_ID}")

# delete django instance
deleteInstance(
  ec2NorthVirginia, 
  waiterNA,
  "H0-Vergara"
)

