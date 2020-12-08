"""a10-device-instance to vthunders

Revision ID: 4fa8c3867dcb
Revises: 05b1446c7f20
Create Date: 2020-12-03 10:12:07.785078

"""
from alembic import op
import sqlalchemy as sa
from oslo_utils import uuidutils
from sqlalchemy.orm import sessionmaker
from oslo_config import cfg

from a10_octavia import a10_config
from a10_octavia.db.models import VThunder

CONF = cfg.CONF

# revision identifiers, used by Alembic.
revision = '4fa8c3867dcb'
down_revision = 'a6e9b9b69494'
branch_labels = None
depends_on = None

try:
    bind = op.get_bind()
except NameError:
    pass
else:
    session = sessionmaker(bind=bind)
    sess = session()


def upgrade():
    a10_cfg = a10_config.A10Config()
    db_str = a10_cfg.get('neutron_database_connection')
    db_engine = sa.create_engine(db_str)
    with db_engine.connect() as con:
        results = con.execute('select * from a10_device_instances')
        vthunders = []
        for _row in results:
            nova_instance_id = _row[17]
            if nova_instance_id is not None:
                undercloud = False
            vthunders.append(VThunder(vthunder_id=_row[0],
                                      device_name=_row[4],
                                      ip_address=_row[18],
                                      username=_row[5],
                                      password=_row[6],
                                      axapi_version=_row[7],
                                      project_id=_row[3],
                                      created_at=_row[1],
                                      updated_at=_row[2],
                                      partition_name=_row[12],
                                      write_memory=_row[16],
                                      protocol=_row[8],
                                      port=_row[9],
                                      undercloud=undercloud))
    sess.add_all(vthunders)
    sess.commit()
    sess.close()


def downgrade():
    sess.query(VThunder).filter().delete()
    sess.commit()
    sess.close()
