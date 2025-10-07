
from flask import Blueprint, render_template, request, current_app
from app.db_core import get_conn, infer_table_and_columns, pick_material_col
import math

listing_bp = Blueprint("listing", __name__, url_prefix="/jobs")

@listing_bp.route("", methods=["GET"])
def list_jobs():
    db_path = current_app.config["DB_PATH"]
    conn = get_conn(db_path)
    table, cols = infer_table_and_columns(conn)
    if not table:
        return render_template("error.html", message="Veritabanında tablo bulunamadı.")
    mat_col = pick_material_col(cols)
    after = [c for c in cols if c != mat_col]
    visible = [mat_col] + after[:7]
    search = request.args.get("q","").strip()
    page = int(request.args.get("page",1))
    limit = int(request.args.get("page_size",50))
    offset = (page-1)*limit
    params = []
    where = ""
    if search:
        like = f"%{search}%"
        wh = [f"{c} LIKE ?" for c in visible]
        where = "WHERE " + " OR ".join(wh)
        params = [like]*len(visible)
    total = conn.execute(f"SELECT COUNT(*) AS c FROM {table} {where}", params).fetchone()["c"]
    rows = conn.execute(f"SELECT {', '.join(visible)} FROM {table} {where} LIMIT ? OFFSET ?", params+[limit,offset]).fetchall()
    total_pages = max(math.ceil(total/limit),1)
    return render_template("jobs_list.html", visible_columns=visible, rows=rows, total=total, page=page, total_pages=total_pages, page_size=limit, search=search)
