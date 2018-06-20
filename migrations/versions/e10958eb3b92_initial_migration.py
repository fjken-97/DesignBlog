"""initial migration

Revision ID: e10958eb3b92
Revises: 
Create Date: 2018-06-14 20:06:51.706362

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e10958eb3b92'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('location', sa.String(length=50), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('login_time', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('blogposted',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.Column('audience_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['audience_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['blog_id'], ['blogposted.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comm')
    op.drop_table('blogposted')
    op.drop_table('user')
    # ### end Alembic commands ###
