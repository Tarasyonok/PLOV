from django import template

register = template.Library()


@register.filter
def can_review(user):
    if not user.is_authenticated:
        return False

    course = user.courses.filter(specialization='D')
    return course.exists() and course.first().is_graduated
