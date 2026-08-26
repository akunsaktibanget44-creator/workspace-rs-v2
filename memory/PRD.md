# Qolbu Manage — Product Requirements Document

**App**: Notion-style Project Management + Spiritual Tracker for team & SPV
**Stack**: React (CRA) + FastAPI + MongoDB
**Language**: Indonesian (Bahasa)
**Theme**: Nabawi dome green + modern touch

## Original Problem Statement
Web aplikasi Project Management dan Spiritual Tracker untuk tim dan SPV — task management (kanban+table, deadlines, presets), spiritual tracker (dynamic amaliyah), MongoDB, Notion-style layout.

## User Personas
- **SPV / Admin**: Approve user baru, atur role & link anggota, monitor deadline & beban kerja tim, export raport, review keputusan.
- **Anggota**: Isi/update tugas divisi mereka, tracker amaliyah pribadi, tracker rutin pribadi.

## Role Visibility Matrix (Iteration 5)
| Menu / Endpoint | SPV | Anggota (approved + linked) |
|---|---|---|
| Beranda | Data global | Data hanya divisi mereka |
| Tugas | Semua divisi | Hanya divisi mereka |
| Tugas Rutin Tracker | Semua | Hanya milik mereka |
| Spiritual Tracker | Semua | Hanya milik mereka (per-user entries) |
| Raport | ✅ menu + PDF | ❌ hidden |
| Monitoring SPV | ✅ | ❌ 403 |
| Manajemen User | ✅ | ❌ 403 |
| Global Search | Semua workspace | Scoped ke divisi mereka |

## Iteration Log

### Iterations 1–3 (Historical)
- Base MVP + Notion layout, Kanban+Table, dynamic status, divisi, unread badges, cross-move, inline CRUD, filter presets, member analytics, merged Amaliyah config into Spiritual.

### Iteration 4 (Feb 2026 — Auth & Monitoring)
- Auth lengkap (email/password + Google Emergent), pending approval, role management, User mgmt menu.
- Monitoring SPV 5-tab (Deadline Radar, Beban Kerja, Kepatuhan Amaliyah, Task Stagnan, Progres Divisi).
- Beranda mini overview cards (Hari Ini, Streak Amaliyah, Pemindahan Baru).
- Export Raport PDF (reportlab).
- Import Excel button hidden.

### Iteration 6 (Feb 2026 — Badges + Weekly Per-Month + Amaliyah UX)
- **Badges & Streak** — `GET /api/amaliyah/streak` per-user (current & longest streak, badges 7/14/30/60/100/180/365 hari, next target). Frontend 4-kartu scoreboard (Progress, Streak, Rekor, Lencana) + strip lencana gradient.
- **Mingguan per-bulan** — Tugas Rutin Mingguan sekarang tampilkan hanya pekan-pekan ISO yang irisan dengan bulan aktif (biasanya 4-6 pekan). Header "Pekan di bulan X" + sub-label "Pekan 1..N".
- **Spiritual UI overhaul** — Kolom nomor dinamis, checkbox select-all + bulk toolbar (SPV), drag-drop reorder via `@dnd-kit/sortable`, inline edit expanded, mini progress bar per baris. Anggota read-only untuk kelola amaliyah.
- **New APIs**: `POST /api/amaliyah/items/reorder`, `POST /api/amaliyah/items/bulk_delete`, `GET /api/amaliyah/streak` — all scoped.

## Iteration 5 (Feb 2026 — Multi-user Scoping)
- **Backend middleware** locks ALL `/api/*` routes (except `/api/auth/register|login|google|me|logout`).
- **Amaliyah per user** — `AmaliyahEntry.user_id` added; each user sees/updates only their own entries. Startup migration backfills existing entries to seeded SPV.
- **Tugas & Divisi visibility** — Anggota sees only their linked divisi (via `user.anggota_id → anggota.divisi_id`). SPV sees all.
- **Task mutation ownership guard** — `_assert_task_access` blocks anggota from PUT/DELETE/archive/move on tasks outside their divisi (403). `bulk_move` cross-divisi is SPV-only.
- **Analytics scoping** — `/api/anggota/analytics` returns 403 to anggota querying another divisi.
- **Raport visibility** — Menu hidden for anggota + route now `requireSpv` in App.js. Backend still returns scoped data if called by anggota (used by Beranda's combined score).
- **User → Anggota linking** — Manajemen User has "Link Anggota (Tim)" dropdown grouped by divisi.
- **Global Search** in sidebar — `GET /api/search?q=` returns scoped tasks/amaliyah/anggota/divisi in a live dropdown.
- **SPV-only CUD** — Anggota, Divisi, Amaliyah items, Raport note, Import Excel are SPV-only.

## Architecture

```
/app
├── backend
│   ├── server.py              (routes, auth middleware, user_scope helper, search endpoint)
│   ├── auth.py                (register/login/google/me/logout, users CRUD, session cookie, seed_admin)
│   ├── monitoring.py          (deadline-radar, workload, compliance, stagnant, div-progress — SPV-only)
│   ├── pdf_export.py          (reportlab raport PDF)
│   └── tests/                 (pytest — 20/20 iter4)
└── frontend
    ├── src/App.js             (routes + ProtectedRoute + AuthCallback)
    ├── src/lib
    │   ├── api.js             (axios withCredentials + search helper)
    │   ├── AuthContext.jsx
    │   └── ProtectedRoute.jsx
    ├── src/layouts/AppShell.jsx (SPV/anggota nav + user block + GlobalSearch)
    ├── src/components/GlobalSearch.jsx (NEW)
    └── src/pages
        ├── Dashboard.jsx      (mini overview cards)
        ├── Tasks.jsx          (Import Excel hidden)
        ├── Spiritual.jsx      (scoped per-user via backend)
        ├── Raport.jsx         (SPV only + PDF export)
        ├── Monitoring.jsx     (SPV only)
        ├── UsersManagement.jsx (SPV only + anggota link dropdown)
        └── auth/              (Login, Register, AuthCallback, Pending)
```

## Key API Endpoints
- Auth: `/api/auth/register|login|google/session|me|logout|users`
- Data: `/api/tasks*, /api/divisi*, /api/anggota*, /api/task_lists*, /api/task_labels*, /api/amaliyah/*, /api/todo/entries, /api/raport/summary, /api/raport/export.pdf, /api/raport/note`
- Monitoring (SPV): `/api/monitoring/deadline-radar|workload|amaliyah-compliance|stagnant-tasks|division-progress`
- Search: `GET /api/search?q=<query>`
- Import (SPV): `POST /api/import/excel` — button hidden in UI

## Roadmap / Backlog
1. **Notifikasi Approval** — Kirim email ke user saat SPV approve (Resend/SendGrid).
2. **Reminder Deadline Harian** — Digest email tugas overdue & hari ini setiap pagi.
3. **Badge & Streak Anggota** — Beranda anggota tampilkan streak amaliyah pribadi + achievement.
4. **Raport per-Anggota PDF** — Export raport individu, bukan hanya tim.
5. **Bulk Approve Users** di Manajemen User.
6. **Rate limit** untuk `/api/auth/register` supaya tidak spam.
7. **Task assignment notification** — Notifikasi in-app saat anggota di-assign task baru.

## Test Credentials
`/app/memory/test_credentials.md` — SPV: `akunsaktibanget06@gmail.com` / `Qolbu2026!`
