## Setting up Alembic Migration Environment
## Excerpts taken from: http://alembic.zzzcomputing.com/en/latest/tutorial.html

### Alembic Migration Environment creation and configuration.

- Change to the root directory of the crossbar project and use the following command:
    ``` alembic init --template generic <directory name>```
    - This will create a directory with the files for a generic single-database configuration migration environment
    - The directory structure will look like:
    
        ```
        yourproject/
            alembic_directory/
                env.py
                README
                script.py.mako
                versions/
                    3512b954651e_add_account.py
                    2b1ae634e5cd_add_order_id.py
                    3adcc9a56557_rename_username_field.py
                
        
        yourproject - this is the root of your application’s source code, or some directory within it.
        
        alembic - this directory lives within your application’s source tree and is the home of the migration environment. It can be named anything, and a project that uses multiple databases may even have more than one.
        
        env.py - This is a Python script that is run whenever the alembic migration tool is invoked. At the very least, it contains instructions to configure and generate a SQLAlchemy engine, procure a connection from that engine along with a transaction, and then invoke the migration engine, using the connection as a source of database connectivity.
        
        The env.py script is part of the generated environment so that the way migrations run is entirely customizable. The exact specifics of how to connect are here, as well as the specifics of how the migration environment are invoked. The script can be modified so that multiple engines can be operated upon, custom arguments can be passed into the migration environment, application-specific libraries and models can be loaded in and made available.
        
        Alembic includes a set of initialization templates which feature different varieties of env.py for different use cases.
        
        README - included with the various environment templates, should have something informative.
        
        script.py.mako - This is a Mako template file which is used to generate new migration scripts. Whatever is here is used to generate new files within versions/. This is scriptable so that the structure of each migration file can be controlled, including standard imports to be within each, as well as changes to the structure of the upgrade() and downgrade() functions. For example, the multidb environment allows for multiple functions to be generated using a naming scheme upgrade_engine1(), upgrade_engine2().
        
        versions/ - This directory holds the individual version scripts. Users of other migration tools may notice that the files here don’t use ascending integers, and instead use a partial GUID approach. In Alembic, the ordering of version scripts is relative to directives within the scripts themselves, and it is theoretically possible to “splice” version files in between others, allowing migration sequences from different branches to be merged, albeit carefully by hand.
        ```
        
    - In order for Alembic to access the postgres db locally, or in deployment, it env.py file needs to be configured to
      access it. Heroku uses DATABASE_URL to access the db in production so we will be using the same locallty. If you
      followed the [Database Programming with Python/Twisted/WAMP(Autobahn/Crossbar) README](docs/database_programming_overview.md),
      then this should already be set when the virtual environment is started. Now, all that's needed is to set alembic's
      env.py file to be able to access it.
        - Add the following import at the top of the file
            - ``` from os import environ```
        - Add the following directly after the import statements:
            - ``` 
              config = context.config
              config.set_main_option('sqlalchemy.url', environ["DATABASE_URL"])
              ```
              
### Manual migration creation with Alembic.

- To create a new migration with changes to the db schema, use the following command:
    - ```alembic revision -m "<migration name>"```
    - This will create a file under alembic_directory/versions, open it:
    - The new file, <letter and number code>_<migration name>.py, will look like the following:
        ```

        """create users table
        
        Revision ID: 1975ea83b712
        Revises:
        Create Date: 2011-11-08 11:40:27.089406
        
        """
        
        # revision identifiers, used by Alembic.
        revision = '1975ea83b712'
        down_revision = None
        branch_labels = None
        
        from alembic import op
        import sqlalchemy as sa
        
        def upgrade():
            pass
        
        def downgrade():
            pass
        ```
        
- To add db operations for upgrading and downgrading the db, use the directives operations modules defined by Alembic
    - Alembic migration directives documentation: http://alembic.zzzcomputing.com/en/latest/ops.html#ops
    - The following is an example migration using Alembic migration directives:
        ```
        from alembic import op
        import sqlalchemy as sa
        
        
        # revision identifiers, used by Alembic.
        revision = 'fc3e28ed98ea'
        down_revision = None
        branch_labels = None
        depends_on = None
        
        
        def upgrade():
            # ### commands auto generated by Alembic - please adjust! ###
            op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('age', sa.Integer(), nullable=True),
            sa.Column('first_name', sa.String(length=1000), nullable=True),
            sa.Column('last_name', sa.String(length=1000), nullable=True),
            sa.PrimaryKeyConstraint('id')
            )
            # ### end Alembic commands ###
        
        
        def downgrade():
            # ### commands auto generated by Alembic - please adjust! ###
            op.drop_table('users')
            # ### end Alembic commands ###
        ```
        
- After you have created your migrations file, you can use the following command to Upgrade the db to the most recent
  migration:
    - ```alembic upgrade head```
    - You can also use the following command to downgrade the db: ```alembic downgrade <version('base' to go to nothing)>```