"""empty message

Revision ID: e492d5127db6
Revises: d1d43ba766b3
Create Date: 2023-12-24 19:14:52.997180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e492d5127db6'
down_revision = 'd1d43ba766b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agelimit', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('agelimit', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)

    # ### end Alembic commands ###