from django import template

register = template.Library()


@register.simple_tag(name='numtostr')
def numtostr(value):
    str_num = "1"
    for i in range(2, value+1):
        str_num = str_num + str(i)
    return str_num
