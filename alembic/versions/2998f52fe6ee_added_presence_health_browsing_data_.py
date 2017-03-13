"""Added Presence Health Browsing Data table

Revision ID: 2998f52fe6ee
Revises: fc3e28ed98ea
Create Date: 2017-03-13 11:10:47.106060

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2998f52fe6ee'
down_revision = 'fc3e28ed98ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('presencebrowsingdata',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cookie_id', sa.String(length=10000), nullable=True),
    sa.Column('oncology_clicks', sa.Integer(), nullable=True),
    sa.Column('oncology_hover_time', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('presencebrowsingdata')
    # ### end Alembic commands ###
