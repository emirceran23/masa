"""initial schema

Revision ID: 0001
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── pgvector extension ───────────────────────────────
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # ── users ────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(150), nullable=False),
        sa.Column("role", sa.String(30), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # ── playbooks ────────────────────────────────────────
    op.create_table(
        "playbooks",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("is_default", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # ── playbook_rules ───────────────────────────────────
    op.create_table(
        "playbook_rules",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("playbook_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("playbooks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("rule_type", sa.String(50), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("threshold_value", sa.Float, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── contracts ────────────────────────────────────────
    op.create_table(
        "contracts",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("storage_path", sa.String(500), nullable=False),
        sa.Column("file_format", sa.String(10), nullable=False),
        sa.Column("file_size", sa.Integer, nullable=False),
        sa.Column("raw_text", sa.Text, nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="uploaded"),
        sa.Column("total_clauses", sa.Integer, nullable=False, server_default="0"),
        sa.Column("playbook_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("playbooks.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    # ── clauses ──────────────────────────────────────────
    op.create_table(
        "clauses",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("contract_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sequence_no", sa.Integer, nullable=False),
        sa.Column("original_text", sa.Text, nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("confidence_score", sa.Float, nullable=False),
        sa.Column("status", sa.String(30), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── risk_assessments ─────────────────────────────────
    op.create_table(
        "risk_assessments",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("clause_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("clauses.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("risk_level", sa.String(30), nullable=False),
        sa.Column("commercial_score", sa.Float, nullable=False),
        sa.Column("legal_score", sa.Float, nullable=False),
        sa.Column("rationale", sa.Text, nullable=True),
        sa.Column("policy_compliance", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("cross_validated", sa.Boolean, nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── revisions ────────────────────────────────────────
    op.create_table(
        "revisions",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("clause_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("clauses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("suggested_text", sa.Text, nullable=False),
        sa.Column("context_used", sa.Text, nullable=True),
        sa.Column("diff_html", sa.Text, nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="pending"),
        sa.Column("edited_text", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── approval_decisions ───────────────────────────────
    op.create_table(
        "approval_decisions",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("clause_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("clauses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("decision", sa.String(30), nullable=False),
        sa.Column("comment", sa.Text, nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── audit_logs ───────────────────────────────────────
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action_type", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(50), nullable=False),
        sa.Column("resource_id", sa.String(50), nullable=True),
        sa.Column("details", sa.dialects.postgresql.JSONB, nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── reports ──────────────────────────────────────────
    op.create_table(
        "reports",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("contract_id", sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("report_type", sa.String(30), nullable=False, server_default="summary"),
        sa.Column("total_clauses", sa.Integer, nullable=False, server_default="0"),
        sa.Column("summary_data", sa.dialects.postgresql.JSONB, nullable=True),
        sa.Column("storage_path", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── Indexes ──────────────────────────────────────────
    op.create_index("ix_contracts_user_id", "contracts", ["user_id"])
    op.create_index("ix_contracts_status", "contracts", ["status"])
    op.create_index("ix_clauses_contract_id", "clauses", ["contract_id"])
    op.create_index("ix_audit_logs_user_id", "audit_logs", ["user_id"])
    op.create_index("ix_audit_logs_action_type", "audit_logs", ["action_type"])


def downgrade() -> None:
    op.drop_table("reports")
    op.drop_table("audit_logs")
    op.drop_table("approval_decisions")
    op.drop_table("revisions")
    op.drop_table("risk_assessments")
    op.drop_table("clauses")
    op.drop_table("contracts")
    op.drop_table("playbook_rules")
    op.drop_table("playbooks")
    op.drop_table("users")
    op.execute("DROP EXTENSION IF EXISTS vector")
