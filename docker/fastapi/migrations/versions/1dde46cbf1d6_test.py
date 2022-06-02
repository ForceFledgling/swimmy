"""Test

Revision ID: 1dde46cbf1d6
Revises: 36d6c653d97c
Create Date: 2022-06-02 16:55:36.832936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1dde46cbf1d6'
down_revision = '36d6c653d97c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups_members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'groups', ['name'])
    op.drop_column('groups', 'members_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('members_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'groups', type_='unique')
    op.drop_table('groups_members')
    # ### end Alembic commands ###
