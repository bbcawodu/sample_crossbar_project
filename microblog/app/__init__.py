from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from project_models import twistar_examples_models as models

app = Flask(__name__)

app.config.from_object('microblog.config')

db = SQLAlchemy(app)

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Post, db.session))
admin.add_view(ModelView(models.PresenceBrowsingData, db.session))

"""
If you are wondering why the import statement is at the end and not at the beginning of the script as it is always done,
the reason is to avoid circular references, because you are going to see that the views module needs to import the app
variable defined in this script. Putting the import at the end avoids the circular import error.
"""
from microblog.app import views
