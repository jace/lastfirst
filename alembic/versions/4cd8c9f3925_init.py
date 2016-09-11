"""Init

Revision ID: 4cd8c9f3925
Revises: None
Create Date: 2016-09-11 01:40:44.585211

"""

# revision identifiers, used by Alembic.
revision = '4cd8c9f3925'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('name',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('title', sa.Unicode(length=250), nullable=False),
        sa.Column('gender', sa.SmallInteger(), nullable=True),
        sa.Column('description', sa.UnicodeText(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
    op.create_index(op.f('ix_name_gender'), 'name', ['gender'], unique=False)
    op.create_index(op.f('ix_name_title'), 'name', ['title'], unique=False)
    op.create_table('tag',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('title', sa.Unicode(length=250), nullable=False),
        sa.Column('type', sa.SmallInteger(), nullable=True),
        sa.Column('description', sa.UnicodeText(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
        )
    op.create_index(op.f('ix_tag_title'), 'tag', ['title'], unique=False)
    op.create_index(op.f('ix_tag_type'), 'tag', ['type'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_tag_type'), table_name='tag')
    op.drop_index(op.f('ix_tag_title'), table_name='tag')
    op.drop_table('tag')
    op.drop_index(op.f('ix_name_title'), table_name='name')
    op.drop_index(op.f('ix_name_gender'), table_name='name')
    op.drop_table('name')
