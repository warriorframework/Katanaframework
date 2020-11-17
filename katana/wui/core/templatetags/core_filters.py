from django import template
from katana.utils.json_utils import read_json_data
from katana.utils.navigator_util import Navigator
import os


nav_obj = Navigator()
BASE_DIR = nav_obj.get_katana_dir()

register = template.Library()


@register.filter(name="get_app_name", is_safe=True)
def get_app_name(value):
    fname_file = os.path.join(BASE_DIR, "wui/core/static/core/framework_name.json")
    data = read_json_data(fname_file)
    appname = data["fr_name"]
    return appname


@register.filter(name="check_timer_flag", is_safe=True)
def check_timer_flag(value):
    app_config_file = os.path.join(BASE_DIR, "katana_configs/app_config.json")
    data = read_json_data(app_config_file)
    Flag = data["enable_utc_clock"].lower()
    return Flag


@register.filter(name="check_fujitsu_logo_flag", is_safe=True)
def check_fujitsu_logo_flag(value):
    app_config_file = os.path.join(BASE_DIR, "katana_configs/app_config.json")
    data = read_json_data(app_config_file)
    Flag = data["enable_fujitsu_logo"].lower()
    return Flag
