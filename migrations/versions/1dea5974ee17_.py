"""empty message

Revision ID: 1dea5974ee17
Revises: 762402052503
Create Date: 2021-03-02 18:07:51.715739

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1dea5974ee17'
down_revision = '762402052503'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chart_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_chart', sa.String(length=30), nullable=False),
    sa.Column('height', sa.String(length=20), nullable=False),
    sa.Column('mass', sa.String(length=10), nullable=False),
    sa.Column('hair_color', sa.String(length=10), nullable=False),
    sa.Column('skin_color', sa.String(length=10), nullable=False),
    sa.Column('eye_color', sa.String(length=10), nullable=False),
    sa.Column('birth_year', sa.String(length=10), nullable=False),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_planet', sa.String(length=30), nullable=False),
    sa.Column('diameter', sa.String(length=30), nullable=False),
    sa.Column('rotation_period', sa.Integer(), nullable=False),
    sa.Column('orbital_period', sa.String(length=20), nullable=False),
    sa.Column('gravity', sa.String(length=20), nullable=False),
    sa.Column('gravity_type', sa.String(length=20), nullable=False),
    sa.Column('population', sa.String(length=20), nullable=False),
    sa.Column('climate', sa.String(length=20), nullable=False),
    sa.Column('terrain', sa.String(length=20), nullable=False),
    sa.Column('surface_water', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('starships_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_starship', sa.String(length=30), nullable=False),
    sa.Column('model', sa.String(length=30), nullable=False),
    sa.Column('starship_class', sa.String(length=25), nullable=False),
    sa.Column('manufacturer', sa.String(length=40), nullable=False),
    sa.Column('cost_in_credits', sa.String(length=20), nullable=False),
    sa.Column('length', sa.String(length=20), nullable=False),
    sa.Column('crew', sa.String(length=20), nullable=False),
    sa.Column('passengers', sa.String(length=30), nullable=False),
    sa.Column('max_atmosphering_speed', sa.String(length=20), nullable=False),
    sa.Column('hyperdrive_rating', sa.String(length=20), nullable=False),
    sa.Column('MGLT', sa.String(length=20), nullable=False),
    sa.Column('cargo_capacity', sa.String(length=30), nullable=False),
    sa.Column('consumables', sa.String(length=15), nullable=False),
    sa.Column('pilots', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('model')
    )
    op.create_table('username_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('bio', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('favlist_chart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_chart', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comments', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['id_chart'], ['chart_data.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['username_data.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favlist_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_planets', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comments', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['id_planets'], ['planets_data.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['username_data.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favlist_starships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_starship', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comments', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['id_starship'], ['starships_data.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['username_data.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index('email', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', mysql.VARCHAR(length=120), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.CheckConstraint('(`is_active` in (0,1))', name='user_chk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('email', 'user', ['email'], unique=True)
    op.drop_table('favlist_starships')
    op.drop_table('favlist_planets')
    op.drop_table('favlist_chart')
    op.drop_table('username_data')
    op.drop_table('starships_data')
    op.drop_table('planets_data')
    op.drop_table('chart_data')
    # ### end Alembic commands ###
