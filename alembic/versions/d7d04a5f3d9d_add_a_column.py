"""Add a column

Revision ID: d7d04a5f3d9d
Revises: 92dc01e60ec3
Create Date: 2017-03-08 15:15:53.673322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7d04a5f3d9d'
down_revision = '92dc01e60ec3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    op.drop_column('account', 'last_transaction_date')
