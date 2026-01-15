"""Initial training result tables

Revision ID: 001
Revises:
Create Date: 2025-01-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "training_result_stage",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.CHAR(36), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column(
            "correct_problem_count", sa.Integer(), nullable=False, server_default="0"
        ),
        sa.Column("average_response_time_ms", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("IN_PROGRESS", "COMPLETED", "ABORTED", name="stagestatus"),
            nullable=False,
            server_default="IN_PROGRESS",
        ),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_training_result_stage")),
    )
    op.create_index(
        op.f("ix_training_result_stage_user_id"), "training_result_stage", ["user_id"], unique=False
    )

    op.create_table(
        "training_result_problem",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("stage_id", sa.BigInteger(), nullable=False),
        sa.Column(
            "spatial_position",
            sa.Enum(
                "FRONT_HORIZONTAL",
                "FRONT_LEFT_VERTICAL",
                "FRONT_RIGHT_VERTICAL",
                "BACK_HORIZONTAL",
                "BACK_LEFT_VERTICAL",
                "BACK_RIGHT_VERTICAL",
                name="spatialposition",
            ),
            nullable=False,
        ),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("response_time_ms", sa.Integer(), nullable=True),
        sa.Column("selection_count", sa.Integer(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_training_result_problem")),
    )
    op.create_index(
        op.f("ix_training_result_problem_stage_id"),
        "training_result_problem",
        ["stage_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_training_result_problem_stage_id"), table_name="training_result_problem")
    op.drop_table("training_result_problem")
    op.drop_index(op.f("ix_training_result_stage_user_id"), table_name="training_result_stage")
    op.drop_table("training_result_stage")

    op.execute("DROP TYPE IF EXISTS spatialposition")
    op.execute("DROP TYPE IF EXISTS stagestatus")
