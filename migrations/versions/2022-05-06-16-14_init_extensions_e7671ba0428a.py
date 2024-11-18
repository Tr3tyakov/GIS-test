"""init_extensions

Revision ID: e7671ba0428a
Revises: 
Create Date: 2022-05-06 16:14:56.133710+03:00

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "e7671ba0428a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "postgis"')


def downgrade():
    op.execute('DROP EXTENSION IF EXISTS "postgis"')
