import { InsightsDashboard } from "@/components/InsightsDashboard";

export default function InsightsPage() {
  return (
    <>
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Pay insights</h1>
        <p className="text-sm text-muted-foreground">
          How ACME pays people, compared in one currency at fixed demo exchange
          rates.
        </p>
      </div>
      <InsightsDashboard />
    </>
  );
}
