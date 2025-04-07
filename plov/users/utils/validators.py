import datetime

import django.core.exceptions
import django.utils.deconstruct
import django.utils.timezone


@django.utils.deconstruct.deconstructible
class YearRangeValidator:
    def __init__(self, min_year, years_offset_from_current=0):
        """
        Args:
            min_year (int): Absolute minimum allowed year (e.g., 2000)
            years_offset_from_current (int):
                - Positive: allows X years in future (e.g., +1)
                - Negative: restricts to X years in past (e.g., -10)
                - Zero: exactly current year
        """
        self.min_year = min_year
        self.years_offset = years_offset_from_current

    def __call__(self, value):
        current_year = django.utils.timezone.now().year
        max_year = current_year + self.years_offset
        if isinstance(value, (datetime.date, datetime.datetime)):
            value = value.year

        if not (self.min_year <= value <= max_year):
            raise django.core.exceptions.ValidationError(
                self.get_error_message(current_year),
                params={'value': value},
            )

    def get_error_message(self, current_year):
        if self.years_offset > 0:
            return f'Year must be between {self.min_year} and {current_year + self.years_offset}.'

        elif self.years_offset < 0:
            return f'Year must be between {self.min_year} and {current_year + self.years_offset}.'

        return f'Year must be exactly {current_year}.'
