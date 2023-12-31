"""empty message

Revision ID: 0121a5599dfb
Revises: 3d55a7327a1c
Create Date: 2023-11-01 12:44:11.981647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0121a5599dfb'
down_revision = '3d55a7327a1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('penjual', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('penjual', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
