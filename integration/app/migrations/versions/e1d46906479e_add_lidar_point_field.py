"""add lidar_point field

Revision ID: e1d46906479e
Revises: 64905dcf7cbe
Create Date: 2023-07-18 10:21:27.268368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1d46906479e'
down_revision = '64905dcf7cbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('app_process', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lidar_point', sa.String(length=200), nullable=True, comment='点云地图数据'))

    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lidar_point_path', sa.Text(), nullable=False, comment='点云地图数据的存放路径'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_column('lidar_point_path')

    with op.batch_alter_table('app_process', schema=None) as batch_op:
        batch_op.drop_column('lidar_point')

    # ### end Alembic commands ###
