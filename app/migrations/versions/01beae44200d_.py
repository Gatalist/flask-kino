"""empty message

Revision ID: 01beae44200d
Revises: 1ba4a9d6a29b
Create Date: 2023-12-02 20:17:44.566448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01beae44200d'
down_revision = '1ba4a9d6a29b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('segment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('segment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_segment_name'), ['name'], unique=False)

    op.create_table('segment_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('segment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['segment_id'], ['segment.id'], )
    )
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('segment_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'segment', ['segment_id'], ['id'], ondelete='SET NULL')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('segment_id')

    op.drop_table('segment_movie')
    with op.batch_alter_table('segment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_segment_name'))

    op.drop_table('segment')
    # ### end Alembic commands ###
