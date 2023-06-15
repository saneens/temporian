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
import os
from absl import flags
import temporian as tp

from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
import apache_beam as beam
import temporian.beam as tp_beam


def test_data() -> str:
    return os.path.join(flags.FLAGS.test_srcdir, "temporian")


class TFPTest(absltest.TestCase):
    def test_base(self):
        input_csv_path = os.path.join(
            test_data(), "temporian/test/test_data/io/input.csv"
        )

        a = tp.input_node(
            features=[
                ("sales", tp.float32),
                ("client", tp.str_),
            ]
        )
        b = tp.add_index(a, "client")
        c = tp.moving_sum(b, tp.duration.weeks(1))

        with TestPipeline() as p:
            output = (
                p
                | tp_beam.read_csv(input_csv_path)
                | tp_beam.run(inputs=a, outputs=c)
            )
            assert_that(output, equal_to([]))


if __name__ == "__main__":
    absltest.main()
