
from findashboard.constants import VALUE_HIT, VALUE_RECOVER, VALUE_NEUTRAL
from findashboard.constants import FORMAT_CURRENCY


def process_threshold_top(column_now, column_previous, value_threshold):
    hit_now = column_now >= value_threshold
    hit_previous = column_previous >= value_threshold

    if not hit_previous and hit_now:
        return VALUE_HIT
    elif hit_previous and not hit_now:
        return VALUE_RECOVER
    else:
        return VALUE_NEUTRAL


def process_threshold_bottom(column_now, column_previous, value_threshold):
    hit_now = column_now <= value_threshold
    hit_previous = column_previous <= value_threshold

    if not hit_previous and hit_now:
        return VALUE_HIT
    elif hit_previous and not hit_now:
        return VALUE_RECOVER
    else:
        return VALUE_NEUTRAL


def format_currency(x):

    try:
        if x < 0:
            return ("("+FORMAT_CURRENCY+")").format(abs(x))
        return FORMAT_CURRENCY.format(x)
    except Exception as e:
        return x