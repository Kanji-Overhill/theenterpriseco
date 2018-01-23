from django import template

register = template.Library()

@register.filter(name='bedroomcheck')
def bedroomcheck(value):
    if value != 0:
        return value
    else:
        return "Studio"

#Otro metodo register.filter('bedroomcheck', bedroomcheck)