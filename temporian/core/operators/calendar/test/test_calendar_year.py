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

from absl.testing import absltest
from absl.testing.parameterized import TestCase

from temporian.implementation.numpy.data.io import event_set
from temporian.test.utils import assertOperatorResult, i32


class CalendarYearTest(TestCase):
    def test_basic(self):
        timestamps = [
            "1960-01-01 00:00:00",
            "1970-01-01 00:00:00",
            "2021-01-01 00:00:00",
            "2021-01-01 00:00:01",
            "2021-12-31 23:59:59",
            "2045-12-31 23:59:59",
        ]
        evset = event_set(timestamps=timestamps)

        expected = event_set(
            timestamps=timestamps,
            features={
                "calendar_year": i32([1960, 1970, 2021, 2021, 2021, 2045]),
            },
            same_sampling_as=evset,
        )

        result = evset.calendar_year()
        assertOperatorResult(self, result, expected)


if __name__ == "__main__":
    absltest.main()
