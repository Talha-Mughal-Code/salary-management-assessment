"use client";

import { type ChangeEvent, type FormEvent, useCallback, useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { FilterOptions } from "@/hooks/useFilterOptions";
import { ApiError, createEmployee, updateEmployee } from "@/lib/api";
import type { Employee, EmployeeDraft, EmployeeUpdate } from "@/types/api";

type Field = {
  name: keyof EmployeeDraft;
  label: string;
  type?: string;
  suggestions?: keyof FilterOptions;
  inputProps?: React.ComponentProps<"input">;
};

const FIELDS: Field[] = [
  { name: "full_name", label: "Full name", inputProps: { maxLength: 200 } },
  {
    name: "email",
    label: "Email",
    type: "email",
    inputProps: { maxLength: 254 },
  },
  { name: "job_title", label: "Job title", suggestions: "job_title" },
  { name: "department", label: "Department", suggestions: "department" },
  {
    name: "country",
    label: "Country code",
    suggestions: "country",
    inputProps: { maxLength: 2, pattern: "[A-Za-z]{2}", placeholder: "DE" },
  },
  {
    name: "currency",
    label: "Currency code",
    inputProps: { maxLength: 3, pattern: "[A-Za-z]{3}", placeholder: "EUR" },
  },
  {
    name: "salary",
    label: "Annual salary (local currency)",
    type: "number",
    inputProps: { min: "0.01", step: "0.01" },
  },
  { name: "hire_date", label: "Hire date", type: "date" },
];

const EMPTY_DRAFT: EmployeeDraft = {
  full_name: "",
  email: "",
  job_title: "",
  department: "",
  country: "",
  currency: "",
  salary: "",
  hire_date: "",
};

type FormErrors = { form?: string; fields: Record<string, string> };

type EmployeeFormDialogProps = {
  employee: Employee | null;
  options: FilterOptions;
  onClose: () => void;
  onSaved: () => void;
};

export function EmployeeFormDialog({
  employee,
  options,
  onClose,
  onSaved,
}: EmployeeFormDialogProps) {
  const [draft, setDraft] = useState<EmployeeDraft>(() => toDraft(employee));
  const [errors, setErrors] = useState<FormErrors>({ fields: {} });
  const [saving, setSaving] = useState(false);

  const handleChange = useCallback(
    (event: ChangeEvent<HTMLInputElement>) =>
      setDraft((current) => ({
        ...current,
        [event.target.name]: event.target.value,
      })),
    [],
  );

  const handleSubmit = useCallback(
    async (event: FormEvent) => {
      event.preventDefault();
      setSaving(true);
      try {
        await (employee
          ? updateEmployee(employee.id, changedFields(toDraft(employee), draft))
          : createEmployee(draft));
        onSaved();
      } catch (error) {
        setErrors(toFormErrors(error));
        setSaving(false);
      }
    },
    [employee, draft, onSaved],
  );

  return (
    <Dialog open onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>
            {employee ? "Edit employee" : "Add employee"}
          </DialogTitle>
          <DialogDescription>
            Salary is in the employee&apos;s local currency. The USD value is
            calculated by the server.
          </DialogDescription>
        </DialogHeader>
        <form
          id="employee-form"
          onSubmit={handleSubmit}
          className="grid gap-3 sm:grid-cols-2"
        >
          {FIELDS.map(({ name, label, type, suggestions, inputProps }) => (
            <div key={name} className="flex flex-col gap-1.5">
              <Label htmlFor={name}>{label}</Label>
              <Input
                id={name}
                name={name}
                type={type ?? "text"}
                required
                value={draft[name]}
                onChange={handleChange}
                list={suggestions && `${name}-options`}
                aria-invalid={Boolean(errors.fields[name])}
                {...inputProps}
              />
              {suggestions && (
                <datalist id={`${name}-options`}>
                  {options[suggestions].map((value) => (
                    <option key={value} value={value} />
                  ))}
                </datalist>
              )}
              {errors.fields[name] && (
                <p className="text-xs text-destructive">
                  {errors.fields[name]}
                </p>
              )}
            </div>
          ))}
        </form>
        {errors.form && (
          <p className="text-sm text-destructive">{errors.form}</p>
        )}
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" form="employee-form" disabled={saving}>
            {saving ? "Saving…" : employee ? "Save changes" : "Add employee"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function toDraft(employee: Employee | null): EmployeeDraft {
  if (!employee) return EMPTY_DRAFT;
  return Object.fromEntries(
    Object.keys(EMPTY_DRAFT).map((key) => [
      key,
      employee[key as keyof EmployeeDraft],
    ]),
  ) as EmployeeDraft;
}

function changedFields(
  original: EmployeeDraft,
  draft: EmployeeDraft,
): EmployeeUpdate {
  return Object.fromEntries(
    Object.entries(draft).filter(
      ([key, value]) => original[key as keyof EmployeeDraft] !== value,
    ),
  );
}

function toFormErrors(error: unknown): FormErrors {
  if (!(error instanceof ApiError))
    return { form: "Something went wrong.", fields: {} };
  if (error.status === 409) return { fields: { email: error.message } };
  return {
    form: Object.keys(error.fieldErrors).length ? undefined : error.message,
    fields: error.fieldErrors,
  };
}
