"""empty message

Revision ID: 0223ce4bf5f2
Revises: a3647e779861
Create Date: 2017-11-26 11:46:13.050915

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0223ce4bf5f2'
down_revision = 'a3647e779861'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('osc_turnover',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('change', sa.Numeric(precision=14, scale=6), nullable=True),
    sa.Column('cnyPrice', sa.Numeric(precision=14, scale=6), nullable=True),
    sa.Column('createTime', sa.Integer(), nullable=True),
    sa.Column('dict_info', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('mark', sa.Integer(), nullable=True),
    sa.Column('sell', sa.Numeric(precision=14, scale=6), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('total', sa.Numeric(precision=14, scale=6), nullable=True),
    sa.Column('turnover', sa.Numeric(precision=14, scale=6), nullable=True),
    sa.Column('exchange', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_osc_turnover_createTime'), 'osc_turnover', ['createTime'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_osc_turnover_createTime'), table_name='osc_turnover')
    op.drop_table('osc_turnover')
    # ### end Alembic commands ###