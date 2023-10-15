"""add disabled field to user table

Revision ID: 807be5c47b4d
Revises: 334f034f69e2
Create Date: 2023-10-14 13:08:28.691581

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "807be5c47b4d"
down_revision: Union[str, None] = "334f034f69e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("disabled", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "disabled")
    # ### end Alembic commands ###