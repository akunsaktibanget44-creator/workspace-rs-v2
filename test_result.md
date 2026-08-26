#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================
# (Preserved.)
#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

user_problem_statement: |
  Iterasi 9 — Tambahkan menu SPV baru "Strategi & Eksekusi" (referensi: Strategi Eksekusi tool):
  Balanced Scorecard, OKR, KPI, Action Plan, Linimasa. Terintegrasi dengan fitur existing.
  Requirements khusus (dari user):
    - Scope MVP: BSC + OKR + KPI + Action Plan + Linimasa (Komitmen/Evaluasi menyusul)
    - OKR: 1 owner (PIC) + multi supporter. SPV dinamis assign owner via dropdown; anggota tanpa OKR tetap bisa jadi supporter.
    - KPI: input manual per periode oleh SPV (anggota hanya bisa update 'aktual').
    - Action Plan: proyek TERHUBUNG ke tasks existing (progress auto dari status task).
    - Periode dinamis: siklus 2-bulanan / kuartal 3-bulanan / semester / tahunan.
  UI/UX user-friendly + mobile-friendly.

backend:
  - task: "Strategy periods CRUD + activate"
    implemented: true
    working: true
    file: "backend/strategy.py, backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Endpoints: GET/POST /strategy/periods, GET /strategy/periods/active, PUT/DELETE /strategy/periods/{id}, POST /strategy/periods/{id}/activate. Cascade delete BSC/OKR/KRs/KPI/Projects. Verified via curl: create Q1 2026, active toggle works."

  - task: "BSC CRUD (Balanced Scorecard)"
    implemented: true
    working: true
    file: "backend/strategy.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "GET/POST /strategy/bsc (?period_id=), PUT/DELETE /strategy/bsc/{id}. 4 aspek: FINANCIAL/CUSTOMER/INTERNAL/LEARNING. Verified create with target/achieved."

  - task: "OKR CRUD + Key Results + dynamic owner/supporter assignment"
    implemented: true
    working: true
    file: "backend/strategy.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "GET/POST /strategy/okr with owner_id + supporter_ids[], PUT/DELETE. KR sub-endpoints: POST/PUT/DELETE /strategy/okr/{oid}/keyresults[/{kid}]. Verified: create OKR with owner, add KR, progress % computed from KR target/actual (avg). RBAC: SPV always, owner/supporters can update KR. `/strategy/okr/my` for anggota view. `?anggota_id=` filter (either owner or supporter). Verified 116.7% progress from KR 3/3.5 target/actual."

  - task: "KPI CRUD with weighted scoring (MAX/MIN polaritas)"
    implemented: true
    working: true
    file: "backend/strategy.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "GET/POST /strategy/kpi (?period_id=), PUT/DELETE /strategy/kpi/{id}. Formula: achievement = (aktual/target) for MAX, (target/aktual) for MIN; weighted_score = (ach%/100)*bobot; status EXCELLENT/ON_TRACK/AT_RISK/OFF_TRACK by thresholds 100/80/60. Anggota RBAC: hanya bisa update 'aktual' pada KPI mereka. Optional link ke OKR. Verified: 280M/300M target with bobot 25% → weighted 23.33 (ON_TRACK)."

  - task: "Action Plan (Projects) CRUD + link/unlink tasks + auto progress"
    implemented: true
    working: true
    file: "backend/strategy.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "GET/POST /strategy/projects, PUT/DELETE, POST /projects/{id}/link-tasks {task_ids}, POST /projects/{id}/unlink-task. Response includes: summary (total/selesai/proses/kendala/overdue/pct/status BERJALAN|SELESAI|TERLAMBAT|BELUM_MULAI) computed from linked tasks; start_effective/end_effective derived from linked task min/max dates if not explicit."

  - task: "Strategy dashboard aggregate"
    implemented: true
    working: true
    file: "backend/strategy.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "GET /strategy/dashboard?period_id= returns bsc_count, okr_count + avg_progress, kpi_count/total_bobot/final_score, project_count/selesai/terlambat. Verified via curl."

