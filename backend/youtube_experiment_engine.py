import sqlite3
from pathlib import Path
from typing import Optional
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "youtube_growth.db"
def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(DB_PATH))
def _row_to_dict(row):
    if row is None:
        return None
    return dict(row)
def create_experiment(
    experiment_type: str,
    variant_name: str,
    video_id: Optional[int] = None,
    title: Optional[str] = None,
    thumbnail_concept: Optional[str] = None,
    hook: Optional[str] = None,
    status: str = "planned",
):
    con = _connect()
    try:
        cur = con.execute(
            """
            INSERT INTO youtube_experiments
            (
                video_id,
                experiment_type,
                variant_name,
                title,
                thumbnail_concept,
                hook,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                video_id,
                experiment_type,
                variant_name,
                title,
                thumbnail_concept,
                hook,
                status,
            ),
        )
        con.commit()
        return {
            "success": True,
            "experiment_id": cur.lastrowid,
            "experiment_type": experiment_type,
            "variant_name": variant_name,
            "status": status,
        }
    finally:
        con.close()
def get_experiment(experiment_id: int):
    con = _connect()
    con.row_factory = sqlite3.Row
    try:
        row = con.execute(
            """
            SELECT *
            FROM youtube_experiments
            WHERE id = ?
            """,
            (int(experiment_id),),
        ).fetchone()
        if not row:
            return {
                "success": False,
                "error": "Experiment not found",
            }
        return {
            "success": True,
            "experiment": _row_to_dict(row),
        }
    finally:
        con.close()
def list_experiments(
    video_id: Optional[int] = None,
    experiment_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100,
):
    con = _connect()
    con.row_factory = sqlite3.Row
    try:
        query = """
            SELECT *
            FROM youtube_experiments
            WHERE 1=1
        """
        params = []
        if video_id is not None:
            query += " AND video_id = ?"
            params.append(int(video_id))
        if experiment_type:
            query += " AND experiment_type = ?"
            params.append(experiment_type)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(int(limit))
        rows = con.execute(query, params).fetchall()
        return {
            "success": True,
            "count": len(rows),
            "experiments": [
                _row_to_dict(row)
                for row in rows
            ],
        }
    finally:
        con.close()
def update_experiment_result(
    experiment_id: int,
    result_metric: str,
    result_value: float,
    status: str = "completed",
):
    con = _connect()
    try:
        cur = con.execute(
            """
            UPDATE youtube_experiments
            SET
                result_metric = ?,
                result_value = ?,
                status = ?
            WHERE id = ?
            """,
            (
                result_metric,
                float(result_value),
                status,
                int(experiment_id),
            ),
        )
        con.commit()
        if cur.rowcount == 0:
            return {
                "success": False,
                "error": "Experiment not found",
            }
        return {
            "success": True,
            "experiment_id": int(experiment_id),
            "result_metric": result_metric,
            "result_value": float(result_value),
            "status": status,
        }
    finally:
        con.close()
def compare_experiments(
    experiment_ids: list,
    higher_is_better: bool = True,
):
    experiments = []
    for experiment_id in experiment_ids:
        result = get_experiment(int(experiment_id))
        if result.get("success"):
            experiment = result["experiment"]
            if experiment.get("result_value") is not None:
                experiments.append(experiment)
    if not experiments:
        return {
            "success": False,
            "error": "No completed experiment results found",
            "experiments": [],
        }
    if higher_is_better:
        ordered = sorted(
            experiments,
            key=lambda x: float(x["result_value"]),
            reverse=True,
        )
    else:
        ordered = sorted(
            experiments,
            key=lambda x: float(x["result_value"]),
        )
    best = ordered[0]
    return {
        "success": True,
        "higher_is_better": higher_is_better,
        "count": len(ordered),
        "best_experiment": best,
        "ranking": ordered,
        "best_variant": best["variant_name"],
        "best_value": float(best["result_value"]),
    }
def create_variant_set(
    experiment_type: str,
    variants: list,
    video_id: Optional[int] = None,
):
    if not variants:
        return {
            "success": False,
            "error": "No variants supplied",
        }
    created = []
    for index, variant in enumerate(variants, start=1):
        if isinstance(variant, dict):
            variant_name = variant.get(
                "variant_name",
                f"Variant {index}",
            )
            title = variant.get("title")
            thumbnail_concept = variant.get(
                "thumbnail_concept"
            )
            hook = variant.get("hook")
        else:
            variant_name = f"Variant {index}"
            title = str(variant)
            thumbnail_concept = None
            hook = None
        result = create_experiment(
            experiment_type=experiment_type,
            variant_name=variant_name,
            video_id=video_id,
            title=title,
            thumbnail_concept=thumbnail_concept,
            hook=hook,
            status="planned",
        )
        if result.get("success"):
            created.append(result)
    return {
        "success": True,
        "experiment_type": experiment_type,
        "variant_count": len(created),
        "variants": created,
    }
def summarize_experiments(
    experiment_type: Optional[str] = None,
):
    result = list_experiments(
        experiment_type=experiment_type,
        limit=500,
    )
    if not result.get("success"):
        return result
    experiments = result["experiments"]
    completed = [
        item
        for item in experiments
        if item.get("result_value") is not None
    ]
    if not completed:
        return {
            "success": True,
            "experiment_type": experiment_type,
            "total_experiments": len(experiments),
            "completed_experiments": 0,
            "average_result": 0.0,
            "best_result": None,
        }
    values = [
        float(item["result_value"])
        for item in completed
    ]
    best = max(
        completed,
        key=lambda x: float(x["result_value"])
    )
    return {
        "success": True,
        "experiment_type": experiment_type,
        "total_experiments": len(experiments),
        "completed_experiments": len(completed),
        "average_result": round(
            sum(values) / len(values),
            2,
        ),
        "best_result": best,
    }
class YouTubeExperimentEngine:
    def create(
        self,
        experiment_type: str,
        variant_name: str,
        video_id: Optional[int] = None,
        title: Optional[str] = None,
        thumbnail_concept: Optional[str] = None,
        hook: Optional[str] = None,
        status: str = "planned",
    ):
        return create_experiment(
            experiment_type,
            variant_name,
            video_id,
            title,
            thumbnail_concept,
            hook,
            status,
        )
    def get(self, experiment_id: int):
        return get_experiment(experiment_id)
    def list(
        self,
        video_id: Optional[int] = None,
        experiment_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
    ):
        return list_experiments(
            video_id,
            experiment_type,
            status,
            limit,
        )
    def update_result(
        self,
        experiment_id: int,
        result_metric: str,
        result_value: float,
        status: str = "completed",
    ):
        return update_experiment_result(
            experiment_id,
            result_metric,
            result_value,
            status,
        )
    def compare(
        self,
        experiment_ids: list,
        higher_is_better: bool = True,
    ):
        return compare_experiments(
            experiment_ids,
            higher_is_better,
        )
    def create_variants(
        self,
        experiment_type: str,
        variants: list,
        video_id: Optional[int] = None,
    ):
        return create_variant_set(
            experiment_type,
            variants,
            video_id,
        )
    def summarize(
        self,
        experiment_type: Optional[str] = None,
    ):
        return summarize_experiments(
            experiment_type
        )
experiment_engine = YouTubeExperimentEngine()
