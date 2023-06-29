from django import template

register = template.Library()

@register.filter
def all_completed(obj):
    return not obj.subtasks.filter(completed=False).exists()