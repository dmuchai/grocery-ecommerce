"""Added address field to Order model

Revision ID: 1b103ac2a525
Revises: 3299ba5e98a6
Create Date: 2025-03-21 16:02:40.648297

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1b103ac2a525'
down_revision = '3299ba5e98a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=256), nullable=False))
        batch_op.drop_column('shipping_address')

    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'category', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shipping_address', mysql.VARCHAR(length=256), nullable=False))
        batch_op.drop_column('address')

    # ### end Alembic commands ###
