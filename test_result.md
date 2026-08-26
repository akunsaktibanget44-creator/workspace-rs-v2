#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================
# (Preserved from previous iteration.)
#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

user_problem_statement: |
  Iteration 8 — Rebrand penuh ke "Workspace Ruang Sanad" (dengan logo custom yang di-upload user),
  perbaiki tampilan PDF export yang masih berantakan (teks overlap, alignment kacau),
  dan revisi hitungan pekan di menu Tugas Rutin Tracker tab Mingguan agar 1 pekan = Senin–Sabtu
  (hari operasional, Ahad libur).

backend:
  - task: "Rebrand backend API title ke Workspace Ruang Sanad"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "GET /api/ returns {message: 'Workspace Ruang Sanad API', version: '1.2'}"

  - task: "PDF export layout diperbaiki (fix overlap, embedded PNG logo, uniform metric grid, cleaner signature block)"
    implemented: true
    working: true
    file: "backend/pdf_export.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: false
        agent: "main"
        comment: "Sebelumnya inline mixed font sizes di score card menyebabkan text 'RUNGAN' overlap dengan '/100'. Metric cells inconsistent alignment. Signature block awkward spacing."
      - working: true
        agent: "main"
        comment: "Rewrite pdf_export.py: uniform metric cells (rowHeights=[52], 6 kolom task / 5 kolom amaliyah, VALIGN MIDDLE), score card jadi nested table (label→number/slash split→sub) tanpa inline font mix, embedded PNG logo dari /app/backend/assets/ruang_sanad_logo.png via reportlab Image, header 3-kolom (logo | brand | period box), gold divider, proper signature block dengan blank space+underline+label. File size 4KB → 374KB (with embedded logo image). Analyze tool report: 'RAPI' untuk header/tabel/tanda tangan/no-overlap; hanya minor alignment metric (accepted)."
      - working: true
        agent: "main"
        comment: "PDF filename slug diubah dari 'raport-sanad-*' ke 'raport-ruang-sanad-*'."

  - task: "GET /api/ rebrand check (regression from iter 7)"
    implemented: true
    working: true
    file: "backend/server.py"
    stuck_count: 0
    priority: "low"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Version bumped 1.1 → 1.2."

frontend:
  - task: "Ganti logo custom SVG dengan PNG Ruang Sanad yang di-upload"
    implemented: true
    working: true
    file: "frontend/src/components/SanadLogo.jsx, frontend/public/brand/ruang-sanad-logo.png"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "PNG di-copy ke /app/frontend/public/brand/ruang-sanad-logo.png. SanadLogo component sekarang render img tag dengan dua variant: 'full' (untuk login/register, tampilkan lockup logo+text) dan 'mark' (untuk sidebar/header mobile, crop calligraphy pakai overflow-hidden + objectPosition top). Screenshot verified: login page tampilkan full logo dengan gold calligraphy + 'RUANG SANAD', sidebar tampilkan calligraphy-only mark."

  - task: "Rebrand semua string 'Sanad' → 'Workspace Ruang Sanad'"
    implemented: true
    working: true
    file: "frontend/src/layouts/AppShell.jsx, pages/auth/Login.jsx, pages/auth/Register.jsx, public/index.html, pages/Raport.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Sidebar & mobile header: 'Workspace' (teal) + 'Ruang Sanad' (gold). HTML title updated. PDF download filename prefix 'raport-ruang-sanad-'."

  - task: "Tugas Rutin Tracker Mingguan — hitung pekan Senin–Sabtu (Ahad libur)"
    implemented: true
    working: true
    file: "frontend/src/pages/TugasRutin.jsx"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "weeksInMonth() sekarang skip Sunday (d.getDay()===0) saat iterate hari-hari bulan, sehingga pekan yang hanya berisi Minggu di dalam bulan tidak dihitung. Header pekan tampilkan range tanggal Senin–Sabtu (misal '01/08–01/08') + label 'Sen–Sab' + 'Pekan N'. Screenshot Aug 2026 shows W31-W36 = 6 pekan operasional dengan range Sen-Sab correct."

metadata:
  created_by: "main_agent"
  version: "1.8"
  test_sequence: 8
  run_ui: false

test_plan:
  current_focus:
    - "PDF export layout diperbaiki (fix overlap, embedded PNG logo, uniform metric grid, cleaner signature block)"
    - "Rebrand backend API title ke Workspace Ruang Sanad"
  stuck_tasks: []
  test_all: false
  test_priority: "high_first"

agent_communication:
  - agent: "main"
    message: |
      Iteration 8 fixes:
        1) Rebrand full "Sanad" → "Workspace Ruang Sanad" di semua UI text, HTML title, API title, PDF branding, filename slugs (raport-sanad-* → raport-ruang-sanad-*). API version 1.1 → 1.2.
        2) Logo custom SVG → PNG upload user (calligraphy gold + "RUANG SANAD" text). Dua variant: 'full' (login page) & 'mark' (sidebar, calligraphy crop).
        3) PDF layout rewrite penuh: no more inline font size mixing (fixes 'RUNGAN' overlap), uniform metric grid (rowHeights, VALIGN), embedded PNG logo via reportlab Image, 3-column header (logo|brand|period box), gold divider, proper signature block. File jadi 374KB (dari 4KB) karena embedded logo image. Analyze tool result: RAPI untuk header, no overlap, tabel rapi, signature rapi (minor metric alignment note only).
        4) TugasRutin.jsx Mingguan: weeksInMonth() skip Sunday saat iterate → hanya pekan yg punya minimal 1 hari operasional (Sen-Sab) di bulan itu yang dihitung. Header pekan tambah range tanggal Sen-Sab + label "Sen–Sab".
      Please test backend endpoints untuk PDF (per-anggota + tim) to make sure regression clean, dan verify API title. All previous iter-7 endpoints should still work (regression).
