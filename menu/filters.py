from django.db.models import Q
from rest_framework.filters import BaseFilterBackend, SearchFilter

FILTERING_AVAILABLE_FIELDS = ['cost', 'volume']


class CustomSearchFilter(SearchFilter):
    """Customized Search. Search will be active only when request >= 3 symbols """
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms or len(search_terms[0]) < 3:
            return queryset
        return super().filter_queryset(request, queryset, view)


class CustomRangeFilter(BaseFilterBackend):
    """Own filter. Allows to filter queryset in fields 'cost', 'volume':
    from the specified parameter to the end;
    from beginning to the specified parameter;
    from the specified parameter to the specified parameter;
    filter by several fields simultaneously;
    ordering of the filters (from largest to smallest and vice versa).
    The ordering direction is specified in the query where
    from largest to smallest is "400,100" """
    def filter_queryset(self, request, queryset, view):
        query = Q()
        ordering = []
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
                if len(range_number) < 2:
                    # fix coma problem
                    continue
                begin, end, *_ = [int(number) if number.isdigit() else 0 for number in range_number]
                # *_ create list with else that not 'begin' or 'end'
                ordering_param = f'{name}'
                if end != 0 and begin > end:
                    ordering_param = f'-{ordering_param}'
                    begin, end = end, begin
                ordering.append(ordering_param)
                query = query & Q(**{f'{name}__gte': begin})
                # query = Q(**{f'{name}__gte': begin})
                if end > 0:
                    query = query & Q(**{f'{name}__lte': end})

        queryset = queryset.filter(query).order_by(*ordering)
        return queryset
