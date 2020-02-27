from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def simple_paginator(object_list, page: int = 1, limit: int = 10):
    paginator = Paginator(object_list, limit)
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
    return data_list
