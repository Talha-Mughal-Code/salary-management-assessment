"use client";

import { useCallback } from "react";

import { useApiData } from "@/hooks/useApiData";
import { getPaySummary } from "@/lib/api";
import type { GroupBy } from "@/types/api";

export type FilterOptions = Record<GroupBy, string[]>;

const GROUPS: GroupBy[] = ["country", "department", "job_title"];

export function useFilterOptions(): FilterOptions {
  const load = useCallback(async (signal: AbortSignal) => {
    const summaries = await Promise.all(
      GROUPS.map((group_by) => getPaySummary({ group_by }, signal)),
    );
    return Object.fromEntries(
      summaries.map((summary) => [
        summary.group_by,
        summary.groups.map((group) => group.key).sort(),
      ]),
    ) as FilterOptions;
  }, []);
  return (
    useApiData(load).data ?? { country: [], department: [], job_title: [] }
  );
}
