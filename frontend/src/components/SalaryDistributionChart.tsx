import { formatCompactUsd, formatCount } from "@/lib/format";
import type { SalaryBucket } from "@/types/api";

export function SalaryDistributionChart({
  buckets,
}: {
  buckets: SalaryBucket[];
}) {
  if (buckets.length === 0) return null;
  const tallest = Math.max(...buckets.map((bucket) => bucket.count));
  const first = buckets[0];
  const last = buckets[buckets.length - 1];

  return (
    <figure className="flex flex-col gap-2">
      <div
        role="img"
        aria-label={`Salary distribution from ${formatCompactUsd(first.min)} to ${formatCompactUsd(last.max)} in ${buckets.length} ranges`}
        className="flex h-48 items-end gap-1"
      >
        {buckets.map((bucket) => (
          <div
            key={bucket.min}
            title={`${formatCompactUsd(bucket.min)}–${formatCompactUsd(bucket.max)}: ${formatCount(bucket.count)} employees`}
            className="flex-1 rounded-t bg-primary/80 hover:bg-primary"
            style={{
              height: `${Math.max((bucket.count / tallest) * 100, bucket.count ? 1 : 0)}%`,
            }}
          />
        ))}
      </div>
      <figcaption className="flex justify-between text-xs text-muted-foreground tabular-nums">
        <span>{formatCompactUsd(first.min)}</span>
        <span>Employees per salary range</span>
        <span>{formatCompactUsd(last.max)}</span>
      </figcaption>
    </figure>
  );
}
