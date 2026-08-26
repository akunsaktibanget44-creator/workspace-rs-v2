"""Generate Raport PDF using reportlab."""
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT


EMERALD_DARK = colors.HexColor("#064E3B")
EMERALD = colors.HexColor("#047857")
EMERALD_LIGHT = colors.HexColor("#D1FAE5")
GOLD = colors.HexColor("#B45309")


def build_raport_pdf(summary: dict, start: str, end: str) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=1.6 * cm,
        bottomMargin=1.6 * cm,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        title="Raport Qolbu Manage",
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"], textColor=EMERALD_DARK, fontSize=22, spaceAfter=6, alignment=TA_LEFT)
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], textColor=EMERALD_DARK, fontSize=14, spaceAfter=4)
    body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=10, leading=14, textColor=colors.HexColor("#1F2937"))
    small = ParagraphStyle("small", parent=styles["BodyText"], fontSize=9, textColor=colors.HexColor("#6B7280"))
    score_big = ParagraphStyle("scoreBig", parent=styles["Heading1"], textColor=EMERALD_DARK, fontSize=48, alignment=TA_CENTER)

    story = []

    # Header
    story.append(Paragraph("Qolbu Manage", ParagraphStyle("brand", parent=styles["BodyText"], textColor=EMERALD, fontSize=10, spaceAfter=2)))
    story.append(Paragraph("Raport Kinerja & Amaliyah", h1))
    story.append(Paragraph(
        f"Periode: <b>{start}</b> — <b>{end}</b>  &nbsp;&nbsp; Dicetak: {datetime.now().strftime('%d %b %Y, %H:%M')}",
        small,
    ))
    story.append(Spacer(1, 14))

    # Combined score card
    combined = summary.get("combined_score", 0)
    auto = summary.get("auto_rekomendasi", "NETRAL")
    rek_color = {"REWARD": EMERALD, "EVALUASI": colors.HexColor("#B91C1C"), "NETRAL": colors.HexColor("#64748B")}[auto]

    score_table = Table(
        [
            [Paragraph("<b>SKOR GABUNGAN</b>", small), Paragraph("<b>REKOMENDASI OTOMATIS</b>", small)],
            [Paragraph(f"<font size=42 color='#064E3B'><b>{combined}</b></font><font size=14 color='#047857'>/100</font>", body),
             Paragraph(f"<font size=22 color='{rek_color.hexval()}'><b>{auto}</b></font>", body)],
        ],
        colWidths=[8 * cm, 8 * cm],
    )
    score_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, EMERALD_DARK),
        ("BACKGROUND", (0, 0), (-1, 0), EMERALD_LIGHT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 18))

    # Task breakdown
    t = summary.get("task", {})
    story.append(Paragraph("Ringkasan Tugas", h2))
    task_table = Table(
        [
            ["Metrik", "Jumlah"],
            ["Total tugas", t.get("total", 0)],
            ["Selesai", t.get("selesai", 0)],
            ["Dalam proses", t.get("dalam_proses", 0)],
            ["Belum mulai", t.get("belum_mulai", 0)],
            ["Terkendala", t.get("terkendala", 0)],
            ["Overdue (deadline lewat & belum selesai)", t.get("overdue", 0)],
            ["Skor tugas", f"{t.get('score', 0)}%"],
        ],
        colWidths=[11 * cm, 5 * cm],
    )
    task_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), EMERALD_DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(task_table)
    story.append(Spacer(1, 14))

    # Amaliyah
    a = summary.get("amaliyah", {})
    story.append(Paragraph("Ringkasan Amaliyah", h2))
    amal_table = Table(
        [
            ["Metrik", "Nilai"],
            ["Check-in tercatat", a.get("total_entries", 0)],
            ["Target check-in", a.get("target", 0)],
            ["Jumlah amaliyah aktif", a.get("items_count", 0)],
            ["Rentang hari", a.get("days", 0)],
            ["Skor amaliyah", f"{a.get('score', 0)}%"],
        ],
        colWidths=[11 * cm, 5 * cm],
    )
    amal_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), EMERALD_DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(amal_table)
    story.append(Spacer(1, 18))

    # SPV note
    note = summary.get("spv_note", {}) or {}
    story.append(Paragraph("Catatan & Keputusan SPV", h2))
    keputusan = note.get("rekomendasi", "NETRAL")
    catatan = note.get("catatan_spv", "") or "<i>Belum ada catatan.</i>"
    story.append(Paragraph(f"<b>Keputusan SPV:</b> {keputusan}", body))
    story.append(Spacer(1, 6))
    story.append(Paragraph(catatan.replace("\n", "<br/>"), body))
    story.append(Spacer(1, 20))

    # Footer
    story.append(Paragraph(
        "<i>Dokumen ini dihasilkan otomatis oleh Qolbu Manage. Fokus pada niat, ikhlaskan usaha.</i>",
        small,
    ))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()
