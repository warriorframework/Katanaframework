#!/usr/bin/env python
'''
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import os
import site
import shutil
import sys
import time
import subprocess
import requests
import json
import pkg_resources
from os.path import abspath, dirname
from termcolor import colored
from collections import OrderedDict

try:
    import katana

    os.environ["pipmode"] = "True"
# except ModuleNotFoundError as error:
except:
    WARRIORDIR = dirname(dirname(abspath(__file__)))
    sys.path.append(WARRIORDIR)
    try:
        import katana

        os.environ["pipmode"] = "False"
    except:
        raise

from katana.utils.navigator_util import Navigator

nav_obj = Navigator()
BASE_DIR = nav_obj.get_katana_dir()
appmanage_py = os.path.join(BASE_DIR, "appmanage.py")

data = requests.get('https://pypi.python.org/pypi/katanaframework/json')
data = data.json()
ord_dict = OrderedDict()
ord_dict = data['releases'].keys()
versn_list = list(ord_dict)

if (os.path.exists(os.path.join(BASE_DIR, 'wapps')) or os.path.exists(os.path.join(BASE_DIR, 'native'))):
    print(colored("Please manually backup and then delete the following dirs before performing the upgrade operation", "red"))
    print(colored("1. katana/native", "red"))
    print(colored("2. katana/wapps", "red"))
    sys.exit()

try:
    if (sys.argv[1] in ['-v', '-V'] and sys.argv[2] is not None):
        if sys.argv[2] == pkg_resources.get_distribution("katanaframework").version:
            print(colored("Current version of katanaframework is same as the given version, please restore the manually backed up wapps and native dirs, then run manage.py runserver", "green"))
            sys.exit()
except Exception as e:
    if pkg_resources.get_distribution("katanaframework").version == versn_list[-1]:
        print(colored("You have already installed the latest version of katanaframework, please restore the manually backed up wapps and native dirs, then run manage.py runserver", "green"))
        sys.exit()

if os.environ["pipmode"] == "True":
    virtual_env = os.getenv('VIRTUAL_ENV')
    if virtual_env:
        katana_configs_dir = virtual_env + os.sep + "katana_configs"
        backup_dir = virtual_env + os.sep + ".backup/katana_configs"
    elif os.path.exists(site.getuserbase() + os.sep + "katana_configs"):
        katana_configs_dir = site.getuserbase() + os.sep + "katana_configs"
        backup_dir = site.getuserbase() + os.sep + ".backup/katana_configs"
    elif os.path.exists("/usr/local/katana_configs"):
        katana_configs_dir = "/usr/local/katana_configs"
        backup_dir = "/usr/local" + os.sep + ".backup/katana_configs"
    else:
        print("--An error occured: Could not find katana_configs directory")
        sys.exit()
else:
    print("--An error occured: Could not find an existing katanaframework PIP package.")
    sys.exit()

print(colored("Upgrading Katana framework, please hold on a moment !", "green"))
time.sleep(1)
print(colored("Preparing to backup of Katana framework...", "green"))
if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir)
if os.path.exists(katana_configs_dir):
    shutil.copytree(katana_configs_dir, backup_dir)
    time.sleep(1)
    print(colored("Backup successful" + u'\u2713', "green"))
    #upgrade command here
    try:
        if len(sys.argv) == 1:
            _pkg = 'katanaframework==' + versn_list[-1]
            output_log = subprocess.call(['pip', 'install' , _pkg])
        elif len(sys.argv) == 3:
            if sys.argv[1] in ['-v', '-V']:
                data = requests.get('https://pypi.python.org/pypi/katanaframework/json')
                json_data = data.json()
                versions_list = json_data["releases"].keys()
                if sys.argv[2].strip() in versions_list:
                    output_log = subprocess.call(['pip', 'uninstall', 'katanaframework', '-y'])
                    _pkg = 'katanaframework==' + sys.argv[2].strip()
                    output_log = subprocess.call(['pip', 'install', _pkg])
                else:
                    print(colored("Error: Could't find the specified version of katanaframework, please check the version you have provided and try again.", "red"))
                    sys.exit()
        else:
            print(colored("Version number is missing.", "red"))
            sys.exit()
    except Exception as e:
        print(colored("Unable to upgrade katanaframework, because of the below error:\n", "red"))
        print(e)
        sys.exit()
    else:
        if os.path.exists(backup_dir):
            if os.path.exists(katana_configs_dir):
                shutil.rmtree(katana_configs_dir)
            shutil.copytree(backup_dir, katana_configs_dir)
            time.sleep(1)
            print(colored("Data files restored successfully" + u'\u2713', "green"))
            time.sleep(1)
            print(colored("Katana framework upgrade completed.", "green"))
            print(colored("Please run appmanage.py to restore the katana configuration", "green"))
        else:
            print(colored("Backup not found!", "red"))
            sys.exit()
else:
    print(colored("Unable to backup the data ({0} directory not found!)", "red").format(katana_configs_dir))
    sys.exit()    
