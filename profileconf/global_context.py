from profileconf.domain import ContextFunction, RestrictedList

__author__ = 'corvis'


def __build_restricted_list_from_string(restriction):
    def func(items_str, context):
        items = []
        for x in items_str.split(','):
            items.append(x.strip())
        return RestrictedList(items, restriction=restriction)
    return func

# Restrict collection
one_of = ContextFunction.builder().set_name('oneof').set_context_tag('global')\
    .set_handler(__build_restricted_list_from_string(RestrictedList.ANY_OF)).build()
only = ContextFunction.builder().set_name('only').set_context_tag('global')\
    .set_handler(__build_restricted_list_from_string(RestrictedList.ONLY)).build()
all = ContextFunction.builder().set_name('all').set_context_tag('global')\
    .set_handler(__build_restricted_list_from_string(RestrictedList.ALL)).build()