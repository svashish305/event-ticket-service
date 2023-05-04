"""Seed initial events data

Revision ID: b572fa67a7f4
Revises: a2ddbaf5296b
Create Date: 2023-05-04 10:16:18.008084

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b572fa67a7f4'
down_revision = 'a2ddbaf5296b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    events_table = sa.Table(
        'events',
        sa.MetaData(),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('date_time', sa.DateTime(), nullable=True),
        sa.Column('num_available', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    data = [
        {'name': 'National Awareness Day', 'description': 'You won''t have time for sleeping, soldier, not with all the bed making you''ll be doing. Guess again. No, I''m Santa Claus! Bender! Ship! Stop bickering or I''m going to come back there and change your opinions manually!', 'date_time': datetime(2027, 3, 5, 13, 0), 'num_available': 10},
        {'name': 'Universal Entrepreneurship Expo', 'description': 'I suppose I could part with ''one'' and still be feared... Enough about your promiscuous mother, Hermes! We have bigger problems. Ummm...to eBay? Can I use the gun?', 'date_time': datetime(2013, 2, 21, 15, 0), 'num_available': 5},
        {'name': 'Wine festival', 'description': 'All I want is to be a monkey of moderate intelligence who wears a suit... that''s why I''m transferring to business school! Meh. We''ll go deliver this crate like professionals, and then we''ll go home.', 'date_time': datetime(2024, 12, 11, 14, 0), 'num_available': 1},
        {'name': 'Annual Bicycle Appreciation Day', 'description': 'Yes, if you make it look like an electrical fire. When you do things right, people won''t be sure you''ve done anything at all. Oh dear! She''s stuck in an infinite loop, and he''s an idiot! Well, that''s love for you.', 'date_time': datetime(2007, 3, 1, 13, 0), 'num_available': 200},
        {'name': 'Rocket to Mars', 'description': 'I''m nobody''s taxi service; I''m not gonna be there to catch you every time you feel like jumping out of a spaceship. I''m the Doctor, I''m worse than everyone''s aunt. *catches himself* And that is not how I''m introducing myself.', 'date_time': datetime(2047, 10, 21, 9, 0), 'num_available': 0}
    ]

    op.bulk_insert(events_table, data)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('DELETE FROM events;')
    # ### end Alembic commands ###
