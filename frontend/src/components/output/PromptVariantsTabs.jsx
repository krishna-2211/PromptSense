import { useState } from "react";

function PromptVariantsTabs({ variants }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!variants || variants.length === 0) return null;

  return (
    <div className="rounded-[24px] border border-white/60 bg-white/90 p-5 shadow-[0_12px_40px_rgba(15,23,42,0.06)] transition hover:-translate-y-0.5 hover:shadow-[0_18px_45px_rgba(168,85,247,0.14)] space-y-4">
      <h2 className="text-lg font-semibold text-slate-800">Prompt Variants</h2>

      <div className="flex flex-wrap gap-2">
        {variants.map((variant, index) => (
          <button
            key={variant.label}
            onClick={() => setActiveTab(index)}
            className={`rounded-full px-3 py-1 text-sm font-medium transition ${
              activeTab === index
                ? "bg-gradient-to-r from-indigo-600 to-fuchsia-600 text-white shadow-md"
                : "bg-slate-100 text-slate-700 hover:bg-slate-200"
            }`}
          >
            {variant.label}
          </button>
        ))}
      </div>

      <div className="rounded-2xl border border-slate-200/70 bg-gradient-to-br from-slate-50 to-white p-4 text-sm whitespace-pre-wrap leading-7 text-slate-700">
        {variants[activeTab].prompt}
      </div>
    </div>
  );
}

export default PromptVariantsTabs;
