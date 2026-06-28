import {
  Timer,
  ArrowDownToLine,
  ArrowUpFromLine,
  Sigma,
} from "lucide-react";

export default function StatsBar({ metrics }) {
  const cards = [
    {
      title: "LATENCY",
      value: metrics ? metrics.latency.toFixed(2) : "—",
      suffix: "s",
      icon: Timer,
    },
    {
      title: "INPUT TOKENS",
      value: metrics ? metrics.input_tokens : "—",
      suffix: "",
      icon: ArrowDownToLine,
    },
    {
      title: "OUTPUT TOKENS",
      value: metrics ? metrics.output_tokens : "—",
      suffix: "",
      icon: ArrowUpFromLine,
    },
    {
      title: "TOTAL TOKENS",
      value: metrics ? metrics.total_tokens : "—",
      suffix: "",
      icon: Sigma,
    },
  ];

  return (
    <div className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4 lg:mt-12">
      {cards.map((card, index) => {
        const Icon = card.icon;

        return (
          <div
            key={index}
            className="flex items-center justify-between rounded-2xl bg-white/5 px-6 py-5 ring-1 ring-white/10 backdrop-blur"
          >
            <div>
              <p className="text-xs font-semibold tracking-widest text-slate-400">
                {card.title}
              </p>

              <p className="mt-2 text-3xl font-extrabold text-brand-300">
                {card.value}
                {card.suffix && (
                  <span className="ml-1 text-sm font-medium text-slate-500">
                    {card.suffix}
                  </span>
                )}
              </p>
            </div>

            <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-brand-500/15 text-brand-300">
              <Icon className="h-6 w-6" strokeWidth={1.8} />
            </span>
          </div>
        );
      })}
    </div>
  );
}