from flask import Blueprint, render_template, request, current_app
from app.db_core import get_conn, infer_table_and_columns, pick_material_col
import math

listing_bp = Blueprint("listing", __name__, url_prefix="/jobs")

def _sanitize_cols(requested, all_cols, mat_col, max_cols=15):
    clean = [c for c in requested if c in all_cols and c != mat_col]
    return [mat_col] + clean[:max_cols-1]

@listing_bp.route("", methods=["GET"])
def list_jobs():
    db_path = current_app.config["DB_PATH"]
    conn = get_conn(db_path)

    table, all_cols = infer_table_and_columns(conn)
    if not table:
        return render_template("error.html", message="Veritabanında tablo bulunamadı.")

    mat_col = pick_material_col(all_cols)
    other_cols = [c for c in all_cols if c != mat_col]

    default_visible = [mat_col] + other_cols[:7]

    cols_param = request.args.getlist("cols")
    visible = _sanitize_cols(cols_param, all_cols, mat_col) if cols_param else default_visible

    q = (request.args.get("q") or "").strip()
    page_size = max(min(int(request.args.get("page_size", 50)), 200), 10)
    page = max(int(request.args.get("page", 1)), 1)
    offset = (page - 1) * page_size

    where = ""
    params = []
    if q:
        like = f"%{q}%"
        wh = [f"{c} LIKE ?" for c in visible]
        where = "WHERE " + " OR ".join(wh)
        params = [like] * len(visible)

    total = conn.execute(f"SELECT COUNT(*) AS c FROM {table} {where}", params).fetchone()["c"]
    rows = conn.execute(
        f"SELECT {', '.join(visible)} FROM {table} {where} LIMIT ? OFFSET ?",
        params + [page_size, offset]
    ).fetchall()

    total_pages = max(math.ceil(total / page_size), 1)

    return render_template(
        "jobs_list.html",
        table=table,
        all_columns=all_cols,
        mat_col=mat_col,
        visible_columns=visible,
        rows=rows,
        total=total,
        page=page,
        total_pages=total_pages,
        page_size=page_size,
        q=q,
        other_cols=other_cols
    )
