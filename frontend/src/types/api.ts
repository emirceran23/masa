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
  created_at: string;
  updated_at: string;
}

export interface ContractDetail extends Contract {
  raw_text: string | null;
  clauses: Clause[];
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
