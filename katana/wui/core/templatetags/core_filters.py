from django import template
import os

register = template.Library()


@register.filter(name='check_logintype', is_safe=True)
def check_logintype(value):
    if os.environ.get('KEYCLOAK_AUTH', False) in ['True', 'true']:
        return "keycloak"
    else:
        return "default"