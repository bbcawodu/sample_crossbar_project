#!/usr/bin/env python
from migrate.versioning.shell import main
import os

if __name__ == '__main__':
    main(url=os.environ["DATABASE_URL"], debug='False', repository='twisted_database_component')
