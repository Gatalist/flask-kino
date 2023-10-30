"""empty message

Revision ID: 620667d2cb5f
Revises: 57efc825ad9e
Create Date: 2023-10-26 18:44:45.626230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '620667d2cb5f'
down_revision = '57efc825ad9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_countryreliase_name', table_name='country')
    op.create_index(op.f('ix_country_name'), 'country', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_country_name'), table_name='country')
    op.create_index('ix_countryreliase_name', 'country', ['name'], unique=False)
    # ### end Alembic commands ###
