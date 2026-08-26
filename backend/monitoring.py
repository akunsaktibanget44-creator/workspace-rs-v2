"""SPV Monitoring endpoints: deadline radar, workload, compliance, stagnation, division progress."""
from datetime import datetime, timezone, timedelta, date
from typing import Optional
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase


def build_monitoring_router(db: AsyncIOMotorDatabase, get_current_user) -> APIRouter:
    router = APIRouter(prefix="/monitoring", tags=["monitoring"])

    def _today():
        return date.today().isoformat()

    def _days_from_today(n):
        return (date.today() + timedelta(days=n)).isoformat()

    @router.get("/deadline-radar")
    async def deadline_radar(divisi_id: Optional[str] = None, _: dict = Depends(get_current_user)):
        base = {"archived": {"$ne": True}, "status": {"$ne": "SELESAI"}}
        if divisi_id:
            base["divisi_id"] = divisi_id
        today = _today()
        d3 = _days_from_today(3)

        overdue = await db.tasks.find({**base, "deadline": {"$lt": today, "$ne": None}}, {"_id": 0}).sort("deadline", 1).to_list(500)
        today_tasks = await db.tasks.find({**base, "deadline": today}, {"_id": 0}).to_list(500)
        upcoming = await db.tasks.find({**base, "deadline": {"$gt": today, "$lte": d3}}, {"_id": 0}).sort("deadline", 1).to_list(500)

        anggota = await db.anggota.find({}, {"_id": 0}).to_list(500)
        anggota_map = {a["id"]: a["nama"] for a in anggota}
        divisi = await db.divisi.find({}, {"_id": 0}).to_list(200)
        divisi_map = {d["id"]: d["nama"] for d in divisi}

        def _decorate(rows):
            return [{
                **r,
                "penerima_nama": anggota_map.get(r.get("penerima_tugas_id"), r.get("penerima_tugas") or "-"),
                "divisi_nama": divisi_map.get(r.get("divisi_id"), "-"),
            } for r in rows]

        return {
            "overdue": _decorate(overdue),
            "today": _decorate(today_tasks),
            "upcoming": _decorate(upcoming),
            "summary": {
                "overdue": len(overdue),
                "today": len(today_tasks),
                "upcoming": len(upcoming),
            },
        }

    @router.get("/workload")
    async def workload(divisi_id: Optional[str] = None, _: dict = Depends(get_current_user)):
        anggota_q = {}
        if divisi_id:
            anggota_q["divisi_id"] = divisi_id
        anggota = await db.anggota.find(anggota_q, {"_id": 0}).sort("urutan", 1).to_list(500)
        divisi = await db.divisi.find({}, {"_id": 0}).to_list(200)
        divisi_map = {d["id"]: d["nama"] for d in divisi}
        rows = []
        for a in anggota:
            base = {"penerima_tugas_id": a["id"], "archived": {"$ne": True}}
            active = await db.tasks.count_documents({**base, "status": {"$ne": "SELESAI"}})
            proses = await db.tasks.count_documents({**base, "status": "DALAM_PROSES"})
            kendala = await db.tasks.count_documents({**base, "status": "TERKENDALA"})
            belum = await db.tasks.count_documents({**base, "status": "BELUM_MULAI"})
            overdue = await db.tasks.count_documents({**base, "status": {"$ne": "SELESAI"}, "deadline": {"$lt": _today(), "$ne": None}})
            rows.append({
                **a,
                "divisi_nama": divisi_map.get(a.get("divisi_id"), "-"),
                "aktif": active,
                "proses": proses,
                "kendala": kendala,
                "belum": belum,
                "overdue": overdue,
            })
        rows.sort(key=lambda x: x["aktif"], reverse=True)
        max_val = max([r["aktif"] for r in rows] + [1])
        return {"anggota": rows, "max": max_val}

    @router.get("/amaliyah-compliance")
    async def amaliyah_compliance(days: int = 7, _: dict = Depends(get_current_user)):
        end = date.today()
        start = end - timedelta(days=days - 1)
        start_s, end_s = start.isoformat(), end.isoformat()
        items = await db.amaliyah_items.find({}, {"_id": 0}).sort("urutan", 1).to_list(500)
        entries = await db.amaliyah_entries.find(
            {"tanggal": {"$gte": start_s, "$lte": end_s}, "checked": True},
            {"_id": 0},
        ).to_list(20000)
        by_item = {}
        for e in entries:
            by_item[e["item_id"]] = by_item.get(e["item_id"], 0) + 1

        result = []
        for it in items:
            done = by_item.get(it["id"], 0)
            target = days
            pct = round(done / target * 100, 1) if target else 0
            result.append({**it, "done": done, "target": target, "pct": pct})
        result.sort(key=lambda x: x["pct"], reverse=True)
        total_target = sum(r["target"] for r in result) or 1
        total_done = sum(r["done"] for r in result)
        return {
            "days": days,
            "start": start_s,
            "end": end_s,
            "items": result,
            "overall_pct": round(total_done / total_target * 100, 1),
        }

    @router.get("/stagnant-tasks")
    async def stagnant_tasks(days: int = 3, _: dict = Depends(get_current_user)):
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        rows = await db.tasks.find(
            {
                "archived": {"$ne": True},
                "status": {"$in": ["BELUM_MULAI", "DALAM_PROSES", "TERKENDALA"]},
                "updated_at": {"$lt": cutoff},
            },
            {"_id": 0},
        ).sort("updated_at", 1).to_list(500)

        anggota = await db.anggota.find({}, {"_id": 0}).to_list(500)
        anggota_map = {a["id"]: a["nama"] for a in anggota}
        divisi = await db.divisi.find({}, {"_id": 0}).to_list(200)
        divisi_map = {d["id"]: d["nama"] for d in divisi}
        out = [{
            **r,
            "penerima_nama": anggota_map.get(r.get("penerima_tugas_id"), r.get("penerima_tugas") or "-"),
            "divisi_nama": divisi_map.get(r.get("divisi_id"), "-"),
            "hari_diam": (datetime.now(timezone.utc) - datetime.fromisoformat(r["updated_at"].replace("Z", "+00:00") if "Z" in r["updated_at"] else r["updated_at"])).days if r.get("updated_at") else 0,
        } for r in rows]
        return {"days_threshold": days, "tasks": out}

    @router.get("/division-progress")
    async def division_progress(_: dict = Depends(get_current_user)):
        divisi = await db.divisi.find({}, {"_id": 0}).sort("urutan", 1).to_list(200)
        rows = []
        for d in divisi:
            base = {"divisi_id": d["id"], "archived": {"$ne": True}}
            total = await db.tasks.count_documents(base)
            selesai = await db.tasks.count_documents({**base, "status": "SELESAI"})
            terkendala = await db.tasks.count_documents({**base, "status": "TERKENDALA"})
            overdue = await db.tasks.count_documents({**base, "status": {"$ne": "SELESAI"}, "deadline": {"$lt": _today(), "$ne": None}})
            pct = round(selesai / total * 100, 1) if total else 0
            rows.append({**d, "total": total, "selesai": selesai, "terkendala": terkendala, "overdue": overdue, "pct": pct})
        return {"divisi": rows}

    return router
