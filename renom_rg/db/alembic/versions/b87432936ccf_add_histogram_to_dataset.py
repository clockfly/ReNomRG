"""add histogram to dataset

Revision ID: b87432936ccf
Revises: 83b33c9bb091
Create Date: 2019-01-16 10:47:11.834735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b87432936ccf'
down_revision = '83b33c9bb091'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dataset_def', sa.Column('true_histogram', sa.BLOB(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dataset_def', 'true_histogram')
    # ### end Alembic commands ###
