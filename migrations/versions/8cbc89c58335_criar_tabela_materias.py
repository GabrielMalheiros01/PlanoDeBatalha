"""Criar tabela materias

Revision ID: 8cbc89c58335
Revises: 
Create Date: 2024-08-20 17:00:20.468930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cbc89c58335'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('materias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('codigo', sa.String(length=50), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('carga_horaria', sa.Integer(), nullable=False),
    sa.Column('natureza', sa.String(length=2), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('codigo')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('materias')
    # ### end Alembic commands ###
