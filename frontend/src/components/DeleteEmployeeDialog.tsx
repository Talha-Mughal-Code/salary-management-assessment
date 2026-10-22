"use client";

import { useCallback, useState } from "react";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { ApiError, deleteEmployee } from "@/lib/api";
import type { Employee } from "@/types/api";

type DeleteEmployeeDialogProps = {
  employee: Employee;
  onClose: () => void;
  onDeleted: () => void;
};

export function DeleteEmployeeDialog({
  employee,
  onClose,
  onDeleted,
}: DeleteEmployeeDialogProps) {
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string>();

  const handleDelete = useCallback(async () => {
    setDeleting(true);
    try {
      await deleteEmployee(employee.id);
      onDeleted();
    } catch (caught) {
      setError(
        caught instanceof ApiError ? caught.message : "Something went wrong.",
      );
      setDeleting(false);
    }
  }, [employee.id, onDeleted]);

  return (
    <AlertDialog open onOpenChange={(open) => !open && onClose()}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete {employee.full_name}?</AlertDialogTitle>
          <AlertDialogDescription>
            This permanently removes {employee.full_name} ({employee.email}) and
            cannot be undone.
          </AlertDialogDescription>
        </AlertDialogHeader>
        {error && <p className="text-sm text-destructive">{error}</p>}
        <AlertDialogFooter>
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction
            variant="destructive"
            disabled={deleting}
            onClick={handleDelete}
          >
            {deleting ? "Deleting…" : "Delete"}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
