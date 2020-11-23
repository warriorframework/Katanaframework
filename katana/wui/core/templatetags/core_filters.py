from django import template
from katana.utils.json_utils import read_json_data
from katana.utils.navigator_util import Navigator
import os


nav_obj = Navigator()
BASE_DIR = nav_obj.get_katana_dir()

register = template.Library()

if os.environ["pipmode"] == "True":
    virtual_env = os.getenv('VIRTUAL_ENV')
    if virtual_env:
        app_config_file = virtual_env + os.sep + "katana_configs" + os.sep + "app_config.json"
    elif os.path.exists(site.getuserbase() + os.sep + "katana_configs"):
        app_config_file = site.getuserbase() + os.sep + "katana_configs" + os.sep + "app_config.json"
    elif os.path.exists("/usr/local/katana_configs"):
        app_config_file = "/usr/local/katana_configs/app_config.json"
    else:
        print("--An error occured: Can not find katana_configs directory")
        exit()
else:
    app_config_file = os.path.join(BASE_DIR, "katana_configs", "app_config.json")

@register.filter(name="get_app_name", is_safe=True)
def get_app_name(value):
    fname_file = os.path.join(BASE_DIR, "wui/core/static/core/framework_name.json")
    data = read_json_data(fname_file)
    appname = data["fr_name"]
    return appname


@register.filter(name="check_timer_flag", is_safe=True)
def check_timer_flag(value):
    data = read_json_data(app_config_file)
    Flag = data["enable_utc_clock"].lower()
    return Flag


@register.filter(name="check_fujitsu_logo_flag", is_safe=True)
def check_fujitsu_logo_flag(value):
    data = read_json_data(app_config_file)
    Flag = data["enable_fujitsu_logo"].lower()
    return Flag


@register.filter(name='check_logintype', is_safe=True)
def check_logintype(value):
    if os.environ.get('KEYCLOAK_AUTH', False) in ['True', 'true']:
        return "keycloak"
    else:
        return "default"
