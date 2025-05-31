#!/usr/bin/python3
"""Deploy web static module
"""
from fabric.api import local, put, run, env
from datetime import datetime
from os.path import isfile

env.hosts = ["44.201.238.52", "54.157.252.190"]


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder
    of AirBnB Clone v2.
    """
    # Create versions folder (if not exits)-> -p
    local("mkdir -p versions")
    # Create web_static file with date and extension .tgz
    now = datetime.now()
    name = "versions/web_static_{}".format(now.strftime("%Y%m%d%H%M%S"))
    name += ".tgz"
    # Create tgz
    compressCommand = "tar -cvzf {} web_static".format(name)
    # Return de path if the file was created
    if local(compressCommand) == 1:
        return None
    return name


def do_deploy(archive_path):
    """Deploy web_static to your web servers
    Args:
    archive_path: path of web_static.tgz
    """
    # if the path doesn't exists
    if isfile(archive_path) is False:
        return False
    try:
        compressFile = archive_path.split("/")[1]
        name = archive_path.split("/")[1].split(".")[0]
        # upload the archive_path in /tmp/
        put(archive_path, "/tmp/{}".format(compressFile))

        # Path of releases
        path = "/data/web_static/releases/{}/".format(name)
        # create the directory where are going to be uncompress
        command = "mkdir -p " + path
        run(command)

        # uncompress the file into /data/web_static/releases/
        command = "tar -xzf /tmp/{} -C ".format(compressFile)
        command += path
        run(command)

        # delete file from server
        command = "rm /tmp/{}".format(compressFile)
        run(command)

        # move all the files into the dir releases/web_static<number>
        command = "mv /data/web_static/releases/{}".format(name)
        command += "/web_static/* "
        command += path
        run(command)

        # delete the folder that create the uncompres process
        command = "rm -rf /data/web_static/releases/{}".format(name)
        command += "/web_static"
        run(command)

        # delete the symbolic link
        command = "rm -rf /data/web_static/current"
        run(command)

        # create symbolic link
        command = "ln -s /data/web_static/releases/{}/ ".format(name)
        command += "/data/web_static/current"
        run(command)
    except Exception:
        return False  # Fail
    return True  # Correct


def deploy():
    """Compress web static and distributes to the web servers
    """
    # compress web static in file with extension .tgz
    archive_path = do_pack()

    if archive_path is None:  # verification
        return False

    return do_deploy(archive_path)
