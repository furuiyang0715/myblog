"""empty message

Revision ID: 5211d59c957d
Revises: f1c5d811c57d
Create Date: 2020-09-02 10:27:17.252160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5211d59c957d'
down_revision = 'f1c5d811c57d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
