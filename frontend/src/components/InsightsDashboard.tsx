"use client";

import { type ChangeEvent, useCallback, useState } from "react";

import { PaySummaryTable } from "@/components/PaySummaryTable";
import { RequestState } from "@/components/RequestState";
import { SalaryDistributionChart } from "@/components/SalaryDistributionChart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  NativeSelect,
  NativeSelectOption,
} from "@/components/ui/native-select";
import { useApiData } from "@/hooks/useApiData";
import { useFilterOptions } from "@/hooks/useFilterOptions";
import { getPaySummary, getSalaryDistribution } from "@/lib/api";
import { formatCount, formatUsd } from "@/lib/format";
import type { EmployeeFilters, GroupBy } from "@/types/api";

const GROUP_LABELS: Record<GroupBy, string> = {
  country: "Country",
  job_title: "Job title",
  department: "Department",
};

export function InsightsDashboard() {
  const options = useFilterOptions();
  const [groupBy, setGroupBy] = useState<GroupBy>("country");
  const [filters, setFilters] = useState<EmployeeFilters>({});
  const loadSummary = useCallback(
    (signal: AbortSignal) =>
      getPaySummary({ ...filters, group_by: groupBy }, signal),
    [filters, groupBy],
  );
  const loadDistribution = useCallback(
    (signal: AbortSignal) => getSalaryDistribution(filters, signal),
    [filters],
  );
  const summary = useApiData(loadSummary);
  const distribution = useApiData(loadDistribution);
  const overall = summary.data?.overall;
  const groups = summary.data?.groups ?? [];

  const handleGroupBy = useCallback(
    (event: ChangeEvent<HTMLSelectElement>) =>
      setGroupBy(event.target.value as GroupBy),
    [],
  );
  const handleFilter = useCallback(
    (event: ChangeEvent<HTMLSelectElement>) =>
      setFilters((current) => ({
        ...current,
        [event.target.name]: event.target.value,
      })),
    [],
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center gap-2 text-sm">
        <span className="text-muted-foreground">Group by</span>
        <NativeSelect
          aria-label="Group by"
          value={groupBy}
          onChange={handleGroupBy}
        >
          {Object.entries(GROUP_LABELS).map(([value, label]) => (
            <NativeSelectOption key={value} value={value}>
              {label}
            </NativeSelectOption>
          ))}
        </NativeSelect>
        <span className="ml-2 text-muted-foreground">for</span>
        {(["country", "department"] as const).map((name) => (
          <NativeSelect
            key={name}
            name={name}
            aria-label={`Filter by ${GROUP_LABELS[name].toLowerCase()}`}
            value={filters[name] ?? ""}
            onChange={handleFilter}
          >
            <NativeSelectOption value="">
              All {name === "country" ? "countries" : "departments"}
            </NativeSelectOption>
            {options[name].map((value) => (
              <NativeSelectOption key={value} value={value}>
                {value}
              </NativeSelectOption>
            ))}
          </NativeSelect>
        ))}
      </div>

      <RequestState
        loading={summary.loading}
        slow={summary.slow}
        error={summary.error}
        hasData={overall !== undefined}
        onRetry={summary.reload}
      >
        {overall && (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            <Stat label="Employees" value={formatCount(overall.headcount)} />
            <Stat
              label={`Median (${summary.data?.currency})`}
              value={formatUsd(overall.median)}
            />
            <Stat label="Average" value={formatUsd(overall.average)} />
            <Stat
              label="Middle 50%"
              value={`${formatUsd(overall.p25)} – ${formatUsd(overall.p75)}`}
            />
          </div>
        )}
      </RequestState>

      <Card>
        <CardHeader>
          <CardTitle>Salary distribution</CardTitle>
        </CardHeader>
        <CardContent>
          <RequestState
            loading={distribution.loading}
            slow={false}
            error={distribution.error}
            hasData={distribution.data !== undefined}
            onRetry={distribution.reload}
          >
            {distribution.data?.buckets.length === 0 ? (
              <p className="text-sm text-muted-foreground">
                No employees match these filters.
              </p>
            ) : (
              <SalaryDistributionChart
                buckets={distribution.data?.buckets ?? []}
              />
            )}
          </RequestState>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Pay by {GROUP_LABELS[groupBy].toLowerCase()}</CardTitle>
          {groups.length > 1 && (
            <p className="text-sm text-muted-foreground">
              Highest median: {groups[0].key} ({formatUsd(groups[0].median)}).
              Lowest: {groups[groups.length - 1].key} (
              {formatUsd(groups[groups.length - 1].median)}).
            </p>
          )}
        </CardHeader>
        <CardContent>
          {groups.length === 0 && !summary.loading ? (
            <p className="text-sm text-muted-foreground">
              No employees match these filters.
            </p>
          ) : (
            <PaySummaryTable
              groupLabel={GROUP_LABELS[groupBy]}
              groups={groups}
            />
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <Card size="sm">
      <CardContent className="flex flex-col gap-1">
        <span className="text-xs text-muted-foreground">{label}</span>
        <span className="text-lg font-semibold tabular-nums">{value}</span>
      </CardContent>
    </Card>
  );
}
