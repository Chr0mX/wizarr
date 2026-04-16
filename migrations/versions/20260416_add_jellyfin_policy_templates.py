"""add_jellyfin_policy_templates

Revision ID: 20260416_jf_policy_templates
Revises: 4a39bd26329d
Create Date: 2026-04-16 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20260416_jf_policy_templates"
down_revision = "4a39bd26329d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "jellyfin_policy_template",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("allowed_tags", sa.Text(), nullable=True),
        sa.Column("blocked_tags", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    with op.batch_alter_table("invitation", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("jellyfin_policy_template_id", sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            "fk_invitation_jellyfin_policy_template_id",
            "jellyfin_policy_template",
            ["jellyfin_policy_template_id"],
            ["id"],
            ondelete="SET NULL",
        )

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(sa.Column("policy_template_applied", sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column("policy_template_error", sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("policy_template_error")
        batch_op.drop_column("policy_template_applied")

    with op.batch_alter_table("invitation", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_invitation_jellyfin_policy_template_id", type_="foreignkey"
        )
        batch_op.drop_column("jellyfin_policy_template_id")

    op.drop_table("jellyfin_policy_template")
