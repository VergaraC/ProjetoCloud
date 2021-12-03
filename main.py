import boto3
from logs import logging

from postgresOhio.postgresOhio import createPostgres
from djangoF.django import createDjango
from securityGroups import createDjangoSG, createPostgresSG, createLoadBalancerSG
from ami import createAmiDjango, deleteAmi, launchAmi, deleteLaunchAmi
from delete import deleteImages, deleteInstance, deleteSG
from targetGp import createTargetDp, deleteTargetGp
from autoScalling import createAutoScalling, deleteAutoScalling, createAutoScallingPolicy
from loadBalencer import createLoadBalancer, deleteLoadBalancer, useLoadBalancer
from listener import createListener
NA_REGION = "us-east-1"
OHIO_REGION = "us-east-2"

# ubuntu 20 us-east-1 e us-east-2
UbuntuNA="ami-083654bd07b5da81d"
UbuntuOHIO="ami-0629230e074c580f2"
SGLists = ["djangoSG", "postgresSg","lbSG"]


#clients
ec2Ohio = boto3.client('ec2', region_name=OHIO_REGION)
ec2NorthVirginia = boto3.client('ec2', region_name=NA_REGION)
ec2LoadBalencer_NA = boto3.client('elbv2', region_name=NA_REGION)
ec2AutoScallingNA = boto3.client('autoscaling', region_name=NA_REGION)

waiterAMI = ec2NorthVirginia.get_waiter('image_available')
waiterCreateLB = ec2LoadBalencer_NA.get_waiter('load_balancer_available')
waiterDeleteLB = ec2LoadBalencer_NA.get_waiter('load_balancers_deleted')
waiterNA = ec2NorthVirginia.get_waiter('instance_terminated')
waiterOhio = ec2Ohio.get_waiter('instance_terminated')

# deletando antigos
print("Deletiing LBs")

deleteLoadBalancer(ec2LoadBalencer_NA, waiterDeleteLB)
deleteAutoScalling(ec2AutoScallingNA)
deleteLaunchAmi(ec2AutoScallingNA)


print("Deleting Images")

deleteImages(
  ec2NorthVirginia, 
  "ImageDjango"
) 
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

deleteTargetGp(ec2LoadBalencer_NA)
deleteSG(
  ec2NorthVirginia, 
  SGLists
)
deleteSG(
  ec2Ohio, 
  SGLists
)
print("SGs Deleted")
logging.info("All Deleted")


# Creating postgres
postgresSG = createPostgresSG(OHIO_REGION)
print("oi ",postgresSG)
postgres_instance, postgresPublicIP = createPostgres(OHIO_REGION, UbuntuOHIO, postgresSG)

if postgresPublicIP:
  print("postgresPublicIP: ",postgresPublicIP)
  logging.info("postgresPublicIP: ",postgresPublicIP)

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
  print("Django Public Ip: ", djangoPublicIp)
  logging.info("Django Public Ip: ", djangoPublicIp)

  print(DJANGO_ID)

print("Criando AMI doD jango")
django_AMI, DJANGO_AMI_ID = createAmiDjango(
  ec2NorthVirginia, 
  DJANGO_ID, 
  waiterAMI
)
if DJANGO_AMI_ID:
  print("Image Django ID: ",DJANGO_AMI_ID)
  logging.info("Image Django ID: ",DJANGO_AMI_ID)


# delete django instance
deleteInstance(
  ec2NorthVirginia, 
  waiterNA,
  "H0-Vergara"
)

TARGET_GROUP_ARN = createTargetDp(
  ec2NorthVirginia, 
  ec2LoadBalencer_NA
) 
lbSG = createLoadBalancerSG(NA_REGION)
load_balancer, LOAD_BALANCER_ARN = createLoadBalancer(
  ec2NorthVirginia, 
  ec2LoadBalencer_NA, 
  lbSG, 
  waiterCreateLB
)

launchAmi(
  ec2AutoScallingNA, 
  DJANGO_AMI_ID, 
  DjangoSG
)

createAutoScalling(
  ec2AutoScallingNA, 
  ec2NorthVirginia, 
  TARGET_GROUP_ARN
)

useLoadBalancer(ec2AutoScallingNA, TARGET_GROUP_ARN)

createListener(
  ec2LoadBalencer_NA, 
  TARGET_GROUP_ARN, 
  LOAD_BALANCER_ARN
)

createAutoScallingPolicy(ec2AutoScallingNA, TARGET_GROUP_ARN, LOAD_BALANCER_ARN)