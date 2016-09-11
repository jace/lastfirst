"""Name tag join table

Revision ID: 9cc025a00cf
Revises: 4cd8c9f3925
Create Date: 2016-09-11 03:29:18.694057

"""

# revision identifiers, used by Alembic.
revision = '9cc025a00cf'
down_revision = '4cd8c9f3925'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('name_tag',
        sa.Column('name_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['name_id'], ['name.id'], ),
        sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
        sa.PrimaryKeyConstraint('name_id', 'tag_id')
        )
    op.create_index(op.f('ix_name_tag_tag_id'), 'name_tag', ['tag_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_name_tag_tag_id'), table_name='name_tag')
    op.drop_table('name_tag')
