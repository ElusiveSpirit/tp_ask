from django import template
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('ask/includes/best_tags.html')
def best_tags():
    tags = cache.get('best_tags')
    classes = [
        '',
        'text-danger',
        '',
        'text-danger',
        'text-success',
        '',
        '',
        'text-warning',
        '',
        '',
    ]
    tags_with_classes = []
    for i in range(len(tags)):
        tags_with_classes.append({
            'tag' : tags[i],
            'class' : classes[i]
        })

    return {
        'best_tags' : tags_with_classes
    }

@register.inclusion_tag('ask/includes/best_members.html')
def best_members():
    return {
        'best_members' : cache.get('best_members')
    }
