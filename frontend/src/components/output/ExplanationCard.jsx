function ExplanationCard({ explanation, promptType }) {
  const formattedType = promptType
    ? promptType
        .replaceAll("_", " ")
        .replace(/\b\w/g, (char) => char.toUpperCase())
    : "Unknown";

  return (
    <div className="rounded-[24px] border border-white/60 bg-white/90 p-5 shadow-[0_12px_40px_rgba(15,23,42,0.06)] transition hover:-translate-y-0.5 hover:shadow-[0_18px_45px_rgba(99,102,241,0.14)] space-y-3">
      <div>
        <h2 className="text-lg font-semibold text-slate-800">Why This Works</h2>
        <p className="mt-1 inline-flex rounded-full bg-slate-100 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-500">
          {formattedType}
        </p>
      </div>

      <p className="text-sm leading-6 text-slate-700">{explanation}</p>
    </div>
  );
}

export default ExplanationCard;
