#!/usr/bin/env python
import os
import sys
import json
import site
from os.path import abspath, dirname

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
from katana.primary_process import install_default_apps
from katana.utils.json_utils import read_json_data
from katana.utils.directory_traversal_utils import join_path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "katana.wui.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    nav_obj = Navigator()
    BASE_DIR = nav_obj.get_katana_dir()
    if os.environ["pipmode"] == "True":
        virtual_env = os.getenv('VIRTUAL_ENV')
        if virtual_env:
            app_config_json_path = virtual_env + os.sep + "katana_configs" + os.sep + "app_config.json"
        elif os.path.exists(site.getuserbase() + os.sep + "katana_configs"):
            app_config_json_path = site.getuserbase() + os.sep + "katana_configs" + os.sep + "app_config.json"
        elif os.path.exists("/usr/local/katana_configs"):
            app_config_json_path = "/usr/local/katana_configs/app_config.json"
        else:
            print("--An error occured: Can not find katana_configs directory")
            exit()
    else:
        app_config_json_path = os.path.join(BASE_DIR, "katana_configs", "app_config.json")

    def read_config_file_data():
            nav_obj = Navigator()
            data = read_json_data(app_config_json_path)
            return data
    app_config_data = read_config_file_data()
    if app_config_data["__userconfigured__"] == "False" and app_config_data["__normal_run__"] == "False":
        app_config_data["__normal_run__"] = "True"
        with open(app_config_json_path, "w") as f:
            json.dump(app_config_data, f)
        install_default_apps('master')

    if app_config_data["__userconfigured__"] == "True":
        if os.path.exists("log.txt"):
            print("=============================KATANA CONFIGURATION LOG================================")
            os.system("tail -n +3 log.txt")
            print("======================================================================================")
            print("\n\n")
    execute_from_command_line(sys.argv)
