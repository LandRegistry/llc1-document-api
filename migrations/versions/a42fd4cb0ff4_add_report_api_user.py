"""Add report-api user

Revision ID: a42fd4cb0ff4
Revises: 0b678503449a
Create Date: 2018-07-04 13:30:33.489188

"""

# revision identifiers, used by Alembic.
revision = 'a42fd4cb0ff4'
down_revision = '0b678503449a'
branch_labels = None
depends_on = None

from alembic import op
from flask import current_app


def upgrade():
    query = "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '{0}') THEN CREATE ROLE {0} " \
            "WITH LOGIN PASSWORD '{1}'; END IF; END $$;".format(current_app.config.get("REPORT_API_SQL_USERNAME"),
                                                                current_app.config.get("REPORT_API_SQL_PASSWORD"))
    op.execute(query)
    op.execute("GRANT SELECT ON document_reference TO {};"
               .format(current_app.config.get("REPORT_API_SQL_USERNAME")))


def downgrade():
    op.execute("REVOKE SELECT ON document_reference FROM {};"
               .format(current_app.config.get("REPORT_API_SQL_USERNAME")))
    query = "DO $$ BEGIN IF EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '{0}') THEN DROP ROLE {0};" \
            " END IF; END $$;".format(current_app.config.get("REPORT_API_SQL_USERNAME"))
    op.execute(query)