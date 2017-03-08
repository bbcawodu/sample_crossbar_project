"""create users table

Revision ID: c47843e9e5df
Revises: d7d04a5f3d9d
Create Date: 2017-03-08 15:25:44.398648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c47843e9e5df'
down_revision = 'd7d04a5f3d9d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('age', sa.Integer),
        sa.Column('first_name', sa.String(1000)),
        sa.Column('last_name', sa.String(1000)),
    )


def downgrade():
    op.drop_table('users')
