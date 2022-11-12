# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from pytorch_lightning import Trainer
from pytorch_lightning.loggers import TensorBoardLogger
from tests_pytorch.loggers.test_logger import CustomLogger


def test_trainer_loggers_property(tmp_path):
    """Test for correct initialization of loggers in Trainer."""
    logger1 = CustomLogger()
    logger2 = CustomLogger()

    # trainer.loggers should be a copy of the input list
    trainer = Trainer(logger=[logger1, logger2])

    assert trainer.loggers == [logger1, logger2]

    # trainer.loggers should create a list of size 1
    trainer = Trainer(logger=logger1)

    assert trainer.logger == logger1
    assert trainer.loggers == [logger1]

    # trainer.loggers should be a list of size 1 holding the default logger
    trainer = Trainer(logger=TensorBoardLogger(tmp_path))

    assert trainer.loggers == [trainer.logger]
    assert isinstance(trainer.logger, TensorBoardLogger)


def test_trainer_loggers_setters(tmp_path):
    """Test the behavior of setters for trainer.logger and trainer.loggers."""
    logger1 = CustomLogger()
    logger2 = CustomLogger()

    trainer = Trainer(logger=TensorBoardLogger(tmp_path))
    assert type(trainer.logger) == TensorBoardLogger
    assert trainer.loggers == [trainer.logger]

    # Test setters for trainer.logger
    trainer.logger = logger1
    assert trainer.logger == logger1
    assert trainer.loggers == [logger1]

    trainer.logger = None
    assert trainer.logger is None
    assert trainer.loggers == []

    # Test setters for trainer.loggers
    trainer.loggers = [logger1, logger2]
    assert trainer.loggers == [logger1, logger2]

    trainer.loggers = [logger1]
    assert trainer.loggers == [logger1]
    assert trainer.logger == logger1

    trainer.loggers = []
    assert trainer.loggers == []
    assert trainer.logger is None

    trainer.loggers = None
    assert trainer.loggers == []
    assert trainer.logger is None


@pytest.mark.parametrize(
    "logger_value",
    [
        None,
        False,
        [],
    ],
)
def test_no_logger(tmpdir, logger_value):
    """Test the cases where logger=None, logger=False, logger=[] are passed to Trainer."""
    if logger_value is False:
        with pytest.deprecated_call(match=r"logger=False\)` has been deprecated"):
            trainer = Trainer(default_root_dir=tmpdir, logger=logger_value)
    else:
        trainer = Trainer(default_root_dir=tmpdir, logger=logger_value)
    assert trainer.logger is None
    assert trainer.loggers == []
    assert trainer.log_dir == tmpdir
