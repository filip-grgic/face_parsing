import os
import sys
import shutil
import subprocess
from setuptools import find_namespace_packages, setup


def clean_repo():
    repo_folder = os.path.realpath(os.path.dirname(__file__))
    dist_folder = os.path.join(repo_folder, 'dist')
    build_folder = os.path.join(repo_folder, 'build')
    if os.path.isdir(dist_folder):
        shutil.rmtree(dist_folder, ignore_errors=True)
    if os.path.isdir(build_folder):
        shutil.rmtree(build_folder, ignore_errors=True)


# Read version string
_version = None
script_folder = os.path.realpath(os.path.dirname(__file__))
with open(os.path.join(script_folder, 'ibug', 'face_parsing', '__init__.py')) as init:
    for line in init.read().splitlines():
        fields = line.replace('=', ' ').replace('\'', ' ').replace(
            '\"', ' ').replace('\t', ' ').split()
        if len(fields) >= 2 and fields[0] == '__version__':
            _version = fields[1]
            break
if _version is None:
    sys.exit('Sorry, cannot find version information.')

def pull_first():
    """This script is in a git directory that can be pulled."""
    cwd = os.getcwd()
    gitdir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(gitdir)
    try:
        subprocess.call(['git', 'lfs', 'pull'])
    except subprocess.CalledProcessError:
        raise RuntimeError("Make sure git-lfs is installed!")
    os.chdir(cwd)

pull_first()

# Installation
config = {
    'name': 'face_parsing',
    'version': _version,
    'description': 'RoI Tanh-polar Transformer Network for Face Parsing in the Wild.',
    'author': 'Yiming Lin',
    'author_email': 'yimingling.ibug@gmail.com',
    'packages': find_namespace_packages(),
    'package_data': {
        'ibug.face_parsing.resnet.weights': ['*.torch']
    },
    'install_requires': ['numpy>=1.17.0', 'scipy>=1.1.0', 'torch>=1.6.0',
                         'torchvision>=0.7.0', 'opencv-python>= 3.4.2'],
    'zip_safe': False
}
clean_repo()
setup(**config)
clean_repo()
