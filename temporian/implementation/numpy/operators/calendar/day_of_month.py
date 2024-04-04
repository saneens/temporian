# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable

from temporian.core.operators.calendar.day_of_month import (
    CalendarDayOfMonthOperator,
)
from temporian.implementation.numpy import implementation_lib
from temporian.implementation.numpy.operators.calendar.base import (
    BaseCalendarNumpyImplementation,
)
from temporian.implementation.numpy_cc.operators import operators_cc


class CalendarDayOfMonthNumpyImplementation(BaseCalendarNumpyImplementation):
    def _implementation(self) -> Callable:
        return operators_cc.calendar_day_of_month


implementation_lib.register_operator_implementation(
    CalendarDayOfMonthOperator, CalendarDayOfMonthNumpyImplementation
)
