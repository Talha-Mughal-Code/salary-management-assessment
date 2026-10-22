"use client";

import { ArrowDown, ArrowUp, ArrowUpDown, Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { USD, formatDate, formatMoney, formatUsd } from "@/lib/format";
import type { Employee, SortField, SortOrder } from "@/types/api";

const COLUMNS: { label: string; field?: SortField; numeric?: boolean }[] = [
  { label: "Name", field: "full_name" },
  { label: "Job title", field: "job_title" },
  { label: "Department", field: "department" },
  { label: "Country", field: "country" },
  { label: "Salary", numeric: true },
  { label: `Salary (${USD})`, field: "salary_usd", numeric: true },
  { label: "Hired", field: "hire_date" },
];

type EmployeeTableProps = {
  employees: Employee[];
  sort: SortField;
  order: SortOrder;
  onSort: (field: SortField) => void;
  onEdit: (employee: Employee) => void;
  onDelete: (employee: Employee) => void;
};

export function EmployeeTable({
  employees,
  sort,
  order,
  onSort,
  onEdit,
  onDelete,
}: EmployeeTableProps) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          {COLUMNS.map(({ label, field, numeric }) => (
            <TableHead
              key={label}
              className={numeric ? "text-right" : undefined}
              aria-sort={ariaSort(field === sort, order)}
            >
              {field ? (
                <Button
                  variant="ghost"
                  size="sm"
                  className="-mx-2.5"
                  onClick={() => onSort(field)}
                >
                  {label}
                  <SortIcon active={field === sort} order={order} />
                </Button>
              ) : (
                label
              )}
            </TableHead>
          ))}
          <TableHead>
            <span className="sr-only">Actions</span>
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {employees.map((employee) => (
          <TableRow key={employee.id}>
            <TableCell>
              <div className="font-medium">{employee.full_name}</div>
              <div className="text-xs text-muted-foreground">
                {employee.email}
              </div>
            </TableCell>
            <TableCell>{employee.job_title}</TableCell>
            <TableCell>{employee.department}</TableCell>
            <TableCell>{employee.country}</TableCell>
            <TableCell className="text-right tabular-nums">
              {formatMoney(employee.salary, employee.currency)}
            </TableCell>
            <TableCell className="text-right tabular-nums">
              {formatUsd(employee.salary_usd)}
            </TableCell>
            <TableCell>{formatDate(employee.hire_date)}</TableCell>
            <TableCell className="text-right whitespace-nowrap">
              <Button
                variant="ghost"
                size="icon-sm"
                aria-label={`Edit ${employee.full_name}`}
                onClick={() => onEdit(employee)}
              >
                <Pencil />
              </Button>
              <Button
                variant="ghost"
                size="icon-sm"
                aria-label={`Delete ${employee.full_name}`}
                onClick={() => onDelete(employee)}
              >
                <Trash2 />
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

function ariaSort(active: boolean, order: SortOrder) {
  if (!active) return undefined;
  return order === "asc" ? "ascending" : "descending";
}

function SortIcon({ active, order }: { active: boolean; order: SortOrder }) {
  if (!active) return <ArrowUpDown className="text-muted-foreground" />;
  return order === "asc" ? <ArrowUp /> : <ArrowDown />;
}
