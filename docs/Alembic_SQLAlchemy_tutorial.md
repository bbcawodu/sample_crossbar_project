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
    - SQLAlchemy Column and Data type documentation: http://docs.sqlalchemy.org/en/latest/core/type_basics.html
    - SQLAlchemy Database schema migrations changeset: https://sqlalchemy-migrate.readthedocs.io/en/latest/changeset.html#changeset-system
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
    
### Auto Generating Migrations with Alembic.
### Excerpts taken from: http://alembic.zzzcomputing.com/en/latest/autogenerate.html, http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

- In order to autogenerate migrations with Alembic, you first must define a db schema that Alembic will generate the
  migrations from. To define our db schema, we will be using the SQLAlchemy ORM library to define our tables.
    - SQLAlchemy Object Relational Tutorial: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
    - SQLAlchemy ORM Declarative documentation(ORM Language for declaring schema): http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/index.html
    
- ```
    When using the ORM, the configurational process starts by describing the database tables we’ll be dealing with, and
    then by defining our own classes which will be mapped to those tables. In modern SQLAlchemy, these two tasks are
    usually performed together, using a system known as Declarative, which allows us to create classes that include
    directives to describe the actual database table they will be mapped to.

    Classes mapped using the Declarative system are defined in terms of a base class which maintains a catalog of
    classes and tables relative to that base - this is known as the declarative base class. Our application will
    usually have just one instance of this base in a commonly imported module. We create the base class using the
    declarative_base() function, as follows:
    
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()
    
    Now that we have a “base”, we can define any number of mapped classes in terms of it
  ```
  
  - All defined classes must inherit from this defined base in order to be detected using Alembic autogenerate.
  - Here is an Example:
    ```
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy import Sequence
        from sqlalchemy import Column
        from sqlalchemy import Integer
        from sqlalchemy import String
        from sqlalchemy import Float
        
        Base = declarative_base()
        
        
        class User(Base):
            __tablename__ = 'users'
        
            id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
            age = Column(Integer)
            first_name = Column(String(1000))
            last_name = Column(String(1000))
        
            def __repr__(self):
                return "<User(first_name='%s', last_name='%s')>" % (
                                        self.first_name, self.last_name)
    ```
  
    - Here the declarative base is defined which all Classes/Tables should inherit from
    - A Class User is defined, and the attribute __tablename__ is set to 'users'. this tells the declarative base which
      table this class corresponds to.
    - ```
        A class using Declarative at a minimum needs a __tablename__ attribute, and at least one Column which is part
        of a primary key [1]. SQLAlchemy never makes any assumptions by itself about the table to which a class refers,
        including that it has no built-in conventions for names, datatypes, or constraints. But this doesn’t mean
        boilerplate is required; instead, you’re encouraged to create your own automated conventions using helper
        functions and mixin classes, which is described in detail at Mixin and Custom Base Classes.

        When our class is constructed, Declarative replaces all the Column objects with special Python accessors known
        as descriptors; this is a process known as instrumentation. The “instrumented” mapped class will provide us
        with the means to refer to our table in a SQL context as well as to persist and load the values of columns
        from the database.
      ```
      
- After you have defined your db schema using SQLAlchemy models, you are ready to load them using Alembic.
  To do this, you must import the declarative base used in your project's SQLAlchemy models package. This is done in 
  your project's Alembic migration environment's env.py. An example is below:
  ```
    # add your model's MetaData object here
    # for 'autogenerate' support
    # target_metadata = None
    from project_models import Base
    target_metadata = Base.metadata
  ```
  
  - Change the variable target_metadata to the metadata attribute of the imported declarative base class.
  - In order for Alembic to access your project's SQLAlchemy models package while running the virtual environment on
    your local machine, your project folder must be added to the PYTHONPATH. To do this, add the following line to the
    end of your virtual environment's activate script.
    ```export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH:}/<project folder absolute path>"```
  
- You are now ready to use Alembic's auto generate feature. To do so run the following command:
    ```alembic revision --autogenerate -m "<migration name>"```
    - This will create a new migration in the versions folder which reflects the detected changes from the db's state to the
      models defined in the declarative base.
    - To apply the migration, use the alembic migrate command.
    
- Although Alembic's autogenerate is convenient, it doesn't detect everything, here is a list of what it does and doenst detect:
    - ```
        The vast majority of user issues with Alembic centers on the topic of what kinds of changes autogenerate can
        and cannot detect reliably, as well as how it renders Python code for what it does detect. it is critical to
        note that autogenerate is not intended to be perfect. It is always necessary to manually review and correct the
        candidate migrations that autogenererate produces. The feature is getting more and more comprehensive and
        error-free as releases continue, but one should take note of the current limitations.

        Autogenerate will detect:
        
        Table additions, removals.
        Column additions, removals.
        Change of nullable status on columns.
        Basic changes in indexes and explcitly-named unique constraints
        New in version 0.6.1: Support for autogenerate of indexes and unique constraints.
        
        Basic changes in foreign key constraints
        New in version 0.7.1: Support for autogenerate of foreign key constraints.
        
        Autogenerate can optionally detect:
        
        Change of column type. This will occur if you set the EnvironmentContext.configure.compare_type parameter to True, or to a custom callable function. The feature works well in most cases, but is off by default so that it can be tested on the target schema first. It can also be customized by passing a callable here; see the section Comparing Types for details.
        Change of server default. This will occur if you set the EnvironmentContext.configure.compare_server_default parameter to True, or to a custom callable function. This feature works well for simple cases but cannot always produce accurate results. The Postgresql backend will actually invoke the “detected” and “metadata” values against the database to determine equivalence. The feature is off by default so that it can be tested on the target schema first. Like type comparison, it can also be customized by passing a callable; see the function’s documentation for details.
        Autogenerate can not detect:
        
        Changes of table name. These will come out as an add/drop of two different tables, and should be hand-edited into a name change instead.
        Changes of column name. Like table name changes, these are detected as a column add/drop pair, which is not at all the same as a name change.
        Anonymously named constraints. Give your constraints a name, e.g. UniqueConstraint('col1', 'col2', name="my_name"). See the section The Importance of Naming Constraints for background on how to configure automatic naming schemes for constraints.
        Special SQLAlchemy types such as Enum when generated on a backend which doesn’t support ENUM directly - this because the representation of such a type in the non-supporting database, i.e. a CHAR+ CHECK constraint, could be any kind of CHAR+CHECK. For SQLAlchemy to determine that this is actually an ENUM would only be a guess, something that’s generally a bad idea. To implement your own “guessing” function here, use the sqlalchemy.events.DDLEvents.column_reflect() event to detect when a CHAR (or whatever the target type is) is reflected, and change it to an ENUM (or whatever type is desired) if it is known that that’s the intent of the type. The sqlalchemy.events.DDLEvents.after_parent_attach() can be used within the autogenerate process to intercept and un-attach unwanted CHECK constraints.
        Autogenerate can’t currently, but will eventually detect:
        
        Some free-standing constraint additions and removals may not be supported, including PRIMARY KEY, EXCLUDE, CHECK; these are not necessarily implemented within the autogenerate detection system and also may not be supported by the supporting SQLAlchemy dialect.
        Sequence additions, removals - not yet implemented.
      ```
      
    - Here is an article outlining how to do a table name change in postgres when autogenerate does not detect it properly:
        http://petegraham.co.uk/rename-postgres-table-with-alembic/