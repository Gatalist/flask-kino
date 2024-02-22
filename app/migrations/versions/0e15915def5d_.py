"""empty message

Revision ID: 0e15915def5d
Revises: 2fcffeb56007
Create Date: 2023-12-24 19:24:36.965656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e15915def5d'
down_revision = '2fcffeb56007'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agelimit', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.Integer(), nullable=True))
        batch_op.drop_index('ix_agelimit_name_old')
        batch_op.drop_column('name_old')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agelimit', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name_old', sa.VARCHAR(length=64), autoincrement=False, nullable=True))
        batch_op.create_index('ix_agelimit_name_old', ['name_old'], unique=False)
        batch_op.drop_column('name')

    # ### end Alembic commands ###
