"""
1. Write the code for `format_timedelta()` so that the tests pass.
2. Turn the `test_cases` into proper unit tests.
"""

import datetime

def format_timedelta(timedelta, rounding='years'):
    """
    Returns a string of a nicely formatted time data
    :param timedelta: datetime.timedelta object or seconds as a float/int
    :param rounding: Round result to given value (months, weeks, days, hours, minutes, seconds)
    :return: formatted string
    """
    if isinstance(timedelta, int) or isinstance(timedelta, float):
        total_seconds = float(timedelta)
    else:
        total_seconds = timedelta.total_seconds()

    periods = [
        ('years', 60*60*24*365.25, int), 
        ('months', 60*60*24*30.00, int),
        ('weeks', 60*60*24*7.00, int),
        ('days', 60*60*24.00, int),
        ('hours', 60*60.00, int),
        ('min', 60.00, int),
        ('sec', 1.00, float)
    ]

    result = []
    max_reached = False
    for period_name, period_seconds, period_type in periods:
        if rounding.startswith(period_name) or max_reached:
            max_reached = True
            period_value , total_seconds = divmod(total_seconds, period_seconds)
            if period_value == 0:
                continue
            result.append("{} {}".format(period_type(period_value), period_name))

    return " ".join(result)

def run_tests():
    test_cases = [
        ("1 years 7 months 1 weeks 9 hours 29 min 26.538 sec", "years",
         datetime.timedelta(days=571, seconds=141, microseconds=1412551, milliseconds=1324125, minutes=125, hours=5, weeks=2)),
        ("2 days 2 hours", "years", datetime.timedelta(days=2, hours=2)),
        ("4 hours 12 min 5.16 sec", "years", 15125.16),
        ("1 min 30.0 sec", "years", 90),
        ("52.0 sec", "years", 52),
        ("5 years 2.2418 sec", "years", 157680002.24178),
        # test rounding
        ("19 months 1 weeks 9 hours 29 min 26.538 sec", "months",
         datetime.timedelta(days=571, seconds=141, microseconds=1412551, milliseconds=1324125, minutes=125, hours=5, weeks=2)),
        ("12 months 2 weeks 6 days 19 hours 5 min 4.0 sec", "months", datetime.timedelta(seconds=7897984, minutes=12, hours=9, weeks=42)),
        ("7 weeks 3 days 20 hours 49 min 42.75 sec", "weeks", 4567782.75),
        ("1 weeks", "weeks", 604800),
        ("49 days", "days", datetime.timedelta(weeks=7)),
        ("5 days", "days", datetime.timedelta(days=5)),
        ("4 hours 12 min 5.16 sec", "years", 15125.16),
        ("1 min 30.0 sec", "hours", 90),
        ("52.0 sec", "minutes", 52),
        ("90.0 sec", "seconds", 90),
        ("10.0 milliseconds", "seconds", .01),
    ]
    all_results = []
    print("   | Match   | Result ")
    print(f"---|---------|{max(len(str(i[0]))+1 for i in test_cases) * '-'}")
    for i, (expected_result, test_rounding, test_input) in enumerate(test_cases):
        result = format_timedelta(test_input, rounding=test_rounding)
        is_match = result == expected_result
        all_results.append(is_match)
        msg = f"{i + 1:>2} | {is_match!r:<8}| {result}"
        if not is_match:
            msg += f"\n{'':15}{expected_result} << Expected"
        print(msg)
    print(f"---|---------|{max(len(str(i[0])) + 1 for i in test_cases) * '-'}")
    print(f"\n{sum(all_results)}/{len(all_results)} tests passed")
    if all(all_results):
        print("Test passed!")
    else:
        print("Test failed!")


run_tests()