"""not unique for journal title

Revision ID: 7fb898164a21
Revises: a67c7679a519
Create Date: 2023-07-24 15:01:18.290068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fb898164a21'
down_revision = 'a67c7679a519'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_journal_title', table_name='journal')
    op.create_index(op.f('ix_journal_title'), 'journal', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_journal_title'), table_name='journal')
    op.create_index('ix_journal_title', 'journal', ['title'], unique=False)
    # ### end Alembic commands ###
