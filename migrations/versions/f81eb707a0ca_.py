"""empty message

Revision ID: f81eb707a0ca
Revises: None
Create Date: 2016-01-02 14:21:22.081831

"""

# revision identifiers, used by Alembic.
revision = 'f81eb707a0ca'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('document', 'documenttest')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.rename_table('documenttest', 'document')
    ### end Alembic commands ###
