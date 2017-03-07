from sqlalchemy import Table, Column, Integer, String, MetaData

meta = MetaData()

users_table = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('age', Integer),
    Column('first_name', String(1000)),
    Column('last_name', String(1000)),
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    users_table.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    users_table.drop()