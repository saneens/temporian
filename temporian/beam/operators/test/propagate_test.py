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

from temporian.implementation.numpy.data.io import event_set
from temporian.beam.test.utils import check_beam_implementation
from temporian.core.operators.propagate import propagate


class PropagateTest(absltest.TestCase):
    def test_basic(self):
        input_data = event_set(
            timestamps=[1, 2, 3],
            features={
                "a": [1, 2, 3],
                "x": [1, 1, 2],
            },
            indexes=["x"],
        )
        sampling = event_set(
            timestamps=[1, 1, 1, 1],
            features={"x": [1, 1, 2, 2], "y": [1, 2, 1, 2]},
            indexes=["x", "y"],
        )
        output_node = propagate(input_data.node(), sampling.node())
        check_beam_implementation(
            self, input_data=[input_data, sampling], output_node=output_node
        )

    def test_remove_index(self):
        input_data = event_set(
            timestamps=[1, 2],
            features={"a": [1, 2], "x": [1, 2]},
            indexes=["x"],
        )
        sampling = event_set(
            timestamps=[3, 4],
            features={"x": [1, 1], "y": [1, 2]},
            indexes=["x", "y"],
        )
        output_node = propagate(input_data.node(), sampling.node())
        check_beam_implementation(
            self, input_data=[input_data, sampling], output_node=output_node
        )

    def test_add_empty_index(self):
        input_data = event_set(
            timestamps=[1, 2],
            features={"a": [1, 2], "x": [1, 2]},
            indexes=["x"],
        )
        sampling = event_set(
            timestamps=[3, 4, 5, 6],
            features={"x": [1, 1, 3, 3], "y": [1, 2, 4, 5]},
            indexes=["x", "y"],
        )
        output_node = propagate(input_data.node(), sampling.node())
        check_beam_implementation(
            self, input_data=[input_data, sampling], output_node=output_node
        )

    def test_no_feature(self):
        input_data = event_set(
            timestamps=[1, 2],
            features={"x": [1, 2]},
            indexes=["x"],
        )
        sampling = event_set(
            timestamps=[3, 4, 5, 6],
            features={"x": [1, 1, 3, 3], "y": [1, 2, 4, 5]},
            indexes=["x", "y"],
        )
        output_node = propagate(input_data.node(), sampling.node())
        check_beam_implementation(
            self, input_data=[input_data, sampling], output_node=output_node
        )


if __name__ == "__main__":
    absltest.main()
