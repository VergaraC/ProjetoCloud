from logging import ERROR
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
        print("")    
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
        print("Postgres SG running")

        return sgPostgres
    except Exception as e:
        print("")
        print("ERROR")
        print(e)
        return False

def createDjangoSG(region):
    try:
        django_region = Config(region_name=region)
        django_resource = boto3.resource("ec2", config=django_region)

        sGDjango = django_resource.create_security_group(
            Description='allowing ports',
            GroupName='djangoSG'
        )
        print("")
        print("Django SG Created")

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
        print("")
        print("ERROR")
        print(e)
        return False