from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'eaac49fb3a17'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'requested_wallets',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('address', sa.String(length=34), nullable=False),
        sa.Column('balance', sa.Numeric(precision=30, scale=6), nullable=False),
        sa.Column('bandwidth', sa.Integer(), nullable=False),
        sa.Column('energy', sa.Integer(), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
            comment='Дата записи в UTC. Автоматически конвертируется в local-time при чтении'
        ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('requested_wallets')
