"""add pgvector embedding tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── clause_embeddings ────────────────────────────────
    op.execute("""
        CREATE TABLE clause_embeddings (
            id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            clause_id   UUID NOT NULL REFERENCES clauses(id) ON DELETE CASCADE,
            embedding   vector(1536) NOT NULL,
            created_at  TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.execute(
        "CREATE UNIQUE INDEX uq_clause_embeddings_clause_id "
        "ON clause_embeddings(clause_id)"
    )
    # IVFFlat index for cosine similarity search.
    # lists=100 is a reasonable default; tune upward once the table has >1M rows.
    op.execute("""
        CREATE INDEX idx_clause_embeddings_vector
        ON clause_embeddings USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    """)

    # ── playbook_rule_embeddings ─────────────────────────
    op.execute("""
        CREATE TABLE playbook_rule_embeddings (
            id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            rule_id     UUID NOT NULL REFERENCES playbook_rules(id) ON DELETE CASCADE,
            embedding   vector(1536) NOT NULL,
            created_at  TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.execute(
        "CREATE UNIQUE INDEX uq_playbook_rule_embeddings_rule_id "
        "ON playbook_rule_embeddings(rule_id)"
    )
    op.execute("""
        CREATE INDEX idx_playbook_rule_embeddings_vector
        ON playbook_rule_embeddings USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100)
    """)

    # ── missing_provisions ───────────────────────────────
    # Populated by the Risk Agent when a required playbook rule has no
    # matching clause in the contract.
    op.execute("""
        CREATE TABLE missing_provisions (
            id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            contract_id      UUID NOT NULL REFERENCES contracts(id) ON DELETE CASCADE,
            playbook_rule_id UUID REFERENCES playbook_rules(id) ON DELETE SET NULL,
            description      TEXT NOT NULL,
            detected_at      TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    op.execute("CREATE INDEX ix_missing_provisions_contract_id ON missing_provisions(contract_id)")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS missing_provisions")
    op.execute("DROP TABLE IF EXISTS playbook_rule_embeddings")
    op.execute("DROP TABLE IF EXISTS clause_embeddings")
