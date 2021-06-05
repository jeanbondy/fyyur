"""empty message

Revision ID: cb0e8226b0d1
Revises: 741aefc436fd
Create Date: 2021-06-02 20:16:40.136366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb0e8226b0d1'
down_revision = '741aefc436fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('artist', sa.Column('website', sa.String(length=120), nullable=True))
    op.alter_column('artist', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('artist', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('artist', 'website')
    op.drop_column('artist', 'seeking_venue')
    # ### end Alembic commands ###