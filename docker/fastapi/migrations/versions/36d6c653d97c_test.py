"""Test

Revision ID: 36d6c653d97c
Revises: 1067702e05d0
Create Date: 2022-06-02 16:28:38.362652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36d6c653d97c'
down_revision = '1067702e05d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('places', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('free_places', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('max_mans', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('max_womans', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('members_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('groups', 'members_id')
    op.drop_column('groups', 'max_womans')
    op.drop_column('groups', 'max_mans')
    op.drop_column('groups', 'free_places')
    op.drop_column('groups', 'places')
    # ### end Alembic commands ###
