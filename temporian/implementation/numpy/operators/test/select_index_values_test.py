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

from temporian.core.operators.select_index_values import SelectIndexValues
from temporian.implementation.numpy.data.io import event_set
from temporian.implementation.numpy.operators.select_index_values import (
    SelectIndexValuesNumpyImplementation,
)
from temporian.implementation.numpy.operators.test.test_util import (
    assertEqualEventSet,
    testOperatorAndImp,
)


class SelectIndexValuesOperatorTest(absltest.TestCase):
    def setUp(self):
        pass

    def test_base(self):
        evset = event_set(
            timestamps=[1, 2, 3, 4],
            features={
                "a": [1.0, 2.0, 3.0, 4.0],
                "b": [5, 6, 7, 8],
                "c": ["A", "A", "B", "B"],
            },
            indexes=["c"],
        )
        node = evset.node()

        expected_output = event_set(
            timestamps=[1, 2],
            features={
                "a": [1.0, 2.0],
                "b": [5, 6],
                "c": ["A", "A"],
            },
            indexes=["c"],
        )

        # Run op
        op = SelectIndexValues(input=node, keys=[("A",)])
        instance = SelectIndexValuesNumpyImplementation(op)
        testOperatorAndImp(self, op, instance)
        output = instance.call(input=evset)["output"]

        assertEqualEventSet(self, output, expected_output)


if __name__ == "__main__":
    absltest.main()
