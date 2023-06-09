"""added versioning for reservations

Revision ID: 1df91bc466fb
Revises: b572fa67a7f4
Create Date: 2023-05-04 14:05:51.027784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1df91bc466fb'
down_revision = 'b572fa67a7f4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservations', sa.Column('version_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reservations', 'version_id')
    # ### end Alembic commands ###
