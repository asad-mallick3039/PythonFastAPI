"""Add Foreign-Key to Posts table

Revision ID: ac1af48b99ae
Revises: e17dbdf990f4
Create Date: 2024-09-04 23:27:29.507299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac1af48b99ae'
down_revision: Union[str, None] = 'e17dbdf990f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Posts', sa.Column('user_id', sa.Integer(), nullable= False))
    op.create_foreign_key('Posts_Users_fk', source_table="Posts", referent_table="Users",
                          local_cols=['user_id'], remote_cols=['id'], ondelete= "CASCADE")
    pass


def downgrade():
    op.drop_constraint('Posts_Users_fk', table_name="Posts")
    op.drop_column('Posts', 'user_id')
    pass
