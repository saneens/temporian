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

from absl import logging
from absl.testing import absltest
import pandas as pd

from temporian.core import evaluator
from temporian.core.data import dtype
from temporian.core.data.event import Event
from temporian.core.data.feature import Feature
from temporian.core.data.sampling import Sampling
from temporian.core.operators import base
from temporian.proto import core_pb2 as pb
from temporian.core.test import utils
from temporian.implementation.numpy.data.event import NumpyEvent


class EvaluatorTest(absltest.TestCase):
    def toy_event_data(self):
        return NumpyEvent.from_dataframe(
            pd.DataFrame(
                {
                    "timestamp": [0, 2, 4, 6],
                    "f1": [1, 2, 3, 4],
                    "f2": [5, 6, 7, 8],
                }
            )
        )

    def test_schedule_trivial(self):
        a = utils.create_input_event()
        b = utils.OpI1O1(a)

        schedule = evaluator.build_schedule(
            inputs=[a],
            outputs=[b.outputs()["output"]],
        )
        self.assertEqual(schedule, [b])

    def test_schedule_empty(self):
        a = utils.create_input_event()

        schedule = evaluator.build_schedule(
            inputs=[a],
            outputs=[a],
        )
        self.assertEqual(schedule, [])

    def test_schedule_two_delayed_inputs(self):
        i1 = utils.create_input_event()
        i2 = utils.create_input_event()
        o1 = utils.OpI1O1(i1)
        o2 = utils.OpI1O1(i2)
        o3 = utils.OpI2O1(o1.outputs()["output"], o2.outputs()["output"])
        schedule = evaluator.build_schedule(
            inputs=[i1, i2],
            outputs=[o3.outputs()["output"]],
        )
        self.assertTrue(
            (schedule == [o2, o1, o3]) or (schedule == [o1, o2, o3])
        )

    def test_schedule_basic(self):
        i1 = utils.create_input_event()
        o2 = utils.OpI1O1(i1)
        i3 = utils.create_input_event()
        o4 = utils.OpI2O1(o2.outputs()["output"], i3)
        o5 = utils.OpI1O2(o4.outputs()["output"])

        schedule = evaluator.build_schedule(
            inputs=[i1, i3],
            outputs=[o5.outputs()["output_1"], o4.outputs()["output"]],
        )
        self.assertTrue(
            (schedule == [o2, o4, o5]) or (schedule == [o4, o2, o5])
        )

    def test_schedule_mid_chain(self):
        i1 = utils.create_input_event()
        o2 = utils.OpI1O1(i1)
        o3 = utils.OpI1O1(o2.outputs()["output"])
        o4 = utils.OpI1O1(o3.outputs()["output"])
        o5 = utils.OpI1O1(o4.outputs()["output"])

        schedule = evaluator.build_schedule(
            inputs=[o3.outputs()["output"]],
            outputs=[o5.outputs()["output"]],
        )
        self.assertEqual(schedule, [o4, o5])

    def test_evaluate_value(self):
        i1 = utils.create_input_event()
        result = evaluator.evaluate(i1, {i1: self.toy_event_data()})
        self.assertIsInstance(result, NumpyEvent)

    def test_evaluate_list(self):
        i1 = utils.create_input_event()
        i2 = utils.create_input_event()
        result = evaluator.evaluate(
            [i1, i2], {i1: self.toy_event_data(), i2: self.toy_event_data()}
        )
        self.assertIsInstance(result, list)
        self.assertLen(result, 2)

    def test_evaluate_dict(self):
        i1 = utils.create_input_event()
        i2 = utils.create_input_event()
        result = evaluator.evaluate(
            {"i1": i1, "i2": i2},
            {i1: self.toy_event_data(), i2: self.toy_event_data()},
        )
        self.assertIsInstance(result, dict)
        self.assertLen(result, 2)
        self.assertEqual(set(result.keys()), {"i1", "i2"})


if __name__ == "__main__":
    absltest.main()
