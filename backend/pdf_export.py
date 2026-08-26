"""Generate Raport PDF using reportlab — Sanad branded, with logo & filters."""
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether,
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas


EMERALD_DARK = colors.HexColor("#064E3B")
EMERALD = colors.HexColor("#047857")
EMERALD_MED = colors.HexColor("#059669")
EMERALD_LIGHT = colors.HexColor("#D1FAE5")
EMERALD_TINT = colors.HexColor("#ECFDF5")
GOLD = colors.HexColor("#B45309")
INK = colors.HexColor("#0F172A")
MUTED = colors.HexColor("#64748B")
BORDER = colors.HexColor("#E2E8F0")


class SanadLogo(Flowable):
    """A simple crescent-in-shield logo drawn with reportlab primitives."""
    def __init__(self, size=18*mm):
        Flowable.__init__(self)
        self.size = size

    def wrap(self, *args):
        return (self.size, self.size)

    def draw(self):
        c = self.canv
        s = self.size
        # Shield background rounded rect
        c.setFillColor(EMERALD_DARK)
        c.setStrokeColor(EMERALD_DARK)
        c.roundRect(0, 0, s, s, s*0.22, fill=1, stroke=0)
        # Crescent
        c.setFillColor(colors.white)
        c.circle(s*0.55, s*0.55, s*0.28, fill=1, stroke=0)
        c.setFillColor(EMERALD_DARK)
        c.circle(s*0.65, s*0.6, s*0.25, fill=1, stroke=0)
        # Dot
        c.setFillColor(colors.HexColor("#FBBF24"))
        c.circle(s*0.32, s*0.32, s*0.05, fill=1, stroke=0)


def _footer(canvas_obj: canvas.Canvas, doc):
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawString(1.8*cm, 1*cm, "Sanad · Amal • Kerja • Raport")
    canvas_obj.drawRightString(A4[0] - 1.8*cm, 1*cm, f"Halaman {doc.page}")
    canvas_obj.setStrokeColor(BORDER)
    canvas_obj.line(1.8*cm, 1.3*cm, A4[0]-1.8*cm, 1.3*cm)
    canvas_obj.restoreState()


