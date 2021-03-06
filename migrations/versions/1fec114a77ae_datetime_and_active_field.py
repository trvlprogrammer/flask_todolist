"""datetime and active field

Revision ID: 1fec114a77ae
Revises: d57f203531cb
Create Date: 2022-06-29 13:13:54.395019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fec114a77ae'
down_revision = 'd57f203531cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('date_todo', sa.DateTime(), nullable=True))
    op.add_column('post', sa.Column('active', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_post_date_todo'), 'post', ['date_todo'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_date_todo'), table_name='post')
    op.drop_column('post', 'active')
    op.drop_column('post', 'date_todo')
    # ### end Alembic commands ###
