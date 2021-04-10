"""empty message

Revision ID: 67ed10db58d4
Revises: aacf5d9143b3
Create Date: 2021-03-18 14:38:50.649668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67ed10db58d4'
down_revision = 'aacf5d9143b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity', sa.Column('hourdsda', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activity', 'hourdsda')
    # ### end Alembic commands ###