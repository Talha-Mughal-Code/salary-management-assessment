import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { formatCount, formatUsd } from "@/lib/format";
import type { GroupPayStats, PayStats } from "@/types/api";

const STATS: { key: keyof PayStats; label: string }[] = [
  { key: "min", label: "Min" },
  { key: "p25", label: "25th pct" },
  { key: "median", label: "Median" },
  { key: "p75", label: "75th pct" },
  { key: "max", label: "Max" },
  { key: "average", label: "Average" },
];

type PaySummaryTableProps = { groupLabel: string; groups: GroupPayStats[] };

export function PaySummaryTable({ groupLabel, groups }: PaySummaryTableProps) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{groupLabel}</TableHead>
          <TableHead className="text-right">Headcount</TableHead>
          {STATS.map(({ key, label }) => (
            <TableHead key={key} className="text-right">
              {label}
            </TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {groups.map((group) => (
          <TableRow key={group.key}>
            <TableCell className="font-medium">{group.key}</TableCell>
            <TableCell className="text-right tabular-nums">
              {formatCount(group.headcount)}
            </TableCell>
            {STATS.map(({ key }) => (
              <TableCell
                key={key}
                className={`text-right tabular-nums ${key === "median" ? "font-medium" : ""}`}
              >
                {formatUsd(group[key] as string | null)}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
