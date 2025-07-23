from django import template

register = template.Library()

@register.simple_tag
def update_query_params(request, page_number):
    query_dict = request.GET.copy()
    query_dict['page'] = page_number
    return query_dict.urlencode()
