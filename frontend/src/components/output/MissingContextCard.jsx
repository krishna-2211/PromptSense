function MissingContextCard({ missingPieces }) {
  return (
    <div className="rounded-[24px] border border-white/60 bg-white/90 p-5 shadow-[0_12px_40px_rgba(15,23,42,0.06)] transition hover:-translate-y-0.5 hover:shadow-[0_18px_45px_rgba(251,191,36,0.15)] space-y-3">
      <h2 className="text-lg font-semibold text-slate-800">Missing Context</h2>

      {missingPieces.length === 0 ? (
        <p className="text-sm text-slate-600">
          No major missing pieces were detected.
        </p>
      ) : (
        <div className="flex flex-wrap gap-2">
          {missingPieces.map((piece) => (
            <span
              key={piece}
              className="rounded-full bg-gradient-to-r from-amber-50 to-orange-50 px-3 py-1.5 text-xs font-semibold text-amber-700 ring-1 ring-amber-100"
            >
              {piece}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

export default MissingContextCard;
