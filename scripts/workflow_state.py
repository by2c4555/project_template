#!/usr/bin/env python3
"""Shared machine-state and integrity helpers for Project Template v4.3.2.

STATE.json is the authoritative workflow state. Human-readable Markdown status files are
views generated from it; agents must not grant themselves authority by editing Markdown.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "EXECUTE" / "control"
STATE_PATH = CONTROL / "STATE.json"
LEDGER_PATH = CONTROL / "TRANSITIONS.jsonl"
WORKFLOW_VERSION = "4.3.2"
SCHEMA_VERSION = 1

PACKAGE_STATIC = [
    Path("EXECUTE/plan/IMPLEMENTATION_PLAN.md"),
    Path("EXECUTE/tasks/TASK_INDEX.md"),
]
PACKAGE_DIRS = [Path("EXECUTE/compiled")]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def initial_state() -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "workflow_version": WORKFLOW_VERSION,
        "project_state": "AWAITING_SCOPE_IMPORT",
        "active_cycle": None,
        "counters": {
            "cycle": 0,
            "planning": 0,
            "execution": 0,
            "evaluation": 0,
            "diagnosis": 0,
            "issue": 0,
            "approval": 0,
            "recovery_approval": 0,
        },
        "runtime_policy": {
            "manager_max_task_dispatches_per_batch": 10,
            "default_local_repair_attempts_per_task": 2,
            "safe_exec_stdout_chars": 12000,
            "safe_exec_stderr_chars": 12000,
            "require_package_integrity_each_dispatch": True,
        },
        "cycles": {},
        "last_transition_at": None,
    }


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def save_state(state: Dict[str, Any]) -> None:
    state["last_transition_at"] = utc_now()
    atomic_write_text(STATE_PATH, json.dumps(state, indent=2, sort_keys=True) + "\n")
    sync_views(state)


def load_state(*, create: bool = False) -> Dict[str, Any]:
    if not STATE_PATH.exists():
        if not create:
            raise SystemExit("WORKFLOW_STATE: FAIL\nSTATE.json missing. Run: python scripts/init_v43.py")
        state = initial_state()
        save_state(state)
        return state
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"WORKFLOW_STATE: FAIL\ninvalid STATE.json: {exc}")
    if state.get("workflow_version") != WORKFLOW_VERSION:
        raise SystemExit(
            f"WORKFLOW_STATE: FAIL\nworkflow_version must be {WORKFLOW_VERSION}, found {state.get('workflow_version')!r}"
        )
    return state


def append_transition(event: str, *, actor: str, cycle_id: Optional[str], details: Optional[Dict[str, Any]] = None) -> None:
    CONTROL.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": utc_now(),
        "event": event,
        "actor": actor,
        "cycle_id": cycle_id,
        "details": details or {},
    }
    with LEDGER_PATH.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def next_id(state: Dict[str, Any], kind: str, prefix: str, width: int = 3) -> str:
    state["counters"][kind] = int(state["counters"].get(kind, 0)) + 1
    return f"{prefix}{state['counters'][kind]:0{width}d}"


def active_cycle(state: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    cid = state.get("active_cycle")
    if not cid or cid not in state.get("cycles", {}):
        raise SystemExit("WORKFLOW_STATE: FAIL\nno active change cycle. Run start_cycle.py after importing external scope.")
    return cid, state["cycles"][cid]


def markdown_value(text: str, key: str) -> Optional[str]:
    m = re.search(rf"^\s*{re.escape(key)}:\s*(.*?)\s*$", text, re.M)
    return m.group(1).strip().strip("\"'") if m else None


def parse_inline_list(raw: Optional[str]) -> List[str]:
    if raw is None:
        return []
    raw = raw.strip()
    if raw in {"", "[]", "none", "null"}:
        return []
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [p.strip().strip("\"'") for p in inner.split(",") if p.strip()]
    return [raw]



def validate_project_details_handoff() -> Dict[str, Any]:
    """Validate the mutable external handoff before it becomes a Scope Snapshot."""
    path = ROOT / "EXECUTE" / "project_details.md"
    errors: List[str] = []
    if not path.is_file():
        raise ValueError("missing EXECUTE/project_details.md")
    text = path.read_text(encoding="utf-8", errors="replace")
    if markdown_value(text, "artifact_kind") != "PROJECT_DETAILS":
        errors.append("project_details artifact_kind must be PROJECT_DETAILS")
    if markdown_value(text, "artifact_status") != "READY_FOR_CODEX":
        errors.append("project_details artifact_status must be READY_FOR_CODEX")
    title = markdown_value(text, "scope_title")
    if not title or title.upper() in {"TODO", "UNKNOWN", "NONE"}:
        errors.append("project_details scope_title must be a real short title")
    raw_unknowns = markdown_value(text, "product_scope_unknowns")
    try:
        unknowns = int(raw_unknowns) if raw_unknowns is not None else -1
    except ValueError:
        unknowns = -1
    if unknowns != 0:
        errors.append("project_details product_scope_unknowns must be exactly 0")
    supporting = parse_inline_list(markdown_value(text, "supporting_files"))
    seen = set()
    for rel in supporting:
        if rel in seen:
            errors.append(f"duplicate supporting file: {rel}")
            continue
        seen.add(rel)
        rp = Path(rel)
        if rp.is_absolute() or ".." in rp.parts:
            errors.append(f"invalid supporting file path: {rel}")
            continue
        norm = str(rp).replace("\\", "/")
        if not norm.startswith("EXECUTE/docs/raw/"):
            errors.append(f"supporting file must be under EXECUTE/docs/raw/: {rel}")
            continue
        if not (ROOT / rp).is_file():
            errors.append(f"supporting file missing: {rel}")
    if errors:
        raise ValueError("\n".join(errors))
    return {
        "path": "EXECUTE/project_details.md",
        "scope_title": title,
        "baseline_ref": markdown_value(text, "baseline_ref") or "none",
        "product_scope_unknowns": unknowns,
        "supporting_files": supporting,
    }


def build_scope_manifest(scope_revision: str) -> Dict[str, Any]:
    """Build a deterministic manifest from the external scope handoff."""
    meta = validate_project_details_handoff()
    rels = [meta["path"], *meta["supporting_files"]]
    file_records = []
    aggregate = hashlib.sha256()
    for rel in rels:
        fp = ROOT / rel
        digest = sha256_file(fp)
        rec = {"path": rel, "sha256": digest, "bytes": fp.stat().st_size}
        file_records.append(rec)
        aggregate.update(rel.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(digest.encode("ascii"))
        aggregate.update(b"\n")
    return {
        "manifest_schema": 1,
        "scope_revision": scope_revision,
        "created_at": utc_now(),
        "scope_title": meta["scope_title"],
        "baseline_ref": meta["baseline_ref"],
        "product_scope_unknowns": 0,
        "source_handoff_path": meta["path"],
        "supporting_files": meta["supporting_files"],
        "scope_digest": aggregate.hexdigest(),
        "files": file_records,
    }


def snapshot_scope(cycle_id: str, manifest: Dict[str, Any]) -> str:
    """Capture the mutable external handoff into immutable cycle history."""
    import shutil
    revision = manifest["scope_revision"]
    base = ROOT / "EXECUTE" / "history" / "cycles" / cycle_id / "scope" / revision
    if base.exists():
        raise ValueError(f"scope snapshot already exists: {base.relative_to(ROOT)}")
    for rec in manifest.get("files", []):
        rel = Path(rec["path"])
        src = ROOT / rel
        dst = base / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    write_json(base / "SCOPE_MANIFEST.json", manifest)
    return str(base.relative_to(ROOT)).replace("\\", "/")


def verify_scope_snapshot(cycle: Dict[str, Any]) -> List[str]:
    """Verify immutable Scope Snapshot files/digest without checking current execution authority."""
    scope = cycle.get("scope") or {}
    snap = scope.get("snapshot_path")
    if not snap:
        return ["cycle has no active Scope Snapshot"]
    base = ROOT / snap
    mp = base / "SCOPE_MANIFEST.json"
    if not mp.is_file():
        return [f"Scope Snapshot manifest missing: {mp.relative_to(ROOT)}"]
    try:
        manifest = json.loads(mp.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"invalid Scope Snapshot manifest: {exc}"]
    errors: List[str] = []
    aggregate = hashlib.sha256()
    for rec in manifest.get("files", []):
        rel = str(rec.get("path"))
        fp = base / rel
        if not fp.is_file():
            errors.append(f"Scope Snapshot file missing: {rel}")
            continue
        got = sha256_file(fp)
        if got != rec.get("sha256"):
            errors.append(f"Scope Snapshot file changed: {rel}")
        aggregate.update(rel.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(got.encode("ascii"))
        aggregate.update(b"\n")
    if not errors and aggregate.hexdigest() != manifest.get("scope_digest"):
        errors.append("Scope Snapshot aggregate digest mismatch")
    if scope.get("digest") != manifest.get("scope_digest"):
        errors.append("cycle scope digest != Scope Snapshot manifest digest")
    if scope.get("revision_label") != manifest.get("scope_revision"):
        errors.append("cycle scope revision != Scope Snapshot manifest revision")
    return errors


def verify_active_scope(cycle: Dict[str, Any]) -> List[str]:
    """Verify the Scope Snapshot and all active approval/execution bindings."""
    scope = cycle.get("scope") or {}
    errors = verify_scope_snapshot(cycle)
    approval = cycle.get("approval") or {}
    if approval:
        if approval.get("scope_digest") != scope.get("digest"):
            errors.append("approval is bound to a different scope digest")
        if approval.get("scope_revision") != scope.get("revision_label"):
            errors.append("approval is bound to a different scope revision")
    execution = cycle.get("execution") or {}
    if execution and execution.get("approved_scope_digest") not in {None, scope.get("digest")}:
        errors.append("execution is bound to a different scope digest")
    return errors


def ensure_scope_snapshot_integrity(cycle: Dict[str, Any]) -> None:
    errors = verify_scope_snapshot(cycle)
    if errors:
        raise SystemExit("SCOPE_INTEGRITY: FAIL\n" + "\n".join(f"FAIL: {e}" for e in errors))


def ensure_scope_integrity(cycle: Dict[str, Any]) -> None:
    errors = verify_active_scope(cycle)
    if errors:
        raise SystemExit("SCOPE_INTEGRITY: FAIL\n" + "\n".join(f"FAIL: {e}" for e in errors))

def task_paths() -> List[Path]:
    task_dir = ROOT / "EXECUTE" / "tasks"
    out = []
    for p in sorted(task_dir.glob("TASK_*.md")):
        if p.name in {"TASK_INDEX.md", "TASK_TEMPLATE.md"}:
            continue
        if re.fullmatch(r"TASK_\d+(?:[-_].*)?\.md", p.name):
            out.append(p)
    return out


def task_id_from_text(path: Path, text: str) -> Optional[str]:
    return markdown_value(text, "task_id") or re.match(r"(TASK_\d+)", path.name).group(1) if re.match(r"(TASK_\d+)", path.name) else None


def parse_task_contract(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    task_id = markdown_value(text, "task_id")
    if not task_id:
        m = re.match(r"(TASK_\d+)", path.name)
        task_id = m.group(1) if m else None
    if not task_id or not re.fullmatch(r"TASK_\d+", task_id):
        raise ValueError(f"{path.relative_to(ROOT)}: missing/invalid task_id")
    max_repairs_raw = markdown_value(text, "max_evidence_driven_repair_attempts")
    try:
        max_repairs = int(max_repairs_raw) if max_repairs_raw is not None else None
    except ValueError:
        max_repairs = None
    return {
        "task_id": task_id,
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "planning_version": markdown_value(text, "planning_version"),
        "planning_revision": markdown_value(text, "planning_revision"),
        "artifact_status": markdown_value(text, "artifact_status"),
        "depends_on": parse_inline_list(markdown_value(text, "depends_on")),
        "max_repairs": max_repairs,
        "contains_mutable_status": bool(re.search(r"^\s*status:\s*", text, re.M)),
    }


def package_file_paths() -> List[Path]:
    files: List[Path] = []
    for rel in PACKAGE_STATIC:
        p = ROOT / rel
        if p.is_file():
            files.append(p)
    for rel_dir in PACKAGE_DIRS:
        d = ROOT / rel_dir
        if d.is_dir():
            files.extend(sorted(p for p in d.rglob("*") if p.is_file() and p.name != ".gitkeep"))
    files.extend(task_paths())
    # deterministic unique order
    uniq = {str(p.resolve()): p for p in files}
    return sorted(uniq.values(), key=lambda p: str(p.relative_to(ROOT)).replace("\\", "/"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_package_manifest(planning_version: str, planning_revision: str) -> Dict[str, Any]:
    errors: List[str] = []
    plan = ROOT / "EXECUTE/plan/IMPLEMENTATION_PLAN.md"
    index = ROOT / "EXECUTE/tasks/TASK_INDEX.md"
    for p in [plan, index]:
        if not p.is_file():
            errors.append(f"missing {p.relative_to(ROOT)}")
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if markdown_value(text, "planning_version") != planning_version:
            errors.append(f"{p.relative_to(ROOT)} planning_version != {planning_version}")
        if markdown_value(text, "planning_revision") != planning_revision:
            errors.append(f"{p.relative_to(ROOT)} planning_revision != {planning_revision}")
        if markdown_value(text, "artifact_status") not in {"COMPILED", "READY_FOR_APPROVAL"}:
            errors.append(f"{p.relative_to(ROOT)} artifact_status must be COMPILED/READY_FOR_APPROVAL")

    compiled_dir = ROOT / "EXECUTE/compiled"
    compiled_files = sorted(p for p in compiled_dir.glob("*.md") if p.is_file())
    if not compiled_files:
        errors.append("no compiled context artifacts exist")
    for cp in compiled_files:
        ctext = cp.read_text(encoding="utf-8", errors="replace")
        if markdown_value(ctext, "planning_version") != planning_version:
            errors.append(f"{cp.relative_to(ROOT)} planning_version != {planning_version}")
        if markdown_value(ctext, "planning_revision") != planning_revision:
            errors.append(f"{cp.relative_to(ROOT)} planning_revision != {planning_revision}")
        if markdown_value(ctext, "artifact_status") not in {"COMPILED", "READY_FOR_APPROVAL"}:
            errors.append(f"{cp.relative_to(ROOT)} artifact_status must be COMPILED/READY_FOR_APPROVAL")

    tasks = task_paths()
    if not tasks:
        errors.append("no generated TASK_NNN.md files")
    seen = set()
    contracts = []
    for path in tasks:
        try:
            c = parse_task_contract(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if c["task_id"] in seen:
            errors.append(f"duplicate task id: {c['task_id']}")
        seen.add(c["task_id"])
        if c["planning_version"] != planning_version:
            errors.append(f"{c['path']} planning_version != {planning_version}")
        if c["planning_revision"] != planning_revision:
            errors.append(f"{c['path']} planning_revision != {planning_revision}")
        if c["artifact_status"] not in {"COMPILED", "READY_FOR_APPROVAL"}:
            errors.append(f"{c['path']} artifact_status must be COMPILED/READY_FOR_APPROVAL")
        if c["contains_mutable_status"]:
            errors.append(f"{c['path']} contains mutable 'status:'; runtime status belongs in STATE.json")
        contracts.append(c)
    for c in contracts:
        for dep in c["depends_on"]:
            if dep not in seen:
                errors.append(f"{c['task_id']} depends on missing {dep}")

    if errors:
        raise ValueError("\n".join(errors))

    file_records = []
    aggregate = hashlib.sha256()
    for p in package_file_paths():
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        digest = sha256_file(p)
        size = p.stat().st_size
        file_records.append({"path": rel, "sha256": digest, "bytes": size})
        aggregate.update(rel.encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(digest.encode("ascii"))
        aggregate.update(b"\n")
    return {
        "manifest_schema": 1,
        "planning_version": planning_version,
        "planning_revision": planning_revision,
        "created_at": utc_now(),
        "package_digest": aggregate.hexdigest(),
        "task_count": len(contracts),
        "files": file_records,
        "task_contracts": contracts,
    }


def verify_manifest(manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    records = manifest.get("files") or []
    aggregate = hashlib.sha256()
    for rec in records:
        rel = rec.get("path")
        p = ROOT / str(rel)
        if not p.is_file():
            errors.append(f"approved package file missing: {rel}")
            continue
        got = sha256_file(p)
        if got != rec.get("sha256"):
            errors.append(f"approved package file changed: {rel}")
        aggregate.update(str(rel).encode("utf-8"))
        aggregate.update(b"\0")
        aggregate.update(got.encode("ascii"))
        aggregate.update(b"\n")
    if not errors and aggregate.hexdigest() != manifest.get("package_digest"):
        errors.append("approved package aggregate digest mismatch")
    return errors


def manifest_path_for(approval_id: str) -> Path:
    return CONTROL / "manifests" / f"{approval_id}_PACKAGE.json"


def approval_path_for(approval_id: str) -> Path:
    return CONTROL / "approvals" / f"{approval_id}.json"


def load_approved_manifest(cycle: Dict[str, Any]) -> Dict[str, Any]:
    approval = cycle.get("approval") or {}
    mp = approval.get("manifest_path")
    if not mp:
        raise ValueError("cycle has no approved package manifest")
    p = ROOT / mp
    if not p.is_file():
        raise ValueError(f"approved manifest missing: {mp}")
    return json.loads(p.read_text(encoding="utf-8"))


def verify_active_package(cycle: Dict[str, Any]) -> List[str]:
    try:
        manifest = load_approved_manifest(cycle)
    except Exception as exc:
        return [str(exc)]
    errors = verify_manifest(manifest)
    approval = cycle.get("approval") or {}
    if approval.get("package_digest") != manifest.get("package_digest"):
        errors.append("approval/package manifest digest mismatch")
    execution = cycle.get("execution") or {}
    if execution and execution.get("approved_package_digest") not in {None, manifest.get("package_digest")}:
        errors.append("execution bound package digest mismatch")
    return errors


def sync_views(state: Dict[str, Any]) -> None:
    """Regenerate compact Markdown views from machine state."""
    cid = state.get("active_cycle")
    cycle = state.get("cycles", {}).get(cid) if cid else None

    if not cycle:
        project = f'''# Project Status\n\n> GENERATED VIEW — authoritative state: `EXECUTE/control/STATE.json`\n\n```yaml\nworkflow_version: "{WORKFLOW_VERSION}"\nactive_cycle: none\nlifecycle_stage: AWAITING_SCOPE_IMPORT\nproject_validation_status: NOT_VALIDATED\nnext_action: IMPORT_EXTERNAL_SCOPE_THEN_START_CYCLE\n```\n'''
        planning = '''# Planning Status\n\n> GENERATED VIEW — authoritative state: `EXECUTE/control/STATE.json`\n\n```yaml\ncycle_id: none\nplanning_version: none\nplanning_revision: none\nplanning_status: NOT_CREATED\nmaterial_unknowns: unknown\npackage_status: NOT_COMPILED\nexecution_locked: true\n```\n'''
        execution = '''# Execution State\n\n> GENERATED VIEW — authoritative state: `EXECUTE/control/STATE.json`\n\n```yaml\ncycle_id: none\nexecution_version: none\nexecution_status: LOCKED\nactive_task: none\nactive_issue: none\nresume_authorized: false\n```\n'''
        evaluation = '''# Evaluation Status\n\n> GENERATED VIEW — authoritative state: `EXECUTE/control/STATE.json`\n\n```yaml\ncycle_id: none\nevaluation_version: none\nevaluation_status: NOT_STARTED\nresult: none\ncompletion_report: none\n```\n'''
        atomic_write_text(ROOT / "EXECUTE/PROJECT_STATUS.md", project)
        atomic_write_text(ROOT / "EXECUTE/plan/PLANNING_STATUS.md", planning)
        atomic_write_text(ROOT / "EXECUTE/execution/EXECUTION_STATE.md", execution)
        atomic_write_text(ROOT / "EXECUTE/evaluation/EVALUATION_STATUS.md", evaluation)
        return

    planning_obj = cycle.get("planning") or {}
    approval = cycle.get("approval") or {}
    execution_obj = cycle.get("execution") or {}
    evaluation_obj = cycle.get("evaluation") or {}
    active_eval = evaluation_obj.get("active") or {}
    validation = "VALIDATED" if cycle.get("status") == "CLOSED_VALIDATED" else "NOT_VALIDATED"
    resume_authorized = bool((execution_obj.get("recovery") or {}).get("resume_authorized"))
    next_action = cycle.get("next_action") or "NONE"

    project = f'''# Project Status\n\n> GENERATED VIEW — authoritative state: `EXECUTE/control/STATE.json`. Agents must not edit this file to grant authority.\n\n```yaml\nworkflow_version: "{WORKFLOW_VERSION}"\nactive_cycle: {cid}\ncycle_status: {cycle.get("status", "UNKNOWN")}\nlifecycle_stage: {cycle.get("lifecycle_stage", "UNKNOWN")}\nproject_validation_status: {validation}\nscope_revision: {(cycle.get("scope") or {}).get("revision_label", "none")}
scope_digest: {(cycle.get("scope") or {}).get("digest", "none")}\nplanning_version: {planning_obj.get("version", "none")}\nplanning_revision: {planning_obj.get("revision_label", "none")}\nplanning_status: {planning_obj.get("status", "NOT_CREATED")}\nbased_on_scope_revision: {planning_obj.get("based_on_scope_revision", "none")}\nbased_on_scope_digest: {planning_obj.get("based_on_scope_digest", "none")}\nmaterial_unknowns: {planning_obj.get("material_unknowns", "unknown")}\napproval_id: {approval.get("approval_id", "none")}\napproval_status: {approval.get("status", "NONE")}\napproved_package_digest: {approval.get("package_digest", "none")}\nexecution_version: {execution_obj.get("version", "none")}\nexecution_status: {execution_obj.get("status", "LOCKED")}\nactive_task: {execution_obj.get("active_task", "none")}\nactive_issue: {execution_obj.get("active_issue", cycle.get("active_issue") or "none")}\nrecovery_status: {(execution_obj.get("recovery") or {}).get("status", "NOT_ACTIVE")}\nresume_authorized: {str(resume_authorized).lower()}\nevaluation_version: {active_eval.get("version", "none")}\nevaluation_status: {evaluation_obj.get("status", "NOT_STARTED")}\nlatest_evaluation_result: {evaluation_obj.get("latest_result", "none")}\ncompletion_report: {cycle.get("completion_report", "none")}\nnext_action: {next_action}\n```\n'''

    planning_view = f'''# Planning Status\n\n> GENERATED VIEW — authoritative state: `EXECUTE/control/STATE.json`. Chat messages are feedback, never implementation approval.\n\n```yaml\ncycle_id: {cid}\nplanning_version: {planning_obj.get("version", "none")}\nplanning_revision: {planning_obj.get("revision_label", "none")}\nplanning_status: {planning_obj.get("status", "NOT_CREATED")}\nbased_on_scope_revision: {planning_obj.get("based_on_scope_revision", "none")}\nbased_on_scope_digest: {planning_obj.get("based_on_scope_digest", "none")}\nmaterial_unknowns: {planning_obj.get("material_unknowns", "unknown")}\npackage_status: {planning_obj.get("package_status", "NOT_COMPILED")}\ntask_expansion_allowed: {str(bool(planning_obj.get("task_expansion_allowed"))).lower()}\ninteraction_gate: {planning_obj.get("interaction_gate", "NONE")}\ninvocation_stop_required: {str(bool(planning_obj.get("invocation_stop_required"))).lower()}\nexecution_locked: {str(cycle.get("status") not in {"EXECUTION", "EXECUTION_COMPLETE"}).lower()}\napproval_id: {approval.get("approval_id", "none")}\napproval_status: {approval.get("status", "NONE")}\n```\n\nAllowed planning states: `NOT_CREATED`, `IN_PROGRESS`, `AWAITING_MATERIAL_FEEDBACK`, `PLAN_READY`, `APPROVED`, `SUPERSEDED`.\n'''

    tasks = execution_obj.get("tasks") or {}
    completed = [tid for tid, t in tasks.items() if t.get("status") in {"PASS", "PASS_RECOVERED"}]
    recovered = [tid for tid, t in tasks.items() if t.get("status") == "PASS_RECOVERED"]
    blocked = [tid for tid, t in tasks.items() if t.get("status") == "BLOCKED"]
    batch = execution_obj.get("manager_batch") or {}
    recovery = execution_obj.get("recovery") or {}
    execution_view = f'''# Execution State\n\n> GENERATED VIEW — authoritative state: `EXECUTE/control/STATE.json`. Manager/Builder must use Python gates for transitions.\n\n```yaml\ncycle_id: {cid}\nexecution_version: {execution_obj.get("version", "none")}\nexecution_status: {execution_obj.get("status", "LOCKED")}\nexecution_bound_planning_version: {execution_obj.get("bound_planning_version", "none")}\napproved_scope_digest: {execution_obj.get("approved_scope_digest", "none")}\napproved_package_digest: {execution_obj.get("approved_package_digest", "none")}\ncompleted_tasks: {json.dumps(completed)}\nrecovered_tasks: {json.dumps(recovered)}\nactive_task: {execution_obj.get("active_task", "none")}\nblocked_tasks: {json.dumps(blocked)}\nactive_issue: {execution_obj.get("active_issue", "none")}\nlast_resolved_issue: {execution_obj.get("last_resolved_issue", "none")}\nmanager_batch_number: {batch.get("number", 0)}\nmanager_batch_dispatches: {batch.get("dispatches", 0)}\nmanager_batch_max_dispatches: {batch.get("max_dispatches", state.get("runtime_policy", {}).get("manager_max_task_dispatches_per_batch", 10))}\nmanager_context_reset_required: {str(bool(batch.get("reset_required"))).lower()}\nrecovery_status: {recovery.get("status", "NOT_ACTIVE")}\nrecovery_diagnosis: {recovery.get("diagnosis", "none")}\nrecovery_resolution: {recovery.get("resolution", "none")}\nrecovery_verification: {recovery.get("verification", "none")}\nresume_authorized: {str(bool(recovery.get("resume_authorized"))).lower()}\nnext_task: {recovery.get("next_task", "none")}\n```\n'''

    evaluation_view = f'''# Evaluation Status\n\n> GENERATED VIEW — authoritative state: `EXECUTE/control/STATE.json`. Evaluation requires `start_evaluation.py`.\n\n```yaml\ncycle_id: {cid}\nevaluation_version: {active_eval.get("version", "none")}\nevaluation_status: {evaluation_obj.get("status", "NOT_STARTED")}\nresult: {evaluation_obj.get("latest_result", "none")}\nblocking_findings: {active_eval.get("blocking_findings", 0)}\ndiagnosis_required: {str(evaluation_obj.get("status") == "DIAGNOSIS_REQUIRED").lower()}\ncompletion_report: {cycle.get("completion_report", "none")}\nnext_route: {evaluation_obj.get("next_route", "none")}\n```\n'''

    atomic_write_text(ROOT / "EXECUTE/PROJECT_STATUS.md", project)
    atomic_write_text(ROOT / "EXECUTE/plan/PLANNING_STATUS.md", planning_view)
    atomic_write_text(ROOT / "EXECUTE/execution/EXECUTION_STATE.md", execution_view)
    atomic_write_text(ROOT / "EXECUTE/evaluation/EVALUATION_STATUS.md", evaluation_view)


def snapshot_package(cycle_id: str, label: str, manifest: Dict[str, Any]) -> str:
    """Copy exact package files to immutable history before active workspace advances."""
    import shutil
    base = ROOT / "EXECUTE" / "history" / "cycles" / cycle_id / label / "package"
    if base.exists():
        raise ValueError(f"history snapshot already exists: {base.relative_to(ROOT)}")
    for rec in manifest.get("files", []):
        rel = Path(rec["path"])
        src = ROOT / rel
        dst = base / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    write_json(base.parent / "PACKAGE_MANIFEST.json", manifest)
    return str(base.parent.relative_to(ROOT)).replace("\\", "/")


def reset_package_workspace(planning_version: str, planning_revision: str) -> None:
    """Clear mutable active package workspace between cycles/replans."""
    for p in task_paths():
        p.unlink()
    plan_text = (
        "---\nartifact_kind: IMPLEMENTATION_PLAN\nartifact_status: PLACEHOLDER\n"
        f"planning_version: {planning_version}\nplanning_revision: {planning_revision}\n---\n\n"
        "# Implementation Plan\n\nNot compiled yet for the active Planning revision.\n"
    )
    atomic_write_text(ROOT / "EXECUTE/plan/IMPLEMENTATION_PLAN.md", plan_text)
    index_text = (
        "---\nartifact_kind: TASK_INDEX\nartifact_status: PLACEHOLDER\n"
        f"planning_version: {planning_version}\nplanning_revision: {planning_revision}\n---\n\n"
        "# Task Index\n\nNo compiled Tasks yet for the active Planning revision. "
        "Runtime Task status belongs in `EXECUTE/control/STATE.json`.\n"
    )
    atomic_write_text(ROOT / "EXECUTE/tasks/TASK_INDEX.md", index_text)
    cdir = ROOT / "EXECUTE/compiled"
    cdir.mkdir(parents=True, exist_ok=True)
    for old_file in cdir.glob("*.md"):
        old_file.unlink()
    standard = ["PROJECT_BRIEF", "ARCHITECTURE", "DECISIONS", "GLOBAL_CONSTRAINTS", "INTERFACES", "DATA_MODEL", "KNOWN_RISKS"]
    for kind in standard:
        cp = cdir / f"{kind}.md"
        compiled_text = (
            f"---\nartifact_kind: {kind}\nartifact_status: PLACEHOLDER\n"
            f"planning_version: {planning_version}\nplanning_revision: {planning_revision}\n---\n\n"
            f"# {kind.replace('_', ' ').title()}\n\nNot compiled yet for the active Planning revision.\n"
        )
        atomic_write_text(cp, compiled_text)

def ensure_package_integrity(cycle: Dict[str, Any]) -> None:
    scope_errors = verify_active_scope(cycle)
    if scope_errors:
        raise SystemExit("SCOPE_INTEGRITY: FAIL\n" + "\n".join(f"FAIL: {e}" for e in scope_errors))
    errors = verify_active_package(cycle)
    if errors:
        raise SystemExit("PACKAGE_INTEGRITY: FAIL\n" + "\n".join(f"FAIL: {e}" for e in errors))


def write_json(path: Path, data: Dict[str, Any]) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, sort_keys=True) + "\n")


def human_tty_challenge(action: str, summary_lines: Iterable[str]) -> str:
    """Require a real interactive terminal acknowledgment.

    This is an accidental-run/token-runaway barrier, not a defense against a malicious
    process with full local-machine control.
    """
    import secrets
    import sys

    if not sys.stdin.isatty() or not sys.stdout.isatty():
        raise SystemExit(
            f"{action}: BLOCKED\nHuman-operated gate requires an interactive TTY. "
            "Do not call this approval from an agent/tool subprocess."
        )
    challenge = secrets.token_hex(3).upper()
    print(f"\n{action}")
    for line in summary_lines:
        print(line)
    print("\nThis transition can unlock a high-cost phase.")
    print(f"Challenge: {challenge}")
    entered = input("Type the challenge exactly to authorize: ").strip().upper()
    if entered != challenge:
        raise SystemExit(f"{action}: CANCELLED\nchallenge mismatch; no state changed")
    return challenge
