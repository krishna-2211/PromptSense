function MissingContextCard({ missingPieces }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-800 mb-3">
        What Was Missing
      </h2>
      {missingPieces.length === 0 ? (
        <p className="text-sm text-slate-600">
          No major missing pieces were detected.
        </p>
      ) : (
        <ul className="list-disc pl-5 space-y-1 text-sm text-slate-700">
          {missingPieces.map((piece) => (
            <li key={piece}>{piece}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default MissingContextCard;
