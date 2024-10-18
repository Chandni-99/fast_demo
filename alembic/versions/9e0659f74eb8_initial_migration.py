"""initial migration

Revision ID: 9e0659f74eb8
Revises: 
Create Date: 2024-10-08 15:31:29.662259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e0659f74eb8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_roles_id', table_name='roles')
    op.drop_index('ix_roles_name', table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('roles_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('permissions', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_roles_name', 'roles', ['name'], unique=False)
    op.create_index('ix_roles_id', 'roles', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('users_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.create_table('user_role',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='user_role_role_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_role_user_id_fkey')
    )
    # ### end Alembic commands ###
