"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback, useMemo } from "react";

import type { EmployeeListParams, SortField, SortOrder } from "@/types/api";

export const PAGE_SIZES = [10, 25, 50, 100];
const SORT_FIELDS: SortField[] = [
  "full_name",
  "job_title",
  "department",
  "country",
  "salary_usd",
  "hire_date",
];
const DEFAULTS: EmployeeListParams = {
  page: 1,
  page_size: 25,
  sort: "full_name",
  order: "asc",
};

export type QueryChanges = Partial<
  Record<keyof EmployeeListParams, string | number>
>;

function parse(search: URLSearchParams): EmployeeListParams {
  const page = Number(search.get("page"));
  const pageSize = Number(search.get("page_size"));
  const sort = search.get("sort") as SortField;
  const order = search.get("order") as SortOrder;
  return {
    page: Number.isInteger(page) && page > 0 ? page : DEFAULTS.page,
    page_size: PAGE_SIZES.includes(pageSize) ? pageSize : DEFAULTS.page_size,
    sort: SORT_FIELDS.includes(sort) ? sort : DEFAULTS.sort,
    order: order === "desc" ? "desc" : "asc",
    q: search.get("q") ?? undefined,
    country: search.get("country") ?? undefined,
    job_title: search.get("job_title") ?? undefined,
    department: search.get("department") ?? undefined,
  };
}

export function useEmployeeQuery() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();
  const params = useMemo(() => parse(searchParams), [searchParams]);

  const update = useCallback(
    (changes: QueryChanges) => {
      const next = new URLSearchParams(searchParams);
      if (!("page" in changes)) next.delete("page");
      for (const [key, value] of Object.entries(changes)) {
        const isDefault = value === DEFAULTS[key as keyof EmployeeListParams];
        if (value === "" || value === undefined || isDefault) next.delete(key);
        else next.set(key, String(value));
      }
      const query = next.toString();
      router.replace(query ? `${pathname}?${query}` : pathname, {
        scroll: false,
      });
    },
    [searchParams, router, pathname],
  );

  return { params, update };
}
