"""merge policy template migration head

Revision ID: 20260416_merge_policy_template_head
Revises: 20260401_repair, 20260416_add_jellyfin_policy_templates
Create Date: 2026-04-16
"""

# revision identifiers, used by Alembic.
revision = "20260416_merge_policy_template_head"
down_revision = ("20260401_repair", "20260416_add_jellyfin_policy_templates")
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
