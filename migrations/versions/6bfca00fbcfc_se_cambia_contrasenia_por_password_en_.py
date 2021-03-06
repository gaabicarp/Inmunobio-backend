"""Se cambia contrasenia por password en el model Usuario

Revision ID: 6bfca00fbcfc
Revises: 
Create Date: 2021-03-21 02:53:28.152881

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6bfca00fbcfc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuarios', sa.Column('password', sa.String(length=30), nullable=True))
    op.drop_column('usuarios', 'contrasenia')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuarios', sa.Column('contrasenia', mysql.VARCHAR(length=30), nullable=True))
    op.drop_column('usuarios', 'password')
    # ### end Alembic commands ###
