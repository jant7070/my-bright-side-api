"""empty message

Revision ID: 01d5d840949c
Revises: f7ecf6483133
Create Date: 2024-03-07 09:03:53.361108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01d5d840949c'
down_revision = 'f7ecf6483133'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('hashed_password', sa.String(length=150), nullable=False),
    sa.Column('salt', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('file', sa.String(length=500), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('file')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=1000), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('admins_id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['admins_id'], ['admins.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('news')
    with op.batch_alter_table('receipt', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fecha', sa.String(length=150), nullable=False))
        batch_op.drop_constraint('receipt_number_key', type_='unique')
        batch_op.drop_column('number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('receipt', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_unique_constraint('receipt_number_key', ['number'])
        batch_op.drop_column('fecha')

    op.create_table('news',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('file', sa.VARCHAR(length=1000), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='news_pkey')
    )
    op.drop_table('message')
    op.drop_table('files')
    op.drop_table('admins')
    # ### end Alembic commands ###
