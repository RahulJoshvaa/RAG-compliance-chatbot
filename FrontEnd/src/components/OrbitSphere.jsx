const RING_AVATARS = [
  { seed: "Milo", top: "0%", left: "50%" },
  { seed: "Zoe", top: "18%", left: "92%" },
  { seed: "Felix", top: "70%", left: "96%" },
  { seed: "Aria", top: "96%", left: "55%" },
  { seed: "Leo", top: "60%", left: "4%" },
  { seed: "Nova", top: "14%", left: "8%" },
];

export default function OrbitSphere() {
  return (
    <div className="absolute inset-0 flex items-center justify-center">
      {/* Concentric guide rings */}
      <div className="absolute h-[440px] w-[440px] rounded-full border border-brand-400/20" />
      <div className="absolute h-[340px] w-[340px] rounded-full border border-brand-400/25" />
      <div className="absolute h-[250px] w-[250px] rounded-full border border-brand-400/20" />

      {/* Outer rotating ring with avatars */}
      <div className="animate-orbit absolute h-[440px] w-[440px]">
        {RING_AVATARS.map((a) => (
          <div
            key={a.seed}
            className="absolute -translate-x-1/2 -translate-y-1/2"
            style={{ top: a.top, left: a.left }}
          >
            <div className="animate-orbit-counter">
              <img
                src={`https://api.dicebear.com/9.x/avataaars/svg?seed=${a.seed}&backgroundColor=22d3ee,3b82f6,67e8f9`}
                alt="avatar"
                className="h-10 w-10 rounded-full border-2 border-white/80 bg-white shadow-lg"
              />
            </div>
          </div>
        ))}
      </div>

      {/* The glass gradient orb */}
      <div className="animate-float relative h-56 w-56 sm:h-64 sm:w-64">
        <div className="absolute inset-0 rounded-full bg-gradient-to-br from-brand-300 via-accent to-accent-deep shadow-[0_25px_60px_-15px_rgba(34,211,238,0.55)]" />
        {/* Glass highlights */}
        <div className="absolute left-[18%] top-[14%] h-20 w-20 rounded-full bg-white/40 blur-xl" />
        <div className="absolute right-[16%] top-[20%] h-10 w-10 rounded-full bg-white/60 blur-md" />
        <div className="absolute inset-0 rounded-full bg-gradient-to-t from-black/20 to-transparent ring-1 ring-white/30" />
        {/* Reflection beneath */}
        <div className="absolute -bottom-10 left-1/2 h-10 w-40 -translate-x-1/2 rounded-full bg-brand-400/30 blur-2xl" />
      </div>
    </div>
  );
}
