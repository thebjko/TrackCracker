import markdown as md

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def all_completed(obj):
    return obj.subtasks.exists() and not obj.subtasks.filter(completed=False).exists()

@register.filter
def markdown(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(md.markdown(value, extensions=extensions))
