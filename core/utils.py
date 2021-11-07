from typing import Any

from django.core.exceptions import EmptyResultSet
from django.urls import reverse
from django.utils.http import urlencode


def calculate_median(temperature_list: list) -> Any:
    """
    Calculates the median value from an list of values.
    Alternative way is to use the 'median' function in the
    python statistics standard library.
    """
    # sort array to arrange in ascending order
    temperature_list.sort()

    # if array is empty, then return none as
    # there wouln't be any calculation done.
    if len(temperature_list) == 0:
        raise EmptyResultSet("no median for empty data")
    elif len(temperature_list) % 2 == 0:
        # get middle index
        middle_index = len(temperature_list) // 2
        # to get the median, we get the no. in the middle and
        # add it to the next immediate index value.
        # Divide the result by 2 to obtain the median.
        sum_of_two_mid_index_values = (
            temperature_list[middle_index - 1] + temperature_list[middle_index]
        )
        median = sum_of_two_mid_index_values // 2
        return round(median, 2)
    else:
        # to get the median in a list of an odd numbered length,
        # get the mid index value.
        middle_index = len(temperature_list) // 2
        median = temperature_list[middle_index]
        return round(median, 2)


def build_url(url, **kwargs):
    """
    builds urls with query params by accepting
    multiple params as key value pairs
    """
    params = kwargs.pop("params", {})
    built_url = url
    if params:
        built_url += "?" + urlencode(params)
    return built_url


def build_reverse_url(*args, **kwargs):
    """
    builds urls with query params by accepting
    multiple params as key value pairs in reversed urls.
    """
    params = kwargs.pop("params", {})
    built_url = reverse(*args, **kwargs)
    if params:
        built_url += "?" + urlencode(params)
    return built_url
