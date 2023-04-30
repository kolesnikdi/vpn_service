from django.db.models import Q
from rest_framework.filters import BaseFilterBackend, SearchFilter

FILTERING_AVAILABLE_FIELDS = ['cost', 'volume']


def perform_product_filtering(view_obj, queryset):
    """Use rest_framework def filter_queryset(self, queryset) to launch all filters in
     LocationMenuView.PRODUCT_FILTER_BACKENDS. This function is equal to sequentially launching objects directly from
     LocationMenuView:
     def retrieve(self, request, *args, **kwargs):
        # CustomSearchFilter() - must make object to transfer self in to
        #.filter_queryset(self.request, product_qs, self)
        product_qs = CustomSearchFilter().filter_queryset(self.request, product_qs, self)
        product_qs = CustomRangeFilter().filter_queryset(self.request, product_qs, self)
        product_qs = filters.OrderingFilter().filter_queryset(self.request, product_qs, self)
        product_qs = DjangoFilterBackend().filter_queryset(self.request, product_qs, self)
    """
    for backend in list(view_obj.PRODUCT_FILTER_BACKENDS):
        queryset = backend().filter_queryset(view_obj.request, queryset, view_obj)
    return queryset


class CustomSearchFilter(SearchFilter):
    """Customized Search. Search will be active only when request >= 3 symbols """

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms or len(search_terms[0]) < 3:
            return queryset
        return super().filter_queryset(request, queryset, view)


class CustomRangeFilter(BaseFilterBackend):
    """ Own filter. Allows to filter queryset in fields 'cost', 'volume':
    from the specified parameter to the end;
    from beginning to the specified parameter;
    from the specified parameter to the specified parameter;
    filter by several fields simultaneously;
    Comands - range_cost range_volume"""

    def filter_queryset(self, request, queryset, view):
        query = Q()
        for param in request.query_params.keys():
            if not param.startswith('range_'):
                # The important part. Does not allow other rest_framework.filters to use this filter
                continue
            name = param[6:]
            if name not in FILTERING_AVAILABLE_FIELDS:
                # Allows you to use filtering only in the allowed fields
                continue
            if range_value := request.query_params.get(param):
                range_number = [range_part.strip() for range_part in range_value.split(',')]
                # create list which everything that is not int becomes 0
                if len(range_number) != 2:
                    # exclude wrong input
                    continue

                begin, end = [int(number) if number.isdigit() else 0 for number in range_number]
                if end != 0 and begin > end:
                    begin, end = end, begin
                query = query & Q(**{f'{name}__gte': begin})
                # second empty query needs for not to rewriting query after second filter comand
                if end > 0:
                    query = query & Q(**{f'{name}__lte': end})

        queryset = queryset.filter(query)
        return queryset
