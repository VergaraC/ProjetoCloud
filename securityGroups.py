from logs import logging
import boto3
from botocore.config import Config

def createPostgresSG(region):
    try:
        postgres_region = Config(region_name=region)
        postgres_resource = boto3.resource("ec2", config=postgres_region)

        sgPostgres = postgres_resource.create_security_group(
            Description='allowing ports',
            GroupName='postgresSg'
        )
        logging.info("Postgres SG created")
        print("Postgres SG created")

        sgPostgres.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=22,
            ToPort=22,
            IpProtocol="tcp"
        )  
        sgPostgres.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=5432,
            ToPort=5432,
            IpProtocol="tcp"
        )

        sgPostgres.load()
        logging.info("Postgres SG running")
        print("Postgres SG running")
        

        return sgPostgres
    except Exception as e:
        print("Error:")
        print(e)
        logging.info("errror:")
        logging.info(e)

        return False

def createDjangoSG(region):
    try:
        django_region = Config(region_name=region)
        django_resource = boto3.resource("ec2", config=django_region)

        sGDjango = django_resource.create_security_group(
            Description='allowing ports',
            GroupName='djangoSG'
        )
        print("Django SG Created")
        logging.info("Django SG created")


        sGDjango.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=22,
            ToPort=22,
            IpProtocol="tcp"
        )
        sGDjango.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=8080,
            ToPort=8080,
            IpProtocol="tcp"
        )

        sGDjango.load()
        print("Django SG unning")

        return sGDjango
    except Exception as e:
        print("Error:")
        print(e)
        logging.info("Error:")
        logging.info(e)

        return False

def createLoadBalancerSG(region):
    try:
        lbRegion = Config(region_name=region)
        lB = boto3.resource("ec2", config=lbRegion)

        sG_LB = lB.create_security_group(
            Description='allowing ports',
            GroupName='lbSG',
        )
        print("Load Balancer SG created")
        
        sG_LB.authorize_ingress(
            CidrIp="0.0.0.0/0",
            FromPort=80,
            ToPort=80,
            IpProtocol="tcp"
        )

        sG_LB.load()
        print("LB Up")
        logging.info("SG LB Done")


        return sG_LB
    except Exception as e:  
        print("Error: ")
        print(e)
        logging.info("Error: ")
        logging.info(e)

        return False