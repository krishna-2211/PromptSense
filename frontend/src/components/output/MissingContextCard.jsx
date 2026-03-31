function MissingContextCard({ missingPieces }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md space-y-3">
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
              className="rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700"
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
