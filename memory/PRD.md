# Workspace Ruang Sanad — Product Requirements Document

**App**: Notion-style Project Management + Spiritual Tracker + Strategy Execution untuk tim & SPV
**Stack**: React (CRA) + FastAPI + MongoDB
**Language**: Indonesian (Bahasa)
**Brand**: **Workspace Ruang Sanad** — logo: crescent calligraphy + gold accent, tagline "Amal • Kerja • Raport"

## User Personas
- **SPV / Admin**: Approve user baru, atur role & link anggota, monitor deadline & beban kerja, export raport (tim & individu), review keputusan, kelola Strategi & Eksekusi (BSC/OKR/KPI/Action Plan).
- **Anggota**: Isi/update tugas divisi mereka, tracker amaliyah pribadi, tracker rutin pribadi, update aktual KPI mereka, kontribusi KR sebagai owner/supporter OKR.

## Iterasi 9 (Feb 2026) — Strategi & Eksekusi Module

### 1. Menu baru "Strategi & Eksekusi" (SPV-only)
- Route `/strategy`, icon `Target`, nav item baru di antara Monitoring & Manajemen User.
- Hero teal-gradient dengan period selector dropdown + tombol "Periode baru" & "Jadikan aktif".
- 6 tab: **Beranda** (dashboard), **BSC**, **OKR**, **KPI**, **Action Plan**, **Linimasa**.

### 2. Periode dinamis
- CRUD `/api/strategy/periods` — dukung siklus 2/3/6/12 bulan (Siklus/Kuartal/Semester/Tahun) via preset.
- Endpoint `POST /periods/{id}/activate` — only 1 active period at a time.
- Cascade delete: BSC, OKR, KR, KPI, Projects untuk periode itu.

### 3. Balanced Scorecard (BSC)
- 4 aspek: FINANCIAL, CUSTOMER, INTERNAL, LEARNING. Tampilan kartu berwarna per aspek.
- CRUD `/api/strategy/bsc?period_id=` dengan nama/target/achieved.

### 4. OKR (Objectives & Key Results) — dinamis
- Level: COMPANY / DIVISI / INDIVIDU. Tab per-level.
- **Owner (PIC) dinamis**: SPV pilih dari dropdown (nullable → "belum ada owner"). Anggota tanpa OKR tetap bisa jadi **Supporter** (multi via Popover+Checkbox).
- Filter: Semua / Tanpa owner / Per anggota.
- Key Results: inline editable (Input onBlur autosave), progress % = avg (actual/target).
- RBAC: SPV always; owner/supporters bisa update KR (via `user_scope().anggota_id`, not lookup by user_id).

### 5. KPI Dashboard
- Manual entry per periode (SPV) — bobot, target, aktual, polaritas MAX/MIN, optional link ke OKR.
- Formula: MAX → `(aktual/target)*100`, MIN → `(target/aktual)*100`, clamped 200%.
- Weighted score = ach%/100 × bobot. Status: EXCELLENT ≥100, ON_TRACK ≥80, AT_RISK ≥60, else OFF_TRACK.
- Summary per-anggota (grid kartu) + tabel editable (bobot/target/aktual inline).
- RBAC: SPV full CRUD; **anggota bisa update `aktual` saja** pada KPI mereka (fixed via `_my_anggota_id()` helper).

### 6. Action Plan (Proyek Strategis)
- CRUD proyek dengan nama, target_outcome, OMTM, anggaran, divisi, owner, tim.
- **Link ke tasks existing** via multi-select dialog. Progress otomatis dari status task tertaut:
  - `selesai/total × 100` = pct
  - Status: SELESAI (all done), TERLAMBAT (overdue > 0), BERJALAN (has tasks), BELUM_MULAI.
- `start_effective/end_effective` auto-derived dari tasks jika tidak explicit set.

### 7. Linimasa (Gantt-style)
- Peta jadwal proyek berdasarkan `start_effective`→`end_effective`.
- Header bulan otomatis dari range, bar berwarna sesuai status (sky/emerald/red/slate).
- Empty state kalau proyek tidak punya tanggal.

### 8. RBAC Fix
- Helper baru `_my_anggota_id(user)` menggunakan `user_scope()` (baca `user.anggota_id` sesuai auth).
- Sebelumnya, lookup `db.anggota.find_one({user_id: ...})` selalu return None → anggota tidak pernah bisa update aktual KPI/KR. Sekarang berfungsi.
- KPI PUT payload guard tightened: `forbidden = [k for k,v in payload if k!='aktual' and v is not None]` → 403 jika ada field terlarang.

## Architecture

```
/app
├── backend
│   ├── server.py          (register /strategy router)
│   ├── auth.py
│   ├── monitoring.py
│   ├── strategy.py        (NEW — 25+ endpoints for BSC/OKR/KPI/Projects/Dashboard)
│   └── pdf_export.py
└── frontend
    └── src/pages
        ├── Strategy.jsx           (NEW — main page with tabs + period)
        └── strategy/
            ├── PeriodDialog.jsx
            ├── StrategyOverview.jsx
            ├── BscTab.jsx
            ├── OkrTab.jsx
            ├── KpiTab.jsx
            ├── ActionPlanTab.jsx
            └── LinimasaTab.jsx
```

## Testing
- iter7: 13/13 pass (raport digest, per-anggota, monitoring/user)
- iter8: 11/11 pass (rebrand + PDF logo embed)
- iter9: 28/28 pass (Strategy module + RBAC)
- Test files: /app/backend/tests/test_iter7*.py, test_iter8*.py, test_iter9_strategy.py

## Roadmap Backlog
1. **Komitmen** tab — Surat Kesepakatan PDF (generate)
2. **Evaluasi** tab — self-assessment + SPV review per periode
3. **Chart Beban Tim** heatmap divisi × status
4. **Sparkline Individu** — tren task+amaliyah 30-hari di Raport per-anggota
5. **Notifikasi Email approval** (Resend/SendGrid) untuk user baru
6. **Bulk Approve Users** di Manajemen User
7. **Custom SPV Signature** upload untuk PDF raport

## Test Credentials
`/app/memory/test_credentials.md` — SPV: `akunsaktibanget06@gmail.com` / `Qolbu2026!`