def build_raport_pdf(
    summary: dict,
    start: str,
    end: str,
    subject: str = "Raport Kinerja Tim",
    anggota_nama: str | None = None,
    divisi_nama: str | None = None,
) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=1.5 * cm,
        bottomMargin=2 * cm,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        title=f"Sanad · {subject}",
        author="Sanad",
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"], textColor=EMERALD_DARK, fontSize=22, spaceAfter=4, alignment=TA_LEFT, leading=26)
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], textColor=EMERALD_DARK, fontSize=13, spaceAfter=6, spaceBefore=6)
    body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=10, leading=14, textColor=INK)
    small = ParagraphStyle("small", parent=styles["BodyText"], fontSize=9, textColor=MUTED, leading=12)
    brand = ParagraphStyle("brand", parent=styles["BodyText"], textColor=EMERALD, fontSize=9, spaceAfter=0, leading=11)
    subject_style = ParagraphStyle("subj", parent=styles["BodyText"], textColor=MUTED, fontSize=10, leading=13, spaceAfter=2)

    story = []

    # ===== HEADER: Logo + Brand =====
    header_tbl = Table(
        [[
            SanadLogo(size=16*mm),
            [
                Paragraph("SANAD", ParagraphStyle("bn", parent=body, textColor=EMERALD_DARK, fontSize=16, leading=18, fontName="Helvetica-Bold")),
                Paragraph("Amal • Kerja • Raport", brand),
            ],
            Paragraph(f"<b>Periode</b><br/>{start} — {end}", ParagraphStyle("dt", parent=small, alignment=TA_RIGHT, textColor=INK)),
        ]],
        colWidths=[2*cm, 9*cm, 5.6*cm],
    )
    header_tbl.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LINEBELOW", (0,0), (-1,-1), 1, EMERALD),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(header_tbl)
    story.append(Spacer(1, 14))

    # ===== TITLE / SUBJECT =====
    story.append(Paragraph(subject, h1))
    meta_line = f"Dicetak: {datetime.now().strftime('%d %B %Y, %H:%M')}"
    if anggota_nama:
        meta_line = f"Anggota: <b>{anggota_nama}</b>" + (f" · Divisi: <b>{divisi_nama}</b>" if divisi_nama else "") + f" · {meta_line}"
    story.append(Paragraph(meta_line, subject_style))
    story.append(Spacer(1, 12))

    # ===== SCORE HERO =====
    combined = summary.get("combined_score", 0)
    auto = summary.get("auto_rekomendasi", "NETRAL")
    rek_color = {"REWARD": EMERALD, "EVALUASI": colors.HexColor("#B91C1C"), "NETRAL": MUTED}[auto]
    rek_bg = {"REWARD": EMERALD_LIGHT, "EVALUASI": colors.HexColor("#FEE2E2"), "NETRAL": colors.HexColor("#F1F5F9")}[auto]

    score_left = Paragraph(
        f"<font size=10 color='#047857'><b>SKOR GABUNGAN</b></font><br/>"
        f"<font size=44 color='#064E3B'><b>{combined}</b></font>"
        f"<font size=14 color='#059669'>/100</font><br/>"
        f"<font size=8 color='#64748B'>60% Tugas + 40% Amaliyah</font>",
        body,
    )
    score_right = Paragraph(
        f"<font size=9 color='#64748B'><b>REKOMENDASI OTOMATIS</b></font><br/>"
        f"<font size=22 color='{rek_color.hexval()}'><b>{auto}</b></font>",
        body,
    )
    score_table = Table([[score_left, score_right]], colWidths=[9*cm, 7.6*cm])
    score_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.5, BORDER),
        ("BACKGROUND", (0,0), (0,0), EMERALD_TINT),
        ("BACKGROUND", (1,0), (1,0), rek_bg),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 14),
        ("TOPPADDING", (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 16))

    # ===== TASK BREAKDOWN =====
    t = summary.get("task", {})
    story.append(Paragraph("Ringkasan Tugas", h2))

    def _metric_cell(label, val, color):
        return Paragraph(f"<font size=8 color='#64748B'><b>{label}</b></font><br/><font size=18 color='{color}'><b>{val}</b></font>", body)

    metrics = Table(
        [[
            _metric_cell("TOTAL", t.get("total", 0), "#0F172A"),
            _metric_cell("SELESAI", t.get("selesai", 0), "#047857"),
            _metric_cell("PROSES", t.get("dalam_proses", 0), "#B45309"),
            _metric_cell("BELUM", t.get("belum_mulai", 0), "#64748B"),
            _metric_cell("KENDALA", t.get("terkendala", 0), "#B91C1C"),
            _metric_cell("OVERDUE", t.get("overdue", 0), "#DC2626"),
        ]],
        colWidths=[2.77*cm]*6,
    )
    metrics.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.4, BORDER),
        ("INNERGRID", (0,0), (-1,-1), 0.4, BORDER),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(metrics)

    # progress bar
    tscore = t.get("score", 0)
    story.append(Spacer(1, 8))
    bar = Table(
        [[
            Paragraph(f"<font size=9 color='#0F172A'><b>Skor Tugas</b></font>", body),
            Paragraph(f"<font size=11 color='#064E3B'><b>{tscore}%</b></font>", ParagraphStyle('r', parent=body, alignment=TA_RIGHT)),
        ]],
        colWidths=[13.6*cm, 3*cm],
    )
    bar.setStyle(TableStyle([("BOTTOMPADDING",(0,0),(-1,-1),2)]))
    story.append(bar)
    # Fake progress bar via nested table
    fill_w = max(0.1, min(16.6, 16.6 * tscore / 100.0))
    pbar = Table([[""]], colWidths=[fill_w*cm], rowHeights=[6])
    pbar.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),EMERALD_MED),("BOX",(0,0),(-1,-1),0,EMERALD_MED)]))
    pbar_bg = Table([[pbar]], colWidths=[16.6*cm])
    pbar_bg.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),EMERALD_LIGHT),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    story.append(pbar_bg)
    story.append(Spacer(1, 16))

    # ===== AMALIYAH =====
    a = summary.get("amaliyah", {})
    story.append(Paragraph("Ringkasan Amaliyah", h2))
    amal_metrics = Table(
        [[
            _metric_cell("CHECK-IN", a.get("total_entries", 0), "#047857"),
            _metric_cell("TARGET", a.get("target", 0), "#0F172A"),
            _metric_cell("AMALIYAH", a.get("items_count", 0), "#0F172A"),
            _metric_cell("HARI", a.get("days", 0), "#0F172A"),
            _metric_cell("SKOR", f"{a.get('score', 0)}%", "#064E3B"),
        ]],
        colWidths=[3.32*cm]*5,
    )
    amal_metrics.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.4, BORDER),
        ("INNERGRID", (0,0), (-1,-1), 0.4, BORDER),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(amal_metrics)
    story.append(Spacer(1, 8))

    ascore = a.get("score", 0)
    fill_w = max(0.1, min(16.6, 16.6 * ascore / 100.0))
    pbar = Table([[""]], colWidths=[fill_w*cm], rowHeights=[6])
    pbar.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),EMERALD),("BOX",(0,0),(-1,-1),0,EMERALD)]))
    pbar_bg = Table([[pbar]], colWidths=[16.6*cm])
    pbar_bg.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),EMERALD_LIGHT),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0),("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    story.append(pbar_bg)
    story.append(Spacer(1, 16))

    # ===== TASKS LIST (optional per-anggota) =====
    tasks_list = summary.get("tasks_list") or []
    if tasks_list:
        story.append(Paragraph(f"Daftar Tugas ({len(tasks_list)})", h2))
        rows = [["No", "Nama Tugas", "Status", "Deadline"]]
        for i, tk in enumerate(tasks_list[:60], 1):
            rows.append([
                str(i),
                Paragraph((tk.get("nama") or "-")[:80], small),
                (tk.get("status") or "-").replace("_", " ").title(),
                tk.get("deadline") or "-",
            ])
        tbl = Table(rows, colWidths=[1*cm, 9.6*cm, 3.5*cm, 2.5*cm], repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), EMERALD_DARK),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,0), 9),
            ("FONTSIZE", (0,1), (-1,-1), 9),
            ("GRID", (0,0), (-1,-1), 0.3, BORDER),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, EMERALD_TINT]),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 14))

    # ===== SPV NOTE =====
    note = summary.get("spv_note", {}) or {}
    story.append(Paragraph("Catatan & Keputusan SPV", h2))
    keputusan = note.get("rekomendasi", "NETRAL")
    catatan = (note.get("catatan_spv") or "").strip() or "<i>Belum ada catatan dari SPV.</i>"
    note_tbl = Table(
        [[
            Paragraph(f"<b>Keputusan SPV:</b> <font color='{rek_color.hexval()}'><b>{keputusan}</b></font>", body),
        ], [
            Paragraph(catatan.replace("\n", "<br/>"), body),
        ]],
        colWidths=[16.6*cm],
    )
    note_tbl.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.5, BORDER),
        ("BACKGROUND", (0,0), (-1,0), EMERALD_TINT),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(note_tbl)
    story.append(Spacer(1, 22))

    # ===== SIGN =====
    sign_tbl = Table(
        [[
            Paragraph("<font size=9 color='#64748B'>Dokumen dihasilkan otomatis oleh <b>Sanad</b>.<br/>Fokus pada niat, ikhlaskan usaha.</font>", small),
            Paragraph("<font size=9 color='#0F172A'><b>Ttd. SPV</b><br/><br/><br/>______________________</font>",
                      ParagraphStyle('sr', parent=small, alignment=TA_RIGHT)),
        ]],
        colWidths=[10*cm, 6.6*cm],
    )
    sign_tbl.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"BOTTOM")]))
    story.append(sign_tbl)

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    buf.seek(0)
    return buf.getvalue()
