"""seed db with mock data

Revision ID: 3509cc39adfb
Revises: da41cd3c82d9
Create Date: 2023-04-28 00:11:20.284861

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3509cc39adfb'
down_revision = 'da41cd3c82d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("INSERT INTO events (id, name, description, date_time) VALUES (1, 'National Awareness Day', 'You won''t have time for sleeping, soldier, not with all the bed making you''ll be doing. Guess again. No, I''m Santa Claus! Bender! Ship! Stop bickering or I''m going to come back there and change your opinions manually!', '2027-03-05 13:00:00.000000');")
    op.execute("INSERT INTO events (id, name, description, date_time) VALUES (2, 'Universal Entrepreneurship Expo', 'I suppose I could part with ''one'' and still be feared... Enough about your promiscuous mother, Hermes! We have bigger problems. Ummm...to eBay? Can I use the gun?', '2013-02-21 15:00:00.000000');")
    op.execute("INSERT INTO events (id, name, description, date_time) VALUES (3, 'Wine festival', 'All I want is to be a monkey of moderate intelligence who wears a suit... that''s why I''m transferring to business school! Meh. We''ll go deliver this crate like professionals, and then we''ll go home.', '2024-12-11 14:00:00.000000');")
    op.execute("INSERT INTO events (id, name, description, date_time) VALUES (4, 'Annual Bicycle Appreciation Day', 'Yes, if you make it look like an electrical fire. When you do things right, people won''t be sure you''ve done anything at all. Oh dear! She''s stuck in an infinite loop, and he''s an idiot! Well, that''s love for you.', '2007-03-01 13:00:00.000000');")
    op.execute("INSERT INTO events (id, name, description, date_time) VALUES (5, 'Rocket to Mars', 'I''m nobody''s taxi service; I''m not gonna be there to catch you every time you feel like jumping out of a spaceship. I''m the Doctor, I''m worse than everyone''s aunt. *catches himself* And that is not how I''m introducing myself.', '2047-10-21 09:00:00.000000');")

    op.execute("INSERT INTO tickets (id, event_id, num_available) VALUES (1, 1, 10);")
    op.execute("INSERT INTO tickets (id, event_id, num_available) VALUES (2, 2, 5);")
    op.execute("INSERT INTO tickets (id, event_id, num_available) VALUES (3, 3, 1);")
    op.execute("INSERT INTO tickets (id, event_id, num_available) VALUES (4, 4, 200);")
    op.execute("INSERT INTO tickets (id, event_id, num_available) VALUES (5, 5, 0);")


def downgrade() -> None:
    op.execute('DELETE FROM events;')
    op.execute('DELETE FROM tickets;')
