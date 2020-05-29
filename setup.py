from setuptools import setup

setup(
    name = "snapshot",
    version = "0.1",
    author = "Manfred Hertenberger",
    author_email = "mhertenberger@gmail.com",
    description = "A tool to manage AWS EC2 snapshots.",
    license = "GPLv3+",
    packages = ["snapshot"],
    url = "https://github.com/mhertenberger/aws_snapshots",
    install_requires = [
        "click",
        "boto3"
    ],
    entry_points = """
        [console_scripts]
        snapshot = snapshot.snapshot:cli
    """,
)
