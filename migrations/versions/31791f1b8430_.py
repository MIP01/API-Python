"""empty message

Revision ID: 31791f1b8430
Revises: 836745e66535
Create Date: 2023-10-30 17:42:32.629027

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '31791f1b8430'
down_revision = '836745e66535'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('barang', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nama_barang', sa.String(length=155), nullable=False))
        batch_op.drop_column('nama')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('barang', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nama', mysql.VARCHAR(length=155), nullable=False))
        batch_op.drop_column('nama_barang')

    # ### end Alembic commands ###
