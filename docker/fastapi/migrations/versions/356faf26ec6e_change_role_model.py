"""Change role model

Revision ID: 356faf26ec6e
Revises: ac7900a5f7df
Create Date: 2022-05-31 18:24:16.853217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '356faf26ec6e'
down_revision = 'ac7900a5f7df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role_name', sa.String(), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role_name'], ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role_name')
    # ### end Alembic commands ###
