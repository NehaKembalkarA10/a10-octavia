#    Copyright 2019, A10 Networks
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


from taskflow import task

from octavia.controller.worker import task_utils as task_utilities
from octavia.common import constants
import acos_client
from octavia.amphorae.driver_exceptions import exceptions as driver_except
import time
from oslo_log import log as logging
from oslo_config import cfg
from a10_octavia.common import openstack_mappings
from a10_octavia.controller.worker.tasks.policy import PolicyUtil
from a10_octavia.controller.worker.tasks import persist
from a10_octavia.controller.worker.tasks.common import BaseVThunderTask

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

class MemberCreate(BaseVThunderTask):
    """Task to update amphora with all specified member configurations."""

    def execute(self, member, vthunder, pool):
        """Execute create member for an amphora."""
        try:
            c = self.client_factory(vthunder)
            out = c.slb.server.create(member.id, member.ip_address)
            LOG.info("Member created successfully.")
        except Exception as e:
            print(str(e))
        try:
            c = self.client_factory(vthunder)
            out = c.slb.service_group.member.create(pool.id, member.id, member.protocol_port)
            LOG.info("Member associated to pool successfully.")
        except Exception as e:
            print(str(e))
            LOG.info("Error occurred")


class MemberDelete(BaseVThunderTask):
    """Task to update amphora with all specified member configurations."""

    def execute(self, member, vthunder, pool):
        """Execute delete member for an amphora."""
        axapi_version = acos_client.AXAPI_21 if vthunder.axapi_version == 21 else acos_client.AXAPI_30
        try:
            c = self.client_factory(vthunder)
            out = c.slb.service_group.member.delete(pool.id, member.id, member.protocol_port)
            LOG.info("Member de-associated to pool successfully.")
        except Exception as e:
            print(str(e))
        try:
            c = self.client_factory(vthunder)
            out = c.slb.server.delete(member.id)
            LOG.info("Member deleted successfully.")
        except Exception as e:
            print(str(e))
            LOG.info("Error occurred")

