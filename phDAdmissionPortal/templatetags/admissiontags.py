from django import template
from django.template import Template

register = template.Library()

@register.filter()
def intHash(h, key):
    return int(h[key])

@register.filter()
def fpHash(h, key):
    return float(h[key])

@register.filter()
def dateHash(h, key):
    return h[key]

@register.filter()
def dictToStr(dict):
    return str(dict)

@register.filter()
def getHashValue(h, key):
    return h[key]

@register.filter()
def getHashValueItems(h, key):
    return h[key].items()

@register.filter()
def firstElement(l):
    return l[0]

@register.filter()
def hasItemInList(l,key):
    return key in l

@register.filter()
def getFirstKey(h):
    return list(h.keys())[0]


@register.filter()
def hasAtleastOneConstraint(h):
    listOfConstraints = list(h.values())
    listOfNonEmptyConstraints = list(filter(({}).__ne__, listOfConstraints))
    return listOfNonEmptyConstraints


