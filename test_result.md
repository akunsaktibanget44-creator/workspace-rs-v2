#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================
# (Preserved from previous iteration.)
#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

user_problem_statement: |
  Iteration 7 — Sanad (rebrand dari Qolbu Manage):
  1. Rebrand app ke "Sanad" + logo custom SVG (crescent-in-shield + gold dot)
  2. Raport per-anggota + PDF export individu + filter divisi & anggota + preset periode
  3. Monitoring SPV per-individu (tab "Per Anggota") + tombol aksi di deadline radar (Selesai, +3/+7 hari)
  4. Deadline Digest di Beranda (SPV): overdue/today/upcoming/stagnant
  5. PDF layout diperbaiki: logo Sanad, header, score card, task list table, signature, footer

backend:
  - task: "Endpoint GET /api/dashboard/digest (SPV-scoped daily digest)"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Verified via curl: returns counts + overdue/today/upcoming/stagnant lists. Scoped per role."

  - task: "Endpoint GET /api/monitoring/user/{anggota_id} (per-anggota monitoring)"
    implemented: true
    working: true
    file: "backend/monitoring.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Verified via curl with test anggota: returns anggota info + deadline (overdue/today/upcoming) + workload + stagnant + amaliyah."

  - task: "Endpoint GET /api/raport/summary?anggota_id= (per-anggota raport summary)"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Verified: filters tasks by penerima_tugas_id=anggota_id, amaliyah scoped ke user_id anggota jika linked, includes tasks_list untuk PDF."

  - task: "Endpoint GET /api/raport/export.pdf?anggota_id= (per-anggota PDF)"
    implemented: true
    working: true
    file: "backend/server.py, backend/pdf_export.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Verified via curl: PDF ~4.4KB dengan header Sanad + tabel daftar tugas. Filename slug per anggota."

  - task: "PUT /api/raport/note?anggota_id= (per-anggota SPV note)"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Note keyed by id=anggota:{aid} vs id=singleton. Backward compatible."

  - task: "Rebrand backend title → Sanad API"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "low"
    needs_retesting: false
    status_history:
      - working: true
        agent: "main"
        comment: "GET /api/ returns {message: 'Sanad API', version: '1.1'}"

frontend:
  - task: "Rebrand UI ke Sanad + custom SanadLogo SVG"
    implemented: true
    working: true
    file: "frontend/src/components/SanadLogo.jsx, layouts/AppShell.jsx, pages/auth/Login.jsx, pages/auth/Register.jsx, public/index.html"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Screenshot verified: sidebar & login page menampilkan logo Sanad + tagline 'Amal • Kerja • Raport'. HTML title updated."

  - task: "Deadline Digest widget di Beranda (SPV)"
    implemented: true
    working: true
    file: "frontend/src/pages/Dashboard.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Widget tampil untuk SPV: 4 chip (overdue/today/upcoming/stagnant) + 2 kolom (Butuh Aksi Sekarang, Perhatian Berikutnya). Empty state 'Alhamdulillah'."

  - task: "Raport per-anggota (filter divisi/anggota + preset + PDF)"
    implemented: true
    working: true
    file: "frontend/src/pages/Raport.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Filter bar dengan Select divisi (cascading anggota list), preset 7/bulan/30/90 hari, individu header block, export PDF per-anggota."

  - task: "Monitoring Per-Anggota tab + action buttons deadline radar"
    implemented: true
    working: true
    file: "frontend/src/pages/Monitoring.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Tab baru 'Per Anggota' dengan cascading select divisi→anggota. Detail: hero avatar, deadline 3-col, stagnant list, amaliyah 7-hari. TaskCard punya keterangan radar + tombol Selesai / +3h / +7h."

metadata:
  created_by: "main_agent"
  version: "1.7"
  test_sequence: 7
  run_ui: false

test_plan:
  current_focus:
    - "Endpoint GET /api/dashboard/digest (SPV-scoped daily digest)"
    - "Endpoint GET /api/monitoring/user/{anggota_id} (per-anggota monitoring)"
    - "Endpoint GET /api/raport/summary?anggota_id= (per-anggota raport summary)"
    - "Endpoint GET /api/raport/export.pdf?anggota_id= (per-anggota PDF)"
    - "PUT /api/raport/note?anggota_id= (per-anggota SPV note)"
  stuck_tasks: []
  test_all: false
  test_priority: "high_first"

agent_communication:
  - agent: "main"
    message: |
      Iterasi 7 selesai implementasi:
        1) Rebrand full "Qolbu Manage" → "Sanad" + custom SVG logo (SanadLogo component).
        2) 5 endpoint baru/updated backend: dashboard/digest, monitoring/user/{id}, raport/summary?anggota_id, raport/export.pdf?anggota_id, raport/note?anggota_id.
        3) 3 halaman frontend diperbarui: Dashboard (+DeadlineDigest untuk SPV), Raport (filter divisi+anggota+preset+PDF individu), Monitoring (tab Per Anggota + action buttons).
        4) PDF export layout redesigned dengan Sanad logo drawn via reportlab Flowable, task list table, signature.
      Sudah verify via curl semua endpoint OK. Frontend compiled with warnings only.
      Test credentials di /app/memory/test_credentials.md.
      Please test backend endpoints (per-anggota flow) + verify frontend Monitoring "Per Anggota" tab and Raport "Export PDF" flow.