frontend:
  - task: "Menu 'Strategi & Eksekusi' di sidebar (SPV-only) dengan icon Target"
    implemented: true
    working: true
    file: "frontend/src/layouts/AppShell.jsx, App.js"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Route /strategy protected requireSpv. Nav item dengan icon Target added between Monitoring dan Manajemen User. Screenshot verified: sidebar tampilkan menu baru."

  - task: "Strategy page dengan period selector + 6 tabs"
    implemented: true
    working: true
    file: "frontend/src/pages/Strategy.jsx, PeriodDialog.jsx, StrategyOverview.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Hero teal-gradient dengan Select periode + tombol 'Periode baru' → PeriodDialog (nama, siklus preset 2/3/6/12 bulan, start/end auto, aktif toggle). 6 tabs: Beranda/BSC/OKR/KPI/Action Plan/Linimasa. Empty state kalau belum ada periode. Screenshot verified."

  - task: "BSC tab: 4-aspek grid dengan CRUD dialog"
    implemented: true
    working: true
    file: "frontend/src/pages/strategy/BscTab.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "4 kartu berwarna per aspek (Financial/Customer/Internal/Learning), tombol Tambah per aspek, dialog form nama/target/achieved. Edit inline via dialog."

  - task: "OKR tab: dynamic owner/supporter assign + inline KR editing"
    implemented: true
    working: true
    file: "frontend/src/pages/strategy/OkrTab.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Level tabs (Company/Divisi/Individu) dengan card OKR ekspandable. Dialog form owner dropdown (single, filter by divisi if level=DIVISI) + supporter multi-picker (Popover+Checkbox). KR list inline (Input onBlur autosave). Filter atas: Semua / Tanpa owner / per anggota. Progress bar computed dari KR target/actual."

  - task: "KPI tab: per-anggota summary + editable table + polaritas MAX/MIN"
    implemented: true
    working: true
    file: "frontend/src/pages/strategy/KpiTab.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Grid summary per-anggota (nama, divisi, jumlah KPI, skor, warning kalau bobot ≠ 100%), tabel editable (bobot/target/aktual inline via onBlur), badge status EXCELLENT/ON_TRACK/AT_RISK/OFF_TRACK. Dialog form dengan link ke OKR. Verified UI dengan curl-created KPI Sales."

  - task: "Action Plan tab: proyek dengan link ke tasks existing + progress otomatis"
    implemented: true
    working: true
    file: "frontend/src/pages/strategy/ActionPlanTab.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Card project dengan nama/outcome/OMTM/anggaran/divisi/owner/tim/tanggal, tombol 'Tautkan Task' (multi-select dari tasks existing), tombol lepas per task, progress bar otomatis dari task status. Badge status BERJALAN/SELESAI/TERLAMBAT/BELUM_MULAI."

  - task: "Linimasa tab: Gantt-style timeline proyek"
    implemented: true
    working: true
    file: "frontend/src/pages/strategy/LinimasaTab.jsx"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Header bulan otomatis dari range project. Setiap proyek satu baris dengan bar berwarna sesuai status (sky/emerald/red/slate). Bar clickable, tampilkan tanggal start→end. Empty state kalau tidak ada tanggal."

metadata:
  created_by: "main_agent"
  version: "1.9"
  test_sequence: 9
  run_ui: false

test_plan:
  current_focus:
    - "Strategy periods CRUD + activate"
    - "BSC CRUD (Balanced Scorecard)"
    - "OKR CRUD + Key Results + dynamic owner/supporter assignment"
    - "KPI CRUD with weighted scoring (MAX/MIN polaritas)"
    - "Action Plan (Projects) CRUD + link/unlink tasks + auto progress"
    - "Strategy dashboard aggregate"
  stuck_tasks: []
  test_all: false
  test_priority: "high_first"

agent_communication:
  - agent: "main"
    message: |
      Iteration 9 — Strategy & Execution module implemented (BSC/OKR/KPI/Action Plan/Linimasa).
      Backend: new /app/backend/strategy.py registered under /api/strategy/*. All 6 categories wired.
      Key business rules to verify:
        (a) OKR owner_id + supporter_ids[] dynamic assignment — SPV can leave owner empty; anggota can be supporter without being owner.
        (b) KPI weighted score correct: MAX → aktual/target; MIN → target/aktual. Status thresholds: >=100 EXCELLENT, >=80 ON_TRACK, >=60 AT_RISK, else OFF_TRACK.
        (c) Anggota RBAC on KPI: 401/403 if editing others' KPI or non-'aktual' fields.
        (d) Project progress derived from linked task IDs (SELESAI count / total). start_effective from min(tanggal_mulai), end_effective from max(deadline) of linked tasks if not explicit.
        (e) Cascade delete on period deletion cleans BSC/OKR/KRs/KPI/projects.
      Base URL: https://sanad-webapp.preview.emergentagent.com/api. SPV creds in /app/memory/test_credentials.md.
      Frontend compiled with warnings only. Screenshot verified /strategy page renders with hero + tabs + panduan.
      Please test the 6 backend tasks + regression on iter7/iter8 endpoints. Frontend not requested this round.
