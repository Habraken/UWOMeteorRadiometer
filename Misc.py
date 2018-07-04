
import platform
import os
import shutil
import errno
import logging
import subprocess

# Get the logger from the main module
log = logging.getLogger("logger")


def mkdirP(path):
    """ Makes a directory and handles all errors.
    """

    # Try to make a directory
    try:
        os.makedirs(path)

    # If it already exist, do nothing
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass

    # Raise all other errors
    except:
        raise 



def archiveDir(source_dir, file_list, dest_dir, compress_file, delete_dest_dir=False, extra_files=None):
    """ Move the given file list from the source directory to the destination directory, compress the 
        destination directory and save it as a .bz2 file. BZ2 compression is used as ZIP files have a limit
        of 2GB in size.

    Arguments:
        source_dir: [str] Path to the directory from which the files will be taken and archived.
        file_list: [list] A list of files from the source_dir which will be archived.
        dest_dir: [str] Path to the archive directory which will be compressed.
        compress_file: [str] Name of the compressed file which will be created.

    Keyword arguments:
        delete_dest_dir: [bool] Delete the destination directory after compression. False by default.
        extra_files: [list] A list of extra files (with fill paths) which will be be saved to the night 
            archive.

    Return:
        archive_name: [str] Full name of the archive.

    """

    # Make the archive directory
    mkdirP(dest_dir)
    
    for file_name in file_list if file_name.endswith(".rdm"):
        # Compress the archive directory
        archive_file_name = shutil.make_archive(os.path.join(source_dir, file_name), 'bztar', source_dir)
    
        shutil.move(archive_file_name,os.path.join(dest_dir, os.path.split(archive_file_name)[1]))

    for graph in file_list if graph.endswith(".png"):
        shutil.move(os.path.join(source_dir, graph), os.path.join(dest_dir, graph))
        
    # Copy the additional files to the archive directory
    if extra_files is not None:
        for file_name in extra_files:
            shutil.copy2(file_name, os.path.join(dest_dir, os.path.basename(file_name)))
    
    # Delete the archive directory after compression
    if delete_dest_dir:
        shutil.rmtree(dest_dir)
    
    return dest_dir



def ping(host):
    """ Ping the host and return True if reachable. 
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.

    Source: https://stackoverflow.com/a/32684938/6002120

    Arguments:
        host: [str] Host name or IP address.

    Return:
        [bool] True if host (str) responds to a ping request.
    """

    # Ping command count option as function of OS
    param = '-n 1' if platform.system().lower()=='windows' else '-c 1'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, host]

    # Pinging
    return subprocess.call(command) == 0
    
if __name__ == "__main__":
    source_dir = "/home/pi/RadiometerData/CapturedData/CA0001_A_20180605-150905"
    compress_file = "CA0001_A_20180605-150905"
    dest_dir = "/home/pi/RadiometerData/ArchivedData"
    archiveDir(source_dir, os.listdir(source_dir), dest_dir, compress_file)
