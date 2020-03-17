#    Copyright 2020, A10 Networks
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


try:
    from unittest.mock import patch
except ImportError:
    import mock
    from mock import patch

from octavia.tests.unit import base


class BaseTaskTestCase(base.TestCase):

    def setUp(self):
        self.client_mock = mock.Mock()
        config = {'return_value': self.client_mock}
        patcher = patch(
            'a10_octavia.controller.worker.tasks.common.BaseVThunderTask.client_factory', **config)
        mock_patch = patcher.start()
        super(base.TestCase, self).setUp()
