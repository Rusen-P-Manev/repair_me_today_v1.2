from django import template

register = template.Library()


@register.filter(name='format_phone')
def format_phone(value):
    if not value:
        return value

    value = str(value).replace(" ", "")

    if len(value) == 10 and value.startswith("0"):
        return f"{value[:4]} {value[4:7]} {value[7:]}"
    elif len(value) == 13 and value.startswith("+359"):
        return f"{value[:4]} {value[4:6]} {value[6:9]} {value[9:]}"

    return value

@register.filter(name='has_group')
def has_group(user, group_name):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=group_name).exists()