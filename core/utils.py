from typing import Any

from django.core.exceptions import EmptyResultSet

def calculate_median(temperature_list: list) -> Any:
    """Calculates the median value from an list of values"""
    # sort array to arrange in ascending order
    temperature_list.sort()

    # if array is empty, then return none as
    # there wouln't be any calculation done.
    if len(temperature_list) == 0:
        raise EmptyResultSet("no median for empty data")
    elif len(temperature_list) % 2 == 0:
        print(
            len(temperature_list),
        )
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
        #  get the mid index value.
        middle_index = len(temperature_list) // 2
        median = temperature_list[middle_index]
        return round(median, 2)
