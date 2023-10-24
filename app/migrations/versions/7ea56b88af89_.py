"""empty message

Revision ID: 7ea56b88af89
Revises: 
Create Date: 2023-10-07 14:20:45.976186

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ea56b88af89'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_actor_name'), 'actor', ['name'], unique=True)
    op.create_table('agelimit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agelimit_name'), 'agelimit', ['name'], unique=True)
    op.create_table('countryreliase',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_countryreliase_name'), 'countryreliase', ['name'], unique=True)
    op.create_table('creator',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_creator_name'), 'creator', ['name'], unique=True)
    op.create_table('director',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_director_name'), 'director', ['name'], unique=True)
    op.create_table('filmlength',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genre',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_genre_name'), 'genre', ['name'], unique=True)
    op.create_table('ratingfilmcritics',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('star', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ratingimdb',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('star', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ratingkinopoisk',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('star', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reliase',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('screenshot',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('url', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_screenshot_name'), 'screenshot', ['name'], unique=False)
    op.create_index(op.f('ix_screenshot_url'), 'screenshot', ['url'], unique=True)
    op.create_table('similars',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('kinopoisk_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_similars_name'), 'similars', ['name'], unique=False)
    op.create_table('typevideo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_typevideo_name'), 'typevideo', ['name'], unique=True)
    op.create_table('movie',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('kinopoisk_id', sa.Integer(), nullable=True),
    sa.Column('imdb_id', sa.String(length=12), nullable=True),
    sa.Column('name_ru', sa.String(length=64), nullable=True),
    sa.Column('name_original', sa.String(length=64), nullable=True),
    sa.Column('poster_url', sa.String(length=128), nullable=True),
    sa.Column('slug', sa.String(length=128), nullable=True),
    sa.Column('rating_kinopoisk_id', sa.Integer(), nullable=True),
    sa.Column('rating_imdb_id', sa.Integer(), nullable=True),
    sa.Column('rating_critics_id', sa.Integer(), nullable=True),
    sa.Column('year_id', sa.Integer(), nullable=True),
    sa.Column('film_length_id', sa.Integer(), nullable=True),
    sa.Column('slogan', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('short_description', sa.Text(), nullable=True),
    sa.Column('type_video_id', sa.Integer(), nullable=True),
    sa.Column('age_limits_id', sa.Integer(), nullable=True),
    sa.Column('last_syncs', sa.DateTime(), nullable=True),
    sa.Column('countries_id', sa.Integer(), nullable=True),
    sa.Column('genres_id', sa.Integer(), nullable=True),
    sa.Column('director_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('screen_img_id', sa.Integer(), nullable=True),
    sa.Column('similar_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actor.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['age_limits_id'], ['agelimit.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['countries_id'], ['countryreliase.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['creator_id'], ['creator.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['director_id'], ['director.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['film_length_id'], ['filmlength.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['genres_id'], ['genre.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['rating_critics_id'], ['ratingfilmcritics.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['rating_imdb_id'], ['ratingimdb.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['rating_kinopoisk_id'], ['ratingkinopoisk.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['screen_img_id'], ['screenshot.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['similar_id'], ['similars.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['type_video_id'], ['typevideo.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['year_id'], ['reliase.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('actor_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actor.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], )
    )
    op.create_table('country_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countryreliase.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], )
    )
    op.create_table('creator_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['creator.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], )
    )
    op.create_table('director_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('director_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['director_id'], ['director.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], )
    )
    op.create_table('genre_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], )
    )
    op.create_table('screenshot_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('screenshot_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['screenshot_id'], ['screenshot.id'], )
    )
    op.create_table('similars_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('similars_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['similars_id'], ['similars.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('similars_movie')
    op.drop_table('screenshot_movie')
    op.drop_table('genre_movie')
    op.drop_table('director_movie')
    op.drop_table('creator_movie')
    op.drop_table('country_movie')
    op.drop_table('actor_movie')
    op.drop_table('movie')
    op.drop_index(op.f('ix_typevideo_name'), table_name='typevideo')
    op.drop_table('typevideo')
    op.drop_index(op.f('ix_similars_name'), table_name='similars')
    op.drop_table('similars')
    op.drop_index(op.f('ix_screenshot_url'), table_name='screenshot')
    op.drop_index(op.f('ix_screenshot_name'), table_name='screenshot')
    op.drop_table('screenshot')
    op.drop_table('reliase')
    op.drop_table('ratingkinopoisk')
    op.drop_table('ratingimdb')
    op.drop_table('ratingfilmcritics')
    op.drop_index(op.f('ix_genre_name'), table_name='genre')
    op.drop_table('genre')
    op.drop_table('filmlength')
    op.drop_index(op.f('ix_director_name'), table_name='director')
    op.drop_table('director')
    op.drop_index(op.f('ix_creator_name'), table_name='creator')
    op.drop_table('creator')
    op.drop_index(op.f('ix_countryreliase_name'), table_name='countryreliase')
    op.drop_table('countryreliase')
    op.drop_index(op.f('ix_agelimit_name'), table_name='agelimit')
    op.drop_table('agelimit')
    op.drop_index(op.f('ix_actor_name'), table_name='actor')
    op.drop_table('actor')
    # ### end Alembic commands ###
