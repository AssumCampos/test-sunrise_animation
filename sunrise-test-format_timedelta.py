"""
1. Write the code for `format_timedelta()` so that the tests pass.
2. Turn the `test_cases` into proper unit tests.
"""
import unittest
import datetime
import math

PERIODS = [
        ('years', 60*60*24*365.00, int), 
        ('months', 2628000.0, int),
        ('weeks', 60*60*24*7.00, int),
        ('days', 60*60*24.00, int),
        ('hours', 60*60.00, int),
        ('min', 60.00, int),
        ('sec', 1.00, float),
        ('milliseconds', 0.001, float)
    ]

def format_timedelta(timedelta, rounding='years'):
    """
    Returns a string of a nicely formatted time data
    :param timedelta: datetime.timedelta object or seconds as a float/int
    :param rounding: Round result to given value (months, weeks, days, hours, minutes, seconds)
    :return: formatted string
    """
    result = []
    max_reached = False

    # Check if timedelta is a datetime.timedelta object or seconds and get the seconds
    if isinstance(timedelta, int) or isinstance(timedelta, float):
        total_seconds = float(timedelta)
    else:
        total_seconds = timedelta.total_seconds()

    # Iterate from all the periods 
    for period_name, period_seconds, period_type in PERIODS:
        if max_reached or rounding.startswith(period_name):
            max_reached = True
            period_value = total_seconds / period_seconds
            total_seconds = total_seconds % period_seconds 

            if round(period_value) == 0 or period_type(period_value) == 0:
                continue
            if PERIODS[-1][0] == period_name and result != []:
                if round(period_type(total_seconds)) == 0:
                    continue
                result.append([period_type(total_seconds), period_name])
            else:
                result.append([period_type(period_value), period_name])

    # Iterate results and check the type of period for the round
    string_result = []
    for res_value, res_period in result:
        if isinstance(res_value, float):
            # res_value = round(res_value, 4)
            # string_result.append("{} {}".format(res_value, res_period))
            string_result.append("{:.5} {}".format(res_value, res_period))
        else:
            string_result.append("{} {}".format(res_value, res_period))

    return " ".join(string_result)

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

class TestFormatTimeDelta(unittest.TestCase):
    def test_deltatime_years(self):
        self.assertEqual(
            format_timedelta(datetime.timedelta(days=571, seconds=141, microseconds=1412551, milliseconds=1324125, minutes=125, hours=5, weeks=2), "years"),
            "1 years 7 months 1 weeks 9 hours 29 min 26.538 sec")

    def test_number_years(self):
        self.assertEqual(
            format_timedelta(157680002.24178, "years"),
            "5 years 2.2418 sec")

    def test_deltatime_months(self):
        self.assertEqual(
            format_timedelta(datetime.timedelta(days=571, seconds=141, microseconds=1412551, milliseconds=1324125, minutes=125, hours=5, weeks=2), "months"),
            "19 months 1 weeks 9 hours 29 min 26.538 sec")

    def test_number_months(self):
        self.assertEqual(
            format_timedelta(33332704.0, "months"),
            "12 months 2 weeks 6 days 19 hours 5 min 4.0 sec")

    def test_deltatime_days(self):
        self.assertEqual(
            format_timedelta(datetime.timedelta(weeks=7), "days"), 
            "49 days")

    def test_number_days(self):
        self.assertEqual(
            format_timedelta(432000.0, "days"), 
            "5 days")

    def test_deltatime_hours(self):
        self.assertEqual(
            format_timedelta(datetime.timedelta(hours=4, minutes=12, milliseconds=5160)), 
            "4 hours 12 min 5.16 sec")

    def test_number_hours(self):
        self.assertEqual(
            format_timedelta(15125.16), 
            "4 hours 12 min 5.16 sec")

    def test_number_minutes(self):
        self.assertEqual(
            format_timedelta(90, "hours"),
            "1 min 30.0 sec")

    def test_number_seconds(self):
        self.assertEqual(
            format_timedelta(90, "seconds"),
            "90.0 sec")

    def test_number_milliseconds(self):
        self.assertEqual(
            format_timedelta(.01, "seconds"),
            "10.0 milliseconds")

unittest.main()
run_tests()

