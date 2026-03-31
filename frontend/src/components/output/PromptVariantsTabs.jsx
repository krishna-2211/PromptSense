import { useState } from "react";

function PromptVariantsTabs({ variants }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!variants || variants.length === 0) return null;

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md space-y-4">
      <h2 className="text-lg font-semibold text-slate-800">Prompt Variants</h2>

      <div className="flex flex-wrap gap-2">
        {variants.map((variant, index) => (
          <button
            key={variant.label}
            onClick={() => setActiveTab(index)}
            className={`rounded-full px-3 py-1 text-sm font-medium transition ${
              activeTab === index
                ? "bg-indigo-600 text-white"
                : "bg-slate-100 text-slate-700 hover:bg-slate-200"
            }`}
          >
            {variant.label}
          </button>
        ))}
      </div>

      <div className="rounded-xl bg-slate-50 p-4 text-sm whitespace-pre-wrap leading-6 text-slate-700">
        {variants[activeTab].prompt}
      </div>
    </div>
  );
}

export default PromptVariantsTabs;
