import type {
  Employee,
  EmployeeDraft,
  EmployeeFilters,
  EmployeeListParams,
  EmployeePage,
  EmployeeQuery,
  EmployeeUpdate,
  GroupBy,
  PaySummary,
  SalaryDistribution,
} from "@/types/api";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "";

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly fieldErrors: Record<string, string> = {},
  ) {
    super(message);
  }
}

type ValidationIssue = { type: string; loc: (string | number)[]; msg: string };

const issueMessage = (issue: ValidationIssue) =>
  issue.type === "string_pattern_mismatch"
    ? "Has an invalid format."
    : issue.msg.replace(/^Value error, /, "");

function toQueryString(params: object): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") search.set(key, String(value));
  }
  return search.toString();
}

async function toApiError(response: Response): Promise<ApiError> {
  const body: unknown = await response.json().catch(() => null);
  const detail =
    body && typeof body === "object" && "detail" in body ? body.detail : null;
  if (typeof detail === "string") return new ApiError(detail, response.status);
  if (Array.isArray(detail)) {
    const fieldErrors = Object.fromEntries(
      (detail as ValidationIssue[]).map((issue) => [
        String(issue.loc.at(-1)),
        issueMessage(issue),
      ]),
    );
    return new ApiError(
      "Please fix the highlighted fields.",
      response.status,
      fieldErrors,
    );
  }
  return new ApiError(`Request failed (${response.status}).`, response.status);
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: init?.body ? { "Content-Type": "application/json" } : undefined,
  }).catch(() => {
    throw new ApiError("Could not reach the server.", 0);
  });
  if (!response.ok) throw await toApiError(response);
  return response.status === 204 ? (undefined as T) : response.json();
}

export const listEmployees = (
  params: EmployeeListParams,
  signal?: AbortSignal,
) =>
  request<EmployeePage>(`/api/v1/employees?${toQueryString(params)}`, {
    signal,
  });

export const createEmployee = (draft: EmployeeDraft) =>
  request<Employee>("/api/v1/employees", {
    method: "POST",
    body: JSON.stringify(draft),
  });

export const updateEmployee = (id: number, changes: EmployeeUpdate) =>
  request<Employee>(`/api/v1/employees/${id}`, {
    method: "PATCH",
    body: JSON.stringify(changes),
  });

export const deleteEmployee = (id: number) =>
  request<void>(`/api/v1/employees/${id}`, { method: "DELETE" });

export const exportEmployeesUrl = ({
  q,
  country,
  job_title,
  department,
  sort,
  order,
}: EmployeeQuery) =>
  `${BASE_URL}/api/v1/employees/export?${toQueryString({ q, country, job_title, department, sort, order })}`;

export const getPaySummary = (
  params: EmployeeFilters & { group_by: GroupBy },
  signal?: AbortSignal,
) =>
  request<PaySummary>(`/api/v1/insights/summary?${toQueryString(params)}`, {
    signal,
  });

export const getSalaryDistribution = (
  filters: EmployeeFilters,
  signal?: AbortSignal,
) =>
  request<SalaryDistribution>(
    `/api/v1/insights/distribution?${toQueryString(filters)}`,
    {
      signal,
    },
  );
