"""Move model column from site into hub

Revision ID: 6a747dfa6d1b
Revises: 85cf6decacbb
Create Date: 2025-06-19 11:13:09.512131

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '6a747dfa6d1b'
down_revision = '85cf6decacbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hub', sa.Column('model', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False))
    op.drop_column('site', 'model')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('site', sa.Column('model', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_column('hub', 'model')
    # ### end Alembic commands ###
