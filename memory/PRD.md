# Sanad (formerly Qolbu Manage) — Product Requirements Document

**App**: Notion-style Project Management + Spiritual Tracker for team & SPV
**Stack**: React (CRA) + FastAPI + MongoDB
**Language**: Indonesian (Bahasa)
**Theme**: Nabawi dome green + modern touch
**Brand**: **Sanad** (Arab: sandaran/tumpuan) — logo: crescent-in-shield with gold dot

## Original Problem Statement
Web aplikasi Project Management dan Spiritual Tracker untuk tim dan SPV — task management (kanban+table, deadlines, presets), spiritual tracker (dynamic amaliyah), MongoDB, Notion-style layout.

## User Personas
- **SPV / Admin**: Approve user baru, atur role & link anggota, monitor deadline & beban kerja, export raport (tim & individu), review keputusan.
- **Anggota**: Isi/update tugas divisi mereka, tracker amaliyah pribadi, tracker rutin pribadi.

## Iteration 7 (Feb 2026 — Rebrand + Per-Anggota Monitoring/Raport + Digest)

### 1. Rebrand → **Sanad**
- Nama app "Qolbu Manage" diganti jadi "Sanad" di seluruh UI (AppShell sidebar & mobile header, Login, Register, HTML title).
- Custom SVG logo `SanadLogo.jsx` (crescent-in-shield + gold accent dot) menggantikan icon Moon lucide.
- PDF header, footer, brand string updated ke "Sanad · Amal • Kerja • Raport".
- Backend API title & version bumped: "Sanad API" v1.1.

### 2. Monitoring SPV — Per-Anggota Tab (Baru)
- Tab baru **"Per Anggota"** di halaman Monitoring dengan dropdown Divisi → Anggota.
- Endpoint baru: `GET /api/monitoring/user/{anggota_id}?days=7` returns combined data:
  - `deadline`: overdue/today/upcoming lists + summary
  - `workload`: aktif/selesai/proses/kendala/belum/pct
  - `stagnant`: task tanpa update >3 hari
  - `amaliyah`: per-item compliance 7 hari (jika anggota di-link ke user login)
- Hero card individu: avatar+nama+divisi + 4 mini-stat + progress bar.
- Deadline radar per-individu (3 kolom overdue/today/upcoming) dengan action buttons.

### 3. Action Buttons pada Deadline Radar
- Setiap TaskCard yang kena radar deadline sekarang punya keterangan (⚠ "Terkena radar OVERDUE — deadline terlewat", dst.) dan 3 tombol aksi:
  - **Selesai** → `PUT /api/tasks/{id}` status=SELESAI
  - **+3 hari** → bump deadline
  - **+7 hari** → bump deadline
- Auto-refresh after action (reload data via `onAction` callback).

### 4. Raport Per-Anggota + Filter + PDF Baru
- Halaman Raport tambah filter **Divisi** & **Anggota** (cascading: pilih divisi → filter anggota list).
- Preset periode: `7 hari`, `Bulan ini`, `30 hari`, `90 hari` (button one-tap).
- `GET /api/raport/summary?anggota_id=X&start=&end=` returns per-anggota metrics (task filtered by penerima_tugas_id, amaliyah scoped ke user_id anggota jika linked, tasks_list included untuk PDF).
- `GET /api/raport/export.pdf?anggota_id=X&start=&end=` export PDF individu.
- `PUT /api/raport/note?anggota_id=X` — SPV note per-anggota (kunci `id=anggota:{aid}`), tetap kompatibel dengan raport tim (`id=singleton`).
- **PDF layout diperbaiki**:
  - Logo Sanad (drawn via reportlab Flowable) + brand block header dengan periode di kanan
  - Score hero card 2 kolom (skor gabungan + rekomendasi otomatis dengan color coding)
  - Task breakdown 6-cell metric grid + progress bar visual
  - Amaliyah breakdown 5-cell + progress bar
  - **Daftar Tugas** (tabel) untuk PDF per-anggota (max 60 rows, header emerald, alternating row bg)
  - Note SPV dengan color-coded keputusan
  - Signature block + auto footer (halaman & brand)

### 5. Deadline Digest di Beranda (SPV-only)
- Widget baru `<DeadlineDigest />` di halaman Beranda untuk SPV.
- Endpoint baru: `GET /api/dashboard/digest` returns overdue + today + upcoming (≤3 hari) + stagnant (>3 hari), scoped per role.
- Tampilan: 4 chip counters + 2 kolom (Butuh Aksi Sekarang / Perhatian Berikutnya) dengan max 3-4 item; klik → navigasi ke Tasks.
- Kalau kosong: "Alhamdulillah, tidak ada task yang butuh perhatian."

## Architecture

```
/app
├── backend
│   ├── server.py          (+ dashboard/digest, raport per-anggota, timedelta import)
│   ├── auth.py
│   ├── monitoring.py      (+ /monitoring/user/{anggota_id})
│   └── pdf_export.py      (redesign: SanadLogo Flowable, per-anggota, tasks_list table)
└── frontend
    ├── src/App.js
    ├── src/lib/api.js     (+ monitoringUser, dashboardDigest, raportExportPdfUrl(anggota_id))
    ├── src/components/SanadLogo.jsx (NEW)
    ├── src/layouts/AppShell.jsx (rebrand)
    └── src/pages
        ├── Dashboard.jsx  (+ DeadlineDigest widget SPV)
        ├── Raport.jsx     (filter divisi/anggota + presets + PDF per-anggota)
        └── Monitoring.jsx (+ Per Anggota tab + action buttons)
```

## Key API Endpoints (Delta Iter 7)
- **New**: `GET /api/monitoring/user/{anggota_id}?days=7`
- **New**: `GET /api/dashboard/digest`
- **Updated**: `GET /api/raport/summary?anggota_id=&start=&end=`
- **Updated**: `GET /api/raport/export.pdf?anggota_id=&start=&end=`
- **Updated**: `PUT /api/raport/note?anggota_id=` (per-anggota note stored with `id=anggota:{aid}`)

## Roadmap / Backlog (post iter-7)
1. **Notifikasi Approval Email** — Resend/SendGrid on user approve
2. **Reminder Deadline Digest via Email** — daily digest email untuk SPV
3. **Bulk Approve Users** di Manajemen User
4. **Rate limit** `/api/auth/register` (anti-spam)
5. **Task assignment notification** in-app
6. **Chart Raport per-anggota** (recharts sparkline task/amaliyah 30 hari)

## Test Credentials
`/app/memory/test_credentials.md` — SPV: `akunsaktibanget06@gmail.com` / `Qolbu2026!`
