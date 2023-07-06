from pydantic import validator

from acc_server_mgr.models.schema import FilterOperator, SortingDir


def apply_filter(query, model, filter_request):
    for field_name, operator, value in filter_request.query:
        field = getattr(model, field_name)
        criterion = apply_operator(field, operator, value)
        query = query.where(criterion)
    return query


def apply_sort(query, model, filter_request):
    sorts = []
    for field_name, direction in filter_request.sort:
        field = getattr(model, field_name)
        if direction == SortingDir.asc:
            sorts.append(field.asc())
        elif direction == SortingDir.desc:
            sorts.append(field.desc())
    return query.order_by(*sorts)


def apply_operator(field, operator, value):
    if operator == FilterOperator.eq:
        return field == value
    elif operator == FilterOperator.neq:
        return field != value
    elif operator == FilterOperator.gt:
        return field > value
    elif operator == FilterOperator.gte:
        return field >= value
    elif operator == FilterOperator.lt:
        return field < value
    elif operator == FilterOperator.lte:
        return field <= value
    elif operator == FilterOperator.contains:
        return field.contains(value)
