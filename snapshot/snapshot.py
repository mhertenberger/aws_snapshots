import boto3
import click

session = boto3.Session(profile_name="snapshot")
ec2 = session.resource("ec2")


def filter_instances(project):
    instances = []

    if project:
        filters = [{"Name":"tag:Project","Values":[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances


@click.group()
def cli():
    """Snapshot manages snapshots"""

@cli.group("snapshots")
def snapshots():
    """Commands for snapshots"""

@snapshots.command("list")
@click.option("--project", default=None,
    help="Only snapshots for project (tag Project:<name>)")

def list_snapshots(project):
    "List EC2 snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                s.id,
                v.id,
                s.state,
                s.progress,
                s.start_time.strftime("%c")
            )))
    return


@cli.group("volumes")
def volumes():
    """Commands for volumes"""

@volumes.command("list")
@click.option("--project", default=None,
    help="Only volumes for project (tag Project:<name>)")

def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
            v.id,
            i.id,
            v.state,
            str(v.size) + "GiB",
            v.encrypted and "Encrypted" or "Not encrypted"
            )))

    return


@cli.group("instances")
def instances():
    """Commands for instances"""

@instances.command("createsnapshot",
    help="Create snapshots of all volumes")
@click.option("--project", default=None,
    help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):

    instances = filter_instances(project)

    for i in instances:
        print("Stopping instance {0} in preparation for snapshot creation...".format(i.id))
        i.stop()
        i.wait_until_stopped()

        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by snapshot script")

        print("Restarting {0} after snapshot creation...".format(i.id))
        i.start()
        i.wait_until_running()

    print("Snapshots have been created.")
    return


@instances.command("list")
@click.option("--project", default=None,
    help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = {t["Key"]:t["Value"] for t in i.tags or []}
        print(", ".join((
            i.id,
            i.instance_type,
            i.placement["AvailabilityZone"],
            i.state["Name"],
            i.public_dns_name,
            tags.get("Project","<No project>"))))
    return


@instances.command("start")
@click.option("--project", default=None,
    help="Only instances for project (tag Project:<name>)")
def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()
    return


@instances.command("stop")
@click.option("--project", default=None,
    help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()
    return



if __name__ == "__main__":
    cli()
