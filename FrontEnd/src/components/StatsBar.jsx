import { Timer } from "lucide-react";

export default function StatsBar({ metrics }) {
  return (
    <div className="mt-10 grid grid-cols-1 lg:mt-12">
      <div className="flex items-center justify-between rounded-2xl bg-white/5 px-6 py-5 ring-1 ring-white/10 backdrop-blur">
        <div>
          <p className="text-xs font-semibold tracking-widest text-slate-400">
            LATENCY
          </p>
          <p className="mt-2 text-3xl font-extrabold text-brand-300">
            {metrics ? metrics.latency.toFixed(2) : "—"}
            <span className="ml-1 text-sm font-medium text-slate-500">
              s
            </span>
          </p>
        </div>

        <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-500/15 text-brand-300">
          <Timer className="h-6 w-6" strokeWidth={1.8} />
        </span>
      </div>
    </div>
  );
}