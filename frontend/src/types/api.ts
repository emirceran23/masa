/* ── TypeScript types for API responses ─────────────────── */

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Contract {
  id: string;
  file_name: string;
  file_format: string;
  file_size: number;
  status: "uploaded" | "processing" | "analyzed" | "error";
  total_clauses: number;
  uploaded_at: string;
  analyzed_at: string | null;
}

export interface ClauseListResponse {
  total: number;
  items: Clause[];
}

export interface ContractDetail extends Contract {
  raw_text: string | null;
}

export interface Clause {
  id: string;
  sequence_no: number;
  original_text: string;
  category: string;
  confidence_score: number;
  status: "draft" | "in_review" | "approved" | "rejected";
  created_at: string;
}

export interface ClauseDetail extends Clause {
  risk_assessment: RiskAssessment | null;
  revisions: Revision[];
}

export interface RiskAssessment {
  id: string;
  risk_level: string;
  commercial_score: number;
  legal_score: number;
  rationale: string | null;
  policy_compliance: boolean;
  cross_validated: boolean;
}

export interface Revision {
  id: string;
  suggested_text: string;
  context_used: string | null;
  diff_html: string | null;
  status: "pending" | "accepted" | "rejected" | "edited";
  edited_text: string | null;
  created_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface AnalysisProgress {
  contract_id: string;
  status: string;
  progress: number;
  message: string;
}

export interface MessageResponse {
  message: string;
}

/* ── Playbook ─────────────────────────────────────────────── */

export type PlaybookRuleType = "acceptable" | "rejected" | "required" | "threshold";

export interface PlaybookRule {
  id: string;
  rule_type: PlaybookRuleType;
  content: string;
  threshold_value: number | null;
  created_at: string;
}

export interface PlaybookRuleInput {
  rule_type: PlaybookRuleType;
  content: string;
  threshold_value: number | null;
}

export interface Playbook {
  id: string;
  user_id: string;
  name: string;
  description: string | null;
  is_default: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface PlaybookDetail extends Playbook {
  rules: PlaybookRule[];
}

/* ── Risk summary / missing provisions ───────────────────── */

export interface RiskAssessmentDetail extends RiskAssessment {
  clause_id: string;
  assessed_at: string;
}

export interface MissingProvision {
  id: string;
  contract_id: string;
  playbook_rule_id: string | null;
  description: string;
  detected_at: string;
}

/* ── Revisions ───────────────────────────────────────────────── */

export type RevisionStatus = "pending" | "accepted" | "rejected" | "edited";

export interface RevisionDetail {
  id: string;
  clause_id: string;
  suggested_text: string;
  context_used: string | null;
  diff_html: string | null;
  status: RevisionStatus;
  edited_text: string | null;
  created_at: string;
}

/* ── Approvals ───────────────────────────────────────────────── */

export type ApprovalDecision = "approved" | "rejected" | "revise";

export interface ApprovalDecisionRecord {
  id: string;
  clause_id: string;
  user_id: string;
  decision: ApprovalDecision;
  comment: string | null;
  decided_at: string;
}

/* ── Reports ─────────────────────────────────────────────────── */

export interface ReportSummaryData {
  risk_counts: Record<string, number>;
  status_counts: Record<string, number>;
  revision_counts: Record<string, number>;
  missing_provisions_count: number;
  missing_provisions: Array<{ key: string; description: string }>;
  generated_at: string;
  contract_name: string;
}

export interface Report {
  id: string;
  contract_id: string;
  report_type: "summary" | "detailed";
  total_clauses: number | null;
  summary_data: ReportSummaryData | null;
  storage_path: string | null;
  created_at: string;
}
