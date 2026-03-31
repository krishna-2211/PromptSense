import { useState } from "react";
import PromptInputBox from "../components/input/PromptInputBox";
import ImprovedPromptCard from "../components/output/ImprovedPromptCard";
import MissingContextCard from "../components/output/MissingContextCard";
import ExplanationCard from "../components/output/ExplanationCard";
import PromptVariantsTabs from "../components/output/PromptVariantsTabs";
import { improvePrompt, uploadFile } from "../services/api";

function WorkspacePage() {
  const [prompt, setPrompt] = useState("");
  const [audience, setAudience] = useState("general");
  const [outputStyle, setOutputStyle] = useState("structured");
  const [additionalContext, setAdditionalContext] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFileId, setUploadedFileId] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState("");
  const [webUrl, setWebUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleImprove = async () => {
    setError("");
    setLoading(true);
    setResult(null);

    try {
      let fileId = uploadedFileId;

      if (selectedFile && !fileId) {
        const uploadResult = await uploadFile(selectedFile);
        fileId = uploadResult.file_id;
        setUploadedFileId(fileId);
        setUploadedFilename(uploadResult.filename);
      }

      const data = await improvePrompt({
        original_prompt: prompt,
        audience,
        output_style: outputStyle,
        additional_context: additionalContext || null,
        file_context: null,
        file_id: fileId,
        web_url: webUrl || null,
      });

      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const usedSources = result?.used_context_sources || [];

  return (
    <div className="relative min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(99,102,241,0.18),_transparent_30%),radial-gradient(circle_at_top_right,_rgba(236,72,153,0.14),_transparent_28%),linear-gradient(to_bottom_right,#f8fafc,#eef2ff,#fdf2f8)] px-6 py-10">
      <div className="pointer-events-none absolute left-10 top-10 h-40 w-40 rounded-full bg-indigo-300/20 blur-3xl" />
      <div className="pointer-events-none absolute right-10 top-20 h-40 w-40 rounded-full bg-fuchsia-300/20 blur-3xl" />

      <div className="mx-auto max-w-7xl space-y-8">
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 rounded-full border border-white/60 bg-white/70 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.22em] text-indigo-700 shadow-sm backdrop-blur">
            ✨ LLM Instruction Optimizer
          </div>

          <div className="space-y-3">
            <h1 className="text-5xl font-black tracking-tight text-slate-900 sm:text-6xl">
              PromptSense
            </h1>
            <p className="max-w-2xl text-lg leading-8 text-slate-600">
              Turn vague ideas into high-performing prompts with hybrid
              intelligence, context-aware refinement, and polished LLM-ready
              instructions.
            </p>
          </div>

          <div className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-indigo-500 to-fuchsia-500 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-indigo-200">
            ⚡ Hybrid Intelligence Enabled
          </div>
        </div>

        <div className="grid gap-8 lg:grid-cols-[1.05fr_1fr]">
          <div className="space-y-5 rounded-[28px] border border-white/60 bg-white/80 p-6 shadow-[0_10px_40px_rgba(99,102,241,0.10)] backdrop-blur">
            <div className="space-y-1">
              <h2 className="text-lg font-semibold text-slate-800">
                Your Prompt
              </h2>
              <p className="text-sm text-slate-500">
                Describe what you want the LLM to do, even if it’s vague.
              </p>
            </div>

            <PromptInputBox
              value={prompt}
              onChange={setPrompt}
              onKeyDown={(e) => {
                if (
                  e.ctrlKey &&
                  e.key === "Enter" &&
                  prompt.trim() &&
                  !loading
                ) {
                  handleImprove();
                }
              }}
            />

            <div className="space-y-2">
              <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                Try a sample
              </p>
              <div className="flex flex-wrap gap-2">
                {[
                  "Write a professional email to recruiter",
                  "Summarize this report",
                  "Explain machine learning simply",
                  "Create a 7-day study plan",
                ].map((sample) => (
                  <button
                    key={sample}
                    type="button"
                    onClick={() => setPrompt(sample)}
                    className="rounded-full border border-white/70 bg-white/70 px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm backdrop-blur transition hover:-translate-y-0.5 hover:bg-white hover:shadow-md"
                  >
                    {sample}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">
                  Audience
                </label>
                <select
                  value={audience}
                  onChange={(e) => setAudience(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 bg-white p-3 text-sm shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300"
                >
                  <option value="technical">Technical</option>
                  <option value="general">General</option>
                  <option value="beginner">Beginner</option>
                  <option value="executive">Executive</option>
                  <option value="professional">Professional</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">
                  Output Style
                </label>
                <select
                  value={outputStyle}
                  onChange={(e) => setOutputStyle(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 bg-white p-3 text-sm shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300"
                >
                  <option value="structured">Structured</option>
                  <option value="concise">Concise</option>
                  <option value="detailed">Detailed</option>
                  <option value="professional">Professional</option>
                </select>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">
                Additional Context
              </label>
              <textarea
                value={additionalContext}
                onChange={(e) => setAdditionalContext(e.target.value)}
                placeholder="Optional: add details that help the system understand your intent"
                className="w-full min-h-28 rounded-2xl border border-slate-300 p-4 text-sm shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300"
              />
            </div>

            <div className="grid gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">
                  Upload File (optional)
                </label>
                <input
                  type="file"
                  onChange={(e) => {
                    const file = e.target.files?.[0] || null;
                    setSelectedFile(file);
                    setUploadedFileId(null);
                    setUploadedFilename(file?.name || "");
                  }}
                  className="w-full rounded-xl border border-slate-300 bg-white p-3 text-sm shadow-sm transition file:mr-4 file:rounded-full file:border-0 file:bg-indigo-50 file:px-3 file:py-1.5 file:text-xs file:font-semibold file:text-indigo-700 hover:file:bg-indigo-100"
                />
                {uploadedFilename && (
                  <p className="text-xs text-slate-500">
                    Selected file: <span className="font-medium">{uploadedFilename}</span>
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">
                  Web URL (optional)
                </label>
                <input
                  type="url"
                  value={webUrl}
                  onChange={(e) => setWebUrl(e.target.value)}
                  placeholder="https://example.com/article-or-job-post"
                  className="w-full rounded-xl border border-slate-300 bg-white p-3 text-sm shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300"
                />
              </div>
            </div>

            <button
              onClick={handleImprove}
              disabled={loading || !prompt.trim()}
              className="flex w-full items-center justify-center rounded-2xl bg-gradient-to-r from-indigo-600 via-violet-600 to-fuchsia-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-200 transition hover:scale-[1.01] hover:shadow-xl active:scale-[0.99] disabled:cursor-not-allowed disabled:from-slate-400 disabled:to-slate-400"
            >
              {loading ? "Thinking..." : "Improve Prompt"}
            </button>

            <p className="text-center text-xs text-slate-400">
              Press Ctrl + Enter to improve
            </p>

            {error && (
              <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                {error}
              </div>
            )}
          </div>

          <div className="space-y-5">
            {result ? (
              <>
                {usedSources.length > 0 && (
                  <div className="rounded-[24px] border border-white/60 bg-white/90 p-4 shadow-[0_12px_40px_rgba(15,23,42,0.06)] backdrop-blur">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">
                        Context Used
                      </span>

                      {usedSources.includes("file") && (
                        <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700 ring-1 ring-indigo-100">
                          📄 File Context
                        </span>
                      )}

                      {usedSources.includes("web") && (
                        <span className="rounded-full bg-fuchsia-50 px-3 py-1 text-xs font-semibold text-fuchsia-700 ring-1 ring-fuchsia-100">
                          🌐 Web Context
                        </span>
                      )}
                    </div>
                  </div>
                )}

                <ImprovedPromptCard
                  improvedPrompt={result.improved_prompt}
                  confidenceScore={result.confidence_score}
                  reasoningMode={result.reasoning_mode}
                />

                <MissingContextCard missingPieces={result.missing_pieces} />

                <ExplanationCard
                  explanation={result.explanation}
                  promptType={result.prompt_type}
                />

                <div className="rounded-[24px] border border-white/60 bg-white/90 p-5 shadow-[0_12px_40px_rgba(15,23,42,0.06)] transition hover:-translate-y-0.5 hover:shadow-[0_18px_45px_rgba(99,102,241,0.14)] space-y-3">
                  <h2 className="text-lg font-semibold text-slate-800">
                    Expected Output Preview
                  </h2>
                  <div className="rounded-2xl border border-slate-200/70 bg-gradient-to-br from-slate-50 to-white p-4 text-sm whitespace-pre-wrap leading-7 text-slate-700">
                    {result.expected_output_preview}
                  </div>
                </div>

                <PromptVariantsTabs variants={result.variants} />
              </>
            ) : (
              <div className="rounded-[28px] border border-dashed border-white/70 bg-white/70 p-10 text-center shadow-[0_12px_40px_rgba(15,23,42,0.05)] backdrop-blur">
                <div className="mx-auto max-w-md space-y-4">
                  <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-fuchsia-500 text-3xl text-white shadow-lg shadow-indigo-200">
                    ✨
                  </div>
                  <h3 className="text-xl font-semibold text-slate-800">
                    Optimized output will appear here
                  </h3>
                  <p className="text-sm leading-6 text-slate-500">
                    Enter a rough idea on the left and let PromptSense transform
                    it into a stronger, more precise instruction for any LLM.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default WorkspacePage;