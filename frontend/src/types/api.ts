export type Money = string;

export type Employee = {
  id: number;
  full_name: string;
  email: string;
  job_title: string;
  department: string;
  country: string;
  currency: string;
  salary: Money;
  salary_usd: Money;
  hire_date: string;
  created_at: string;
  updated_at: string;
};

export type EmployeeDraft = Pick<
  Employee,
  | "full_name"
  | "email"
  | "job_title"
  | "department"
  | "country"
  | "currency"
  | "salary"
  | "hire_date"
>;

export type EmployeeUpdate = Partial<EmployeeDraft>;

export type SortField =
  | "full_name"
  | "job_title"
  | "department"
  | "country"
  | "salary_usd"
  | "hire_date";

export type SortOrder = "asc" | "desc";

export type EmployeeFilters = {
  country?: string;
  job_title?: string;
  department?: string;
};

export type EmployeeQuery = EmployeeFilters & {
  q?: string;
  sort: SortField;
  order: SortOrder;
};

export type EmployeeListParams = EmployeeQuery & {
  page: number;
  page_size: number;
};

export type EmployeePage = {
  items: Employee[];
  total: number;
  page: number;
  page_size: number;
};

export type GroupBy = "country" | "job_title" | "department";

export type PayStats = {
  headcount: number;
  min: Money | null;
  p25: Money | null;
  median: Money | null;
  p75: Money | null;
  max: Money | null;
  average: Money | null;
};

export type GroupPayStats = PayStats & { key: string };

export type PaySummary = {
  group_by: GroupBy;
  currency: string;
  overall: PayStats;
  groups: GroupPayStats[];
};

export type SalaryBucket = { min: Money; max: Money; count: number };

export type SalaryDistribution = { currency: string; buckets: SalaryBucket[] };
