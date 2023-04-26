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

import numpy as np

from temporian.implementation.numpy import implementation_lib
from temporian.core.operators.window.moving_standard_deviation import (
    MovingStandardDeviationOperator,
)
from temporian.implementation.numpy.operators.window.base import (
    BaseWindowNumpyImplementation,
)


class MovingStandardDeviationNumpyImplementation(BaseWindowNumpyImplementation):
    """Numpy implementation of the moving standard deviation operator."""

    def __init__(self, operator: MovingStandardDeviationOperator) -> None:
        super().__init__(operator)

    def _apply_operation(self, values: np.array) -> np.array:
        """Calculates the standard deviation of the values in each row in the
        input.

        NaNs are ignored.

        See base class for further info.
        """
        return np.nanstd(values, axis=1)


implementation_lib.register_operator_implementation(
    MovingStandardDeviationOperator, MovingStandardDeviationNumpyImplementation
)
