"""empty message

Revision ID: ad9b29f10864
Revises: cb0e8226b0d1
Create Date: 2021-06-02 23:21:38.935053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad9b29f10864'
down_revision = 'cb0e8226b0d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('genres', sa.ARRAY(sa.String(length=120)), nullable=True))
    op.add_column('venue', sa.Column('website', sa.String(length=120), nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_description')
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('venue', 'website')
    op.drop_column('venue', 'genres')
    # ### end Alembic commands ###
