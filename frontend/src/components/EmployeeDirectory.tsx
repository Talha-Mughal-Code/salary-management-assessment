"use client";

import { Download, Plus, SearchX, X } from "lucide-react";
import { useCallback, useState } from "react";

import { DeleteEmployeeDialog } from "@/components/DeleteEmployeeDialog";
import { EmployeeFilters } from "@/components/EmployeeFilters";
import { EmployeeFormDialog } from "@/components/EmployeeFormDialog";
import { EmployeeTable } from "@/components/EmployeeTable";
import { RequestState } from "@/components/RequestState";
import { TablePagination } from "@/components/TablePagination";
import { Button, buttonVariants } from "@/components/ui/button";
import { useApiData } from "@/hooks/useApiData";
import { useEmployeeQuery } from "@/hooks/useEmployeeQuery";
import { useFilterOptions } from "@/hooks/useFilterOptions";
import { exportEmployeesUrl, listEmployees } from "@/lib/api";
import type { Employee, SortField } from "@/types/api";

export function EmployeeDirectory() {
  const { params, update } = useEmployeeQuery();
  const options = useFilterOptions();
  const load = useCallback(
    (signal: AbortSignal) => listEmployees(params, signal),
    [params],
  );
  const { data, error, loading, slow, reload } = useApiData(load);
  const [editing, setEditing] = useState<Employee | null>();
  const [deleting, setDeleting] = useState<Employee>();
  const [filtersKey, setFiltersKey] = useState(0);
  const hasFilters = Boolean(
    params.q || params.country || params.job_title || params.department,
  );

  const handleSort = useCallback(
    (field: SortField) =>
      update({
        sort: field,
        order: params.sort === field && params.order === "asc" ? "desc" : "asc",
      }),
    [update, params.sort, params.order],
  );

  const clearFilters = useCallback(() => {
    update({ q: "", country: "", job_title: "", department: "" });
    setFiltersKey((key) => key + 1);
  }, [update]);

  const closeForm = useCallback(() => setEditing(undefined), []);
  const closeDelete = useCallback(() => setDeleting(undefined), []);

  const handleSaved = useCallback(() => {
    setEditing(undefined);
    reload();
  }, [reload]);

  const handleDeleted = useCallback(() => {
    setDeleting(undefined);
    if (data?.items.length === 1 && params.page > 1)
      update({ page: params.page - 1 });
    else reload();
  }, [data, params.page, update, reload]);

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <EmployeeFilters
          key={filtersKey}
          params={params}
          options={options}
          onChange={update}
        />
        <div className="flex flex-wrap gap-2">
          {hasFilters && (
            <Button variant="ghost" onClick={clearFilters}>
              <X />
              Clear filters
            </Button>
          )}
          <a
            href={exportEmployeesUrl(params)}
            className={buttonVariants({ variant: "outline" })}
          >
            <Download />
            Export CSV
          </a>
          <Button onClick={() => setEditing(null)}>
            <Plus />
            Add employee
          </Button>
        </div>
      </div>

      <RequestState
        loading={loading}
        slow={slow}
        error={error}
        hasData={data !== undefined}
        onRetry={reload}
      >
        {data?.total === 0 ? (
          <div className="flex flex-col items-center gap-3 rounded-lg border border-dashed py-12 text-center text-sm text-muted-foreground">
            <SearchX className="size-6" />
            {hasFilters
              ? "No employees match these filters."
              : "No employees yet."}
            {hasFilters && (
              <Button variant="outline" onClick={clearFilters}>
                Clear filters
              </Button>
            )}
          </div>
        ) : (
          data && (
            <div className="flex flex-col gap-3">
              <div className="rounded-lg border">
                <EmployeeTable
                  employees={data.items}
                  sort={params.sort}
                  order={params.order}
                  onSort={handleSort}
                  onEdit={setEditing}
                  onDelete={setDeleting}
                />
              </div>
              <TablePagination
                page={params.page}
                pageSize={params.page_size}
                total={data.total}
                onChange={update}
              />
            </div>
          )
        )}
      </RequestState>

      {editing !== undefined && (
        <EmployeeFormDialog
          employee={editing}
          options={options}
          onClose={closeForm}
          onSaved={handleSaved}
        />
      )}
      {deleting && (
        <DeleteEmployeeDialog
          employee={deleting}
          onClose={closeDelete}
          onDeleted={handleDeleted}
        />
      )}
    </div>
  );
}
