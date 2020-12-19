# -*- coding: utf-8 -*-
import os
import shutil
import zipfile
from pathlib import Path
from setuptools import setup, find_packages
from makeInstallScript import create_install_script


########## PACKAGE INFO ##########
name = 'executorUpdater'
description='Tester Side Executor Software Updater'
version ='1.2'
author='Farsens'
author_email='info@farsens.com'
url='https://www.farsens.com'

try:
    # Clean previous outputs
    old_dist_files = os.listdir(Path('dist'))
    for file in old_dist_files:
        os.remove(Path('dist/' + file))
except Exception as e:
    os.mkdir(Path('dist'))
    pass

# Read additional files
with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read()

# Create wheel
setup(
    name=name,
    version=version,
    description=description,
    long_description=readme,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requirements
)

wheel_name = name + '-' + version + '-py3-none-any.whl'

# Create version.txt
version_file = open('dist/version.txt','w+')
version_file.write(version)
version_file.close()

# Create install.sh
create_install_script(name, description, wheel_name)

# Zip dist folder
dist_zip = zipfile.ZipFile('dist\\' + name + '_' + version + '.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
dist_zip.write(Path('./dist/' + wheel_name), arcname=wheel_name)
dist_zip.write(Path('./dist/version.txt'), arcname='version.txt')
dist_zip.write(Path('./dist/install.sh'), arcname='install.sh')
dist_zip.close()

# Delete intermediate files
os.remove(Path('./dist/' + wheel_name))
os.remove(Path('./dist/version.txt'))
os.remove(Path('./dist/install.sh'))
shutil.rmtree(Path(name + '.egg-info'))
shutil.rmtree(Path('build'))
