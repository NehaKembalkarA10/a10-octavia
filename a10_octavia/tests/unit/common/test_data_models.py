# Copyright 2020, A10 Networks.
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

import copy
import datetime

from oslo_utils import uuidutils

from a10_octavia.common import data_models
from a10_octavia.tests.unit import base


class TestDataModels(base.BaseTaskTestCase):

    def setUp(self):

        super(TestDataModels, self).setUp()
        self.AMP_ID = uuidutils.generate_uuid()
        self.CREATED_AT = datetime.datetime.now()
        self.UPDATED_AT = datetime.datetime.utcnow()
        self.LAST_UDP_UPDATE = datetime.datetime.utcnow()

        self.AMP_obj = data_models.AmphoraMeta(
            id=self.AMP_ID,
            created_at=self.CREATED_AT,
            updated_at=self.UPDATED_AT,
            last_udp_update=self.LAST_UDP_UPDATE,
            status="ACTIVE"
        )

    def test_AmphoraMeta_update(self):

        new_id = uuidutils.generate_uuid()
        new_created_at = self.CREATED_AT + datetime.timedelta(minutes=5)
        new_updated_at = self.UPDATED_AT + datetime.timedelta(minutes=10)
        new_last_udp_update = self.LAST_UDP_UPDATE + datetime.timedelta(minutes=5)
        new_status = "ERROR"

        update_dict = {
            'id': new_id,
            'created_at': new_created_at,
            'updated_at': new_updated_at,
            'last_udp_update': new_last_udp_update,
            'status': new_status
        }

        test_Amp_obj = copy.deepcopy(self.AMP_obj)

        reference_Amp_obj = data_models.AmphoraMeta(
            id=new_id,
            created_at=new_created_at,
            updated_at=new_updated_at,
            last_udp_update=new_last_udp_update,
            status=new_status
        )

        test_Amp_obj.update(update_dict)

        self.assertEqual(reference_Amp_obj, test_Amp_obj)