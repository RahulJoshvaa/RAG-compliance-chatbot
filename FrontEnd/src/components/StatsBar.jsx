import { Timer, Coins, Target, DollarSign } from "lucide-react";

export default function StatsBar({ metrics }) {
  const stats = [
    {
      label: "LATENCY",
      value: metrics ? metrics.latency.toFixed(2) : "—",
      unit: "s",
      Icon: Timer,
    },
    {
      label: "TOKENS / QUERY",
      value: metrics ? (metrics.tokens / 1000).toFixed(2) : "—",
      unit: "K",
      Icon: Coins,
    },
    {
      label: "CONTEXT RELEVANCE",
      value: metrics ? (metrics.relevance * 100).toFixed(1) : "—",
      unit: "%",
      Icon: Target,
    },
    {
      label: "COST / 1K QUERIES",
      value: metrics ? metrics.cost_per_1k.toFixed(2) : "—",
      unit: "$",
      Icon: DollarSign,
    },
  ];

  return (
    <div className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-4 lg:mt-12">
      {stats.map(({ label, value, unit, Icon }) => (
        <div
          key={label}
          className="flex items-center justify-between rounded-2xl bg-white/5 px-6 py-5 ring-1 ring-white/10 backdrop-blur"
        >
          <div>
            <p className="text-xs font-semibold tracking-widest text-slate-400">
              {label}
            </p>
            <p className="mt-2 text-3xl font-extrabold text-brand-300">
              {value}
              <span className="ml-1 text-sm font-medium text-slate-500">
                {unit}
              </span>
            </p>
          </div>
          <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-500/15 text-brand-300">
            <Icon className="h-6 w-6" strokeWidth={1.8} />
          </span>
        </div>
      ))}
    </div>
  );
}
