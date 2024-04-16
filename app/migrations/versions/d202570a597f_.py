"""empty message

Revision ID: d202570a597f
Revises: 2c091e683b75
Create Date: 2024-04-12 20:45:18.172999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd202570a597f'
down_revision = '2c091e683b75'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('age_limits',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('countries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('countries', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_countries_name'), ['name'], unique=True)

    op.create_table('creators',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('image_url', sa.String(length=256), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('creators', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_creators_image_url'), ['image_url'], unique=False)
        batch_op.create_index(batch_op.f('ix_creators_name'), ['name'], unique=True)

    op.create_table('directors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('image_url', sa.String(length=256), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('directors', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_directors_image_url'), ['image_url'], unique=False)
        batch_op.create_index(batch_op.f('ix_directors_name'), ['name'], unique=True)

    op.create_table('film_length',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('length', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genres',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('genres', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_genres_name'), ['name'], unique=True)

    op.create_table('rating_critics',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('star', sa.Float(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating_imdb',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('star', sa.Float(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rating_kinopoisk',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('star', sa.Float(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('releases',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('screenshots',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('kinopoisk_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('url', sa.String(length=256), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('screenshots', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_screenshots_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_screenshots_url'), ['url'], unique=False)

    op.create_table('segments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('activate', sa.DateTime(), nullable=True),
    sa.Column('deactivate', sa.DateTime(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('segments', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_segments_name'), ['name'], unique=False)

    op.create_table('similars',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('kinopoisk_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('similars', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_similars_name'), ['name'], unique=False)

    op.create_table('tags',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tags_name'), ['name'], unique=False)

    op.create_table('type_videos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('type_videos', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_type_videos_name'), ['name'], unique=True)

    op.create_table('actors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('image_url', sa.String(length=256), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_actors_image_url'), ['image_url'], unique=False)
        batch_op.create_index(batch_op.f('ix_actors_name'), ['name'], unique=True)

    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('roles_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['roles_id'], ['roles.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)

    op.create_table('movies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('kinopoisk_id', sa.Integer(), nullable=True),
    sa.Column('imdb_id', sa.String(length=12), nullable=True),
    sa.Column('name_ru', sa.String(length=256), nullable=True),
    sa.Column('name_original', sa.String(length=256), nullable=True),
    sa.Column('poster_url', sa.String(length=256), nullable=True),
    sa.Column('slug', sa.String(length=256), nullable=True),
    sa.Column('rating_kinopoisk_id', sa.Integer(), nullable=True),
    sa.Column('rating_imdb_id', sa.Integer(), nullable=True),
    sa.Column('rating_critics_id', sa.Integer(), nullable=True),
    sa.Column('year_id', sa.Integer(), nullable=True),
    sa.Column('film_length_id', sa.Integer(), nullable=True),
    sa.Column('slogan', sa.String(length=512), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('short_description', sa.Text(), nullable=True),
    sa.Column('type_video_id', sa.Integer(), nullable=True),
    sa.Column('age_limits_id', sa.Integer(), nullable=True),
    sa.Column('last_syncs', sa.DateTime(), nullable=True),
    sa.Column('segment_id', sa.Integer(), nullable=True),
    sa.Column('countries_id', sa.Integer(), nullable=True),
    sa.Column('genres_id', sa.Integer(), nullable=True),
    sa.Column('director_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('screen_img_id', sa.Integer(), nullable=True),
    sa.Column('similar_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['age_limits_id'], ['age_limits.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['countries_id'], ['countries.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['creator_id'], ['creators.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['director_id'], ['directors.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['film_length_id'], ['film_length.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['genres_id'], ['genres.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['rating_critics_id'], ['rating_critics.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['rating_imdb_id'], ['rating_imdb.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['rating_kinopoisk_id'], ['rating_kinopoisk.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['screen_img_id'], ['screenshots.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['segment_id'], ['segments.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['similar_id'], ['similars.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['type_video_id'], ['type_videos.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['year_id'], ['releases.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('tag_actor',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], )
    )
    op.create_table('actor_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actors.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], )
    )
    op.create_table('country_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], )
    )
    op.create_table('creator_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['creators.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], )
    )
    op.create_table('director_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('director_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['director_id'], ['directors.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], )
    )
    op.create_table('genre_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], )
    )
    op.create_table('screenshot_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('screenshot_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.ForeignKeyConstraint(['screenshot_id'], ['screenshots.id'], )
    )
    op.create_table('segment_movie',
    sa.Column('movies_id', sa.Integer(), nullable=True),
    sa.Column('segments_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movies_id'], ['movies.id'], ),
    sa.ForeignKeyConstraint(['segments_id'], ['segments.id'], )
    )
    op.create_table('similar_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('similar_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.ForeignKeyConstraint(['similar_id'], ['similars.id'], )
    )
    op.create_table('user_movie',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_movie')
    op.drop_table('similar_movie')
    op.drop_table('segment_movie')
    op.drop_table('screenshot_movie')
    op.drop_table('genre_movie')
    op.drop_table('director_movie')
    op.drop_table('creator_movie')
    op.drop_table('country_movie')
    op.drop_table('actor_movie')
    op.drop_table('tag_actor')
    op.drop_table('roles_users')
    op.drop_table('movies')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    with op.batch_alter_table('actors', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_actors_name'))
        batch_op.drop_index(batch_op.f('ix_actors_image_url'))

    op.drop_table('actors')
    with op.batch_alter_table('type_videos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_type_videos_name'))

    op.drop_table('type_videos')
    with op.batch_alter_table('tags', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tags_name'))

    op.drop_table('tags')
    with op.batch_alter_table('similars', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_similars_name'))

    op.drop_table('similars')
    with op.batch_alter_table('segments', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_segments_name'))

    op.drop_table('segments')
    with op.batch_alter_table('screenshots', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_screenshots_url'))
        batch_op.drop_index(batch_op.f('ix_screenshots_name'))

    op.drop_table('screenshots')
    op.drop_table('roles')
    op.drop_table('releases')
    op.drop_table('rating_kinopoisk')
    op.drop_table('rating_imdb')
    op.drop_table('rating_critics')
    with op.batch_alter_table('genres', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_genres_name'))

    op.drop_table('genres')
    op.drop_table('film_length')
    with op.batch_alter_table('directors', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_directors_name'))
        batch_op.drop_index(batch_op.f('ix_directors_image_url'))

    op.drop_table('directors')
    with op.batch_alter_table('creators', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_creators_name'))
        batch_op.drop_index(batch_op.f('ix_creators_image_url'))

    op.drop_table('creators')
    with op.batch_alter_table('countries', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_countries_name'))

    op.drop_table('countries')
    op.drop_table('age_limits')
    # ### end Alembic commands ###
