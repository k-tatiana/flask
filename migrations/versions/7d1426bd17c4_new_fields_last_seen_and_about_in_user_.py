"""new fields, last_seen and about in User model(table)

Revision ID: 7d1426bd17c4
Revises: 8df2c2a261d5
Create Date: 2018-04-30 21:22:38.222217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d1426bd17c4'
down_revision = '8df2c2a261d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about')
    # ### end Alembic commands ###
