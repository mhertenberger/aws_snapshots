# aws_snapshots
Demo to manage AWS EC2 snapshots using Python.


## About

This project is a demo and uses boto3 to manage AWS EC2 instance snapshots.


## Configuring

snapshot uses the configuration file created by the AWS CLI

`aws configure --profile snapshot`


## Running

`pipenv run "python snapshot/snapshot.py" <command> <subcommand> <--project=PROJECT>`

*command* is instances, volumes or aws_snapshots
*subcommand* depends on command
*project* is optional (project should be a tag for the instance)
