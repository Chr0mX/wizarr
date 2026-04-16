"""add jellyfin policy templates

Revision ID: 20260416_add_jellyfin_policy_templates
Revises: 4a39bd26329d
Create Date: 2026-04-16
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20260416_add_jellyfin_policy_templates"
down_revision = "4a39bd26329d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "jellyfin_policy_template",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("allowed_tags", sa.JSON(), nullable=False),
        sa.Column("blocked_tags", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.add_column(
        "invitation",
        sa.Column("policy_template_id", sa.Integer(), nullable=True),
    )
    with op.batch_alter_table("invitation", schema=None) as batch_op:
        batch_op.create_foreign_key(
            "fk_invitation_policy_template_id",
            "jellyfin_policy_template",
            ["policy_template_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade() -> None:
    with op.batch_alter_table("invitation", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_invitation_policy_template_id",
            type_="foreignkey",
        )
    op.drop_column("invitation", "policy_template_id")
    op.drop_table("jellyfin_policy_template")
