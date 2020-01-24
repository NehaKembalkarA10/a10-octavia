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


from oslo_log import log as logging
from oslo_config import cfg
from a10_octavia.controller.worker.tasks.common import BaseVThunderTask

CONF = cfg.CONF
LOG = logging.getLogger(__name__)


class MemberCreate(BaseVThunderTask):
    """ Task to create member """

    def execute(self, member, vthunder, pool):
        """ Execute create member """

        conn_limit = self.readConf('SERVER', 'conn_limit')
        if conn_limit is not None:
            conn_limit = int(conn_limit)
        conn_resume = self.readConf('SERVER', 'conn_resume')
        if conn_resume is not None:
            conn_resume = int(conn_resume)
        server_args = self.meta(member, 'server', {})
        try:
            c = self.client_factory(vthunder)
            if not member.enabled:
                status = False
            else:
                status = True
            if conn_limit is not None:
                if conn_limit < 1 or conn_limit > 8000000:
                    LOG.warning("The specified member server connection limit " +
                                "(configuration setting: conn-limit) is out of " +
                                "bounds with value {0}. Please set to between " +
                                "1-8000000. Defaulting to 8000000".format(conn_limit))
                else:
                    server_args['conn-limit'] = conn_limit
            if conn_resume is not None:
                if conn_resume < 1 or conn_resume > 1000000:
                    LOG.warning(
                        "The specified conn_resume value is invalid. The value should be either 0 or 1")
                else:
                    server_args['conn-resume'] = conn_resume
            server_args = {'server': server_args}
            try:
                conf_templates = self.readConf('SERVER', 'templates')
                server_temp = {}
                if conf_templates is not None:
                    conf_templates = conf_templates.strip('"')
                    server_temp['template-server'] = conf_templates
            except:
                server_temp = None
                LOG.warning("Invalid definition of A10 config in Pool section.")
            c.slb.server.create(member.id, member.ip_address, status=status,
                                server_templates=server_temp,
                                axapi_args=server_args)
            LOG.info("Member created successfully.")
            c.slb.service_group.member.create(pool.id, member.id, member.protocol_port)
            LOG.info("Member associated to pool successfully.")
        except Exception as e:
            LOG.error(str(e))
            LOG.info("Error occurred")


class MemberDelete(BaseVThunderTask):
    """ Task to delete member """

    def execute(self, member, vthunder, pool):
        """ Execute delete member """
        try:
            c = self.client_factory(vthunder)
            c.slb.service_group.member.delete(pool.id, member.id, member.protocol_port)
            LOG.info("Member dissociated from pool successfully.")
            c.slb.server.delete(member.id)
            LOG.info("Member deleted successfully.")
        except Exception as e:
            LOG.error(str(e))
            LOG.info("Error occurred")


class MemberUpdate(BaseVThunderTask):
    """ Task to update member """

    def execute(self, member, vthunder):
        """ Execute update member """
        conn_limit = self.readConf('SERVER', 'conn_limit')
        if conn_limit is not None:
            conn_limit = int(conn_limit)
        conn_resume = self.readConf('SERVER', 'conn_resume')
        if conn_resume is not None:
            conn_resume = int(conn_resume)
        server_args = self.meta(member, 'server', {})

        try:
            c = self.client_factory(vthunder)
            if not member.enabled:
                status = False
            else:
                status = True
            if conn_limit is not None:
                if conn_limit < 1 or conn_limit > 8000000:
                    LOG.warning("The specified member server connection limit " +
                                "(configuration setting: conn-limit) is out of " +
                                "bounds with value {0}. Please set to between " +
                                "1-8000000. Defaulting to 8000000".format(conn_limit))
                else:
                    server_args['conn-limit'] = conn_limit
            if conn_resume is not None:
                if conn_resume < 1 or conn_resume > 1000000:
                    LOG.warning(
                        "The specified conn_resume value is invalid. The value should be either 0 or 1")
                else:
                    server_args['conn-resume'] = conn_resume
            server_args = {'server': server_args}
            try:
                conf_templates = self.readConf('SERVER', 'templates')
                server_temp = {}
                if conf_templates is not None:
                    conf_templates = conf_templates.strip('"')
                    server_temp['template-server'] = conf_templates
            except:
                server_temp = None
                LOG.error("Invalid definition of A10 config in Member section.")

            c.slb.server.update(member.id, member.ip_address, status=status,
                                server_templates=server_temp,
                                axapi_args=server_args)
            LOG.info("Member updated successfully.")
        except Exception as e:
            LOG.error(str(e))
            LOG.info("Error occurred")
