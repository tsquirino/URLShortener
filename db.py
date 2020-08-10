# -----------------------------------------------------------------------
# Database connection module
# Starts an instance of SQLAlchemy for connecting with SQL database.
#
# (C) Tomás Quirino, August 2020
# -----------------------------------------------------------------------

from flask_sqlalchemy import SQLAlchemy

# Connection with SQL database
db = SQLAlchemy()
