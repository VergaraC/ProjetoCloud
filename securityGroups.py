from logging import ERROR
import boto3
from botocore.config import Config
from utils import print_errors, print_successes

def createPostgresSG(region):
    try:
        postgres_region = Config(region_name=region)
        postgres_resource = boto3.resource("ec2", config=postgres_region)

        sgPostgres = postgres_resource.create_security_group(
            Description='allowing ports',
            GroupName='postgres-sg',
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'postgres'
                        },
                    ]
                },
            ],
        )
        print("")    
        print_successes("Postgres SG created")

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
        print_successes("Postgres SG running")

        return sgPostgres
    except Exception as e:
        print("")
        print_errors("ERROR")
        print_errors("MAYBE THIS SECURITY-GROUP IS ALREADY CREATED")
        print(e)
        return False

def createDjangoSG(region):
    try:
        django_region = Config(region_name=region)
        django_resource = boto3.resource("ec2", config=django_region)

        sGDjango = django_resource.create_security_group(
            Description='allowing ports',
            GroupName='django_security_group',
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'django'
                        },
                    ]
                },
            ],
        )
        print("")
        print_successes("Django SG Created")

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
        print_successes("Django SG unning")

        return sGDjango
    except Exception as e:
        print("")
        print_errors("ERROR")
        print_errors("MAYBE THIS SECURITY-GROUP IS ALREADY CREATED")
        print(e)
        return False