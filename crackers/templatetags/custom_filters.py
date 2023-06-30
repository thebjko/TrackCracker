from django import template
from django.db.models import F, FloatField, Case, When

register = template.Library()

@register.filter
def all_completed(obj):
    '''
    하위 태스크들이 모두 완료된 경우.
    (1) 서브태스크가 존재하면서 (2) 현재 task의 pseudo_completed가 False인 경우가 존재하지 않으면 True 반환.
    현재 task의 pseudo_completed는 현재 태스크의 completed와 achievement에서 영향을 받는다.
    1. 현재 태스크의 achievement가 1.0인 경우 True
        1. 하위 태스크들의 pseudo_achievement가 모두 1.0인 경우
        2. 하위 태스크들의 pseudo_completed가 모두 True인 경우
        현재 태스크의 achievement가 1.0이다.
    2. 그렇지 않은 경우 completed를 그대로 반환.
    '''
    return obj.subtasks.exists() and not obj.subtasks.filter(completed=False).exists()