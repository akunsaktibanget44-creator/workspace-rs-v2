import { useEffect, useState } from "react";
import { strategyDashboard } from "@/lib/api";
import { Landmark, Compass, Gauge, Rocket, CheckCircle2, AlertTriangle } from "lucide-react";

function Metric({ icon: Icon, label, value, sub, tone = "emerald", testId }) {
  const tones = {
    emerald: "border-emerald-200 bg-emerald-50/50 text-emerald-900",
    gold: "border-amber-200 bg-amber-50/50 text-amber-900",
    red: "border-red-200 bg-red-50/50 text-red-900",
    slate: "border-slate-200 bg-slate-50/50 text-slate-900",
  };
  return (
    <div data-testid={testId} className={`rounded-xl border p-4 ${tones[tone]}`}>
      <div className="flex items-center justify-between">
        <p className="text-[10px] font-semibold uppercase tracking-wider opacity-70">{label}</p>
        <Icon size={16} />
      </div>
      <p className="font-display mt-1 text-3xl font-bold">{value}</p>
      {sub && <p className="mt-1 text-xs opacity-70">{sub}</p>}
    </div>
  );
}

export default function StrategyOverview({ periodId, period }) {
  const [data, setData] = useState(null);
  useEffect(() => {
    if (!periodId) return;
    strategyDashboard(periodId).then(setData).catch(() => setData({}));
  }, [periodId]);

  if (!periodId) return null;

  const d = data || {};
  return (
    <div className="space-y-4">
      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
        <Metric icon={Landmark} label="BSC Target" value={d.bsc_count || 0} sub="Balanced Scorecard items" testId="ov-bsc" />
        <Metric icon={Compass} label="OKR Objectives" value={d.okr_count || 0} sub={`Rata2 progres ${d.okr_avg_progress || 0}%`} tone="gold" testId="ov-okr" />
        <Metric icon={Gauge} label="KPI Items" value={d.kpi_count || 0} sub={`Skor tim ${d.kpi_final_score || 0} / ${d.kpi_total_bobot || 0}`} testId="ov-kpi" />
        <Metric icon={Rocket} label="Proyek Strategis" value={d.project_count || 0} sub={`${d.project_selesai || 0} selesai · ${d.project_terlambat || 0} terlambat`} tone={d.project_terlambat > 0 ? "red" : "emerald"} testId="ov-projects" />
      </div>

      <div className="rounded-2xl border border-emerald-100 bg-white p-6">
        <p className="text-xs font-semibold uppercase tracking-wider text-emerald-800/70">Panduan Cepat</p>
        <ol className="mt-3 space-y-2 text-sm text-emerald-950">
          <li className="flex items-start gap-2"><CheckCircle2 size={16} className="mt-0.5 shrink-0 text-emerald-600" /> Mulai dari <b>BSC</b> — tentukan target tahunan 4 aspek (Financial, Customer, Internal Process, Learning &amp; Growth).</li>
          <li className="flex items-start gap-2"><CheckCircle2 size={16} className="mt-0.5 shrink-0 text-emerald-600" /> Lanjut ke <b>OKR</b> — buat Objective per level (Company/Divisi/Individu). SPV yang menentukan <b>Owner</b> anggota via dropdown; sisanya tanpa OKR.</li>
          <li className="flex items-start gap-2"><CheckCircle2 size={16} className="mt-0.5 shrink-0 text-emerald-600" /> Tambahkan <b>KPI</b> per anggota — atur bobot, target, dan hubungkan ke OKR.</li>
          <li className="flex items-start gap-2"><CheckCircle2 size={16} className="mt-0.5 shrink-0 text-emerald-600" /> Buat <b>Action Plan</b> — proyek strategis yang <i>terhubung</i> ke Tugas di menu Tugas (progress otomatis dari status task).</li>
          <li className="flex items-start gap-2"><AlertTriangle size={16} className="mt-0.5 shrink-0 text-amber-600" /> Cek <b>Linimasa</b> untuk melihat tumpang tindih jadwal antar proyek.</li>
        </ol>
        {period && (
          <p className="mt-4 rounded-lg bg-emerald-50 p-3 text-xs text-emerald-900">
            Periode aktif: <b>{period.nama}</b> · {period.start} → {period.end} · siklus tiap {period.siklus_bulan} bulan.
          </p>
        )}
      </div>
    </div>
  );
}
