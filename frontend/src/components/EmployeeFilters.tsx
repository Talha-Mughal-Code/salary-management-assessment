"use client";

import { Search } from "lucide-react";
import { type ChangeEvent, useCallback, useRef } from "react";

import { Input } from "@/components/ui/input";
import {
  NativeSelect,
  NativeSelectOption,
} from "@/components/ui/native-select";
import type { QueryChanges } from "@/hooks/useEmployeeQuery";
import type { FilterOptions } from "@/hooks/useFilterOptions";
import type { EmployeeListParams, GroupBy } from "@/types/api";

const SEARCH_DELAY_MS = 300;
const FILTERS: { name: GroupBy; label: string }[] = [
  { name: "country", label: "All countries" },
  { name: "department", label: "All departments" },
  { name: "job_title", label: "All job titles" },
];

type EmployeeFiltersProps = {
  params: EmployeeListParams;
  options: FilterOptions;
  onChange: (changes: QueryChanges) => void;
};

export function EmployeeFilters({
  params,
  options,
  onChange,
}: EmployeeFiltersProps) {
  const timer = useRef<ReturnType<typeof setTimeout>>(undefined);

  const handleSearch = useCallback(
    (event: ChangeEvent<HTMLInputElement>) => {
      const q = event.target.value.trim();
      clearTimeout(timer.current);
      timer.current = setTimeout(() => onChange({ q }), SEARCH_DELAY_MS);
    },
    [onChange],
  );

  const handleFilter = useCallback(
    (event: ChangeEvent<HTMLSelectElement>) =>
      onChange({ [event.target.name]: event.target.value }),
    [onChange],
  );

  return (
    <div className="flex flex-wrap items-center gap-2">
      <div className="relative w-full sm:w-64">
        <Search className="pointer-events-none absolute top-1/2 left-2.5 size-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          type="search"
          placeholder="Search name or email"
          aria-label="Search name or email"
          defaultValue={params.q}
          onChange={handleSearch}
          className="pl-8"
        />
      </div>
      {FILTERS.map(({ name, label }) => (
        <NativeSelect
          key={name}
          name={name}
          aria-label={label}
          value={params[name] ?? ""}
          onChange={handleFilter}
        >
          <NativeSelectOption value="">{label}</NativeSelectOption>
          {options[name].map((value) => (
            <NativeSelectOption key={value} value={value}>
              {value}
            </NativeSelectOption>
          ))}
        </NativeSelect>
      ))}
    </div>
  );
}
