#!/usr/bin/env python3
"""Provider-neutral resumable External Agent work checkpoints for Project Template v4.4.0.

STATE.json owns authority. EXECUTE/control/AGENT_WORK.json and EXECUTE/work/WORK_*_RESUME.md
are durable working memory only.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from workflow_state import ROOT, CONTROL, active_cycle, append_transition, load_state, next_id, save_state, utc_now, write_json

WORK_PATH = CONTROL / "AGENT_WORK.json"
ROLES = {"PLANNING","DIAGNOSIS","RECOVERY","EVALUATION"}

def git_snapshot():
    try:
        head=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
        status=subprocess.check_output(["git","status","--porcelain=v1"],cwd=ROOT,text=True,stderr=subprocess.DEVNULL)
        dirty=hashlib.sha256(status.encode()).hexdigest()
        return {"git_head":head,"git_dirty_digest":dirty,"git_available":True}
    except Exception:
        return {"git_head":None,"git_dirty_digest":None,"git_available":False}

def role_binding(cycle,role):
    scope=cycle.get("scope") or {}; planning=cycle.get("planning") or {}; ex=cycle.get("execution") or {}; ev=cycle.get("evaluation") or {}; active_ev=ev.get("active") or {}
    out={"cycle_id":cycle.get("cycle_id"),"role":role,"scope_revision":scope.get("revision_label"),"scope_digest":scope.get("digest")}
    if role=="PLANNING": out.update({"planning_version":planning.get("version"),"planning_revision":planning.get("revision_label")})
    elif role=="DIAGNOSIS": out.update({"issue_id":cycle.get("active_issue")})
    elif role=="RECOVERY":
        issue=next((x for x in cycle.get("issues",[]) if x.get("issue_id")==cycle.get("active_issue")),{})
        out.update({"issue_id":cycle.get("active_issue"),"diagnosis_digest":issue.get("diagnosis_digest"),"recovery_approval":issue.get("recovery_approval")})
    elif role=="EVALUATION": out.update({"evaluation_version":active_ev.get("version"),"approved_package_digest":ex.get("approved_package_digest")})
    return out

def binding_digest(binding):
    return hashlib.sha256(json.dumps(binding,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def validate_role_state(cycle,role):
    status=cycle.get("status"); stage=cycle.get("lifecycle_stage")
    if role=="PLANNING" and status!="PLANNING": raise SystemExit(f"AGENT_WORK: BLOCKED\nPLANNING requires cycle status PLANNING, found {status}")
    if role=="DIAGNOSIS" and (not cycle.get("active_issue") or stage!="DIAGNOSIS"): raise SystemExit("AGENT_WORK: BLOCKED\nDIAGNOSIS requires an active Issue routed to DIAGNOSIS")
    if role=="RECOVERY":
        issue=next((x for x in cycle.get("issues",[]) if x.get("issue_id")==cycle.get("active_issue")),None)
        if not issue or not issue.get("recovery_approval"): raise SystemExit("AGENT_WORK: BLOCKED\nRECOVERY requires an active Issue with human recovery approval")
    if role=="EVALUATION":
        ev=cycle.get("evaluation") or {}
        if status!="EVALUATION" or ev.get("status")!="AUTHORIZED": raise SystemExit("AGENT_WORK: BLOCKED\nEVALUATION requires one authorized Evaluation attempt")

def load_work():
    if not WORK_PATH.is_file(): return None
    return json.loads(WORK_PATH.read_text(encoding="utf-8"))

def write_resume(path,work,note=None):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True)
    if note is not None:
        body=note.rstrip()+"\n"
    elif p.exists():
        body=p.read_text(encoding="utf-8")
    else:
        body="No verified findings persisted yet.\n"
    header=(f"# External Agent Resume Capsule — {work['work_id']}\n\n"
            f"role: {work['role']}\ncheckpoint_seq: {work['checkpoint_seq']}\nphase: {work.get('phase')}\n"
            f"current_unit: {work.get('current_unit')}\nnext_unit: {work.get('next_unit')}\nstatus: {work['status']}\n\n"
            "## Durable Handoff\n\n")
    p.write_text(header+body,encoding="utf-8")

def cmd_begin(a):
    state=load_state(); cid,cycle=active_cycle(state); role=a.role.upper(); validate_role_state(cycle,role)
    bind=role_binding(cycle,role); bd=binding_digest(bind); existing=load_work(); ref=state.get("active_external_work") or {}
    if existing and ref.get("work_id")==existing.get("work_id") and existing.get("status") in {"IN_PROGRESS","CHECKPOINTED"}:
        if existing.get("role")==role and existing.get("binding_digest")==bd:
            print("AGENT_WORK: RESUME"); print(f"work_id: {existing['work_id']}"); print(f"checkpoint_seq: {existing['checkpoint_seq']}"); print(f"resume_artifact: {existing['resume_artifact']}"); print(f"next_unit: {existing.get('next_unit')}"); return
        raise SystemExit("AGENT_WORK: BLOCKED\nanother External Agent work item is active; finish or explicitly supersede it before beginning a different role/binding")
    wid=next_id(state,"agent_work","WORK_",4); resume=f"EXECUTE/work/{wid}_RESUME.md"
    work={"work_id":wid,"cycle_id":cid,"role":role,"status":"IN_PROGRESS","phase":a.phase or "START","current_unit":None,"next_unit":a.next_unit,"checkpoint_seq":0,"binding":bind,"binding_digest":bd,"git":git_snapshot(),"resume_artifact":resume,"started_at":utc_now(),"updated_at":utc_now(),"last_agent":{"tool":a.tool,"model":a.model}}
    write_json(WORK_PATH,work); write_resume(resume,work,"Start from the authoritative role prompt. No prior work units are complete.")
    state["active_external_work"]={"work_id":wid,"cycle_id":cid,"role":role,"status":"IN_PROGRESS","checkpoint_seq":0,"work_path":"EXECUTE/control/AGENT_WORK.json","resume_artifact":resume,"binding_digest":bd}
    save_state(state); append_transition("EXTERNAL_AGENT_WORK_STARTED",actor="agent:agent_work",cycle_id=cid,details={"work_id":wid,"role":role,"tool":a.tool,"model":a.model})
    print("AGENT_WORK: STARTED"); print(f"work_id: {wid}"); print(f"resume_artifact: {resume}")

def verify_current(state,cycle,work):
    if not work: raise SystemExit("AGENT_WORK: BLOCKED\nno AGENT_WORK.json; run begin")
    bind=role_binding(cycle,work.get("role")); now=binding_digest(bind)
    if now!=work.get("binding_digest"):
        raise SystemExit("AGENT_WORK: STALE\nauthoritative workflow inputs changed; start/reconcile a new work item instead of replaying the old checkpoint")
    ref=state.get("active_external_work") or {}
    if ref.get("work_id")!=work.get("work_id") or ref.get("checkpoint_seq")!=work.get("checkpoint_seq"):
        raise SystemExit("AGENT_WORK: STALE\nSTATE.json pointer/sequence differs from AGENT_WORK.json")

def cmd_status(_a):
    state=load_state(); cid,cycle=active_cycle(state); work=load_work()
    if not work: print("AGENT_WORK: NONE"); return
    try: verify_current(state,cycle,work); valid=True
    except SystemExit as exc: print(str(exc)); valid=False
    for k in ["work_id","role","status","phase","current_unit","next_unit","checkpoint_seq","resume_artifact"]: print(f"{k}: {work.get(k)}")
    print(f"binding_valid: {str(valid).lower()}")

def cmd_checkpoint(a):
    state=load_state(); cid,cycle=active_cycle(state); work=load_work(); verify_current(state,cycle,work)
    if work.get("status")=="COMPLETED": raise SystemExit("AGENT_WORK: BLOCKED\ncompleted work cannot be checkpointed")
    if a.expected_seq!=work.get("checkpoint_seq"): raise SystemExit(f"AGENT_WORK: STALE\nexpected checkpoint_seq {work.get('checkpoint_seq')}, received {a.expected_seq}")
    work["checkpoint_seq"]+=1; work["status"]="CHECKPOINTED"; work["phase"]=a.phase or work.get("phase"); work["current_unit"]=a.unit; work["next_unit"]=a.next_unit; work["updated_at"]=utc_now(); work["last_agent"]={"tool":a.tool,"model":a.model}; work["git"]=git_snapshot()
    write_json(WORK_PATH,work); write_resume(work["resume_artifact"],work,a.note)
    ref=state["active_external_work"]; ref.update({"status":"CHECKPOINTED","checkpoint_seq":work["checkpoint_seq"],"binding_digest":work["binding_digest"]}); save_state(state)
    append_transition("EXTERNAL_AGENT_CHECKPOINT",actor="agent:agent_work",cycle_id=cid,details={"work_id":work["work_id"],"role":work["role"],"checkpoint_seq":work["checkpoint_seq"],"phase":work["phase"],"unit":a.unit,"next_unit":a.next_unit})
    print("AGENT_WORK: CHECKPOINTED"); print(f"checkpoint_seq: {work['checkpoint_seq']}"); print(f"next_unit: {work.get('next_unit')}")

def cmd_resume(a):
    state=load_state(); cid,cycle=active_cycle(state); work=load_work(); verify_current(state,cycle,work)
    if work.get("status")=="COMPLETED": raise SystemExit("AGENT_WORK: BLOCKED\nwork already completed")
    work["status"]="IN_PROGRESS"; work["updated_at"]=utc_now(); work["last_agent"]={"tool":a.tool,"model":a.model}; write_json(WORK_PATH,work)
    state["active_external_work"]["status"]="IN_PROGRESS"; save_state(state); append_transition("EXTERNAL_AGENT_WORK_RESUMED",actor="agent:agent_work",cycle_id=cid,details={"work_id":work["work_id"],"role":work["role"],"checkpoint_seq":work["checkpoint_seq"],"tool":a.tool,"model":a.model})
    print("AGENT_WORK: RESUMED"); print(f"resume_artifact: {work['resume_artifact']}"); print(f"next_unit: {work.get('next_unit')}")

def cmd_complete(a):
    state=load_state(); cid,cycle=active_cycle(state); work=load_work(); verify_current(state,cycle,work)
    if a.expected_seq!=work.get("checkpoint_seq"): raise SystemExit(f"AGENT_WORK: STALE\nexpected checkpoint_seq {work.get('checkpoint_seq')}, received {a.expected_seq}")
    work["checkpoint_seq"]+=1; work["status"]="COMPLETED"; work["phase"]=a.phase or "COMPLETE"; work["current_unit"]=a.unit; work["next_unit"]=None; work["updated_at"]=utc_now(); work["completed_at"]=utc_now(); work["last_agent"]={"tool":a.tool,"model":a.model}; work["git"]=git_snapshot()
    write_json(WORK_PATH,work); write_resume(work["resume_artifact"],work,a.note)
    state["active_external_work"].update({"status":"COMPLETED","checkpoint_seq":work["checkpoint_seq"]}); save_state(state)
    append_transition("EXTERNAL_AGENT_WORK_COMPLETED",actor="agent:agent_work",cycle_id=cid,details={"work_id":work["work_id"],"role":work["role"],"checkpoint_seq":work["checkpoint_seq"]})
    print("AGENT_WORK: COMPLETED"); print(f"work_id: {work['work_id']}")

def main():
    ap=argparse.ArgumentParser(description="provider-neutral External Agent resumability")
    sub=ap.add_subparsers(dest="cmd",required=True)
    b=sub.add_parser("begin"); b.add_argument("--role",required=True,choices=sorted(ROLES)); b.add_argument("--phase"); b.add_argument("--next-unit"); b.add_argument("--tool",default="unspecified"); b.add_argument("--model",default="unspecified"); b.set_defaults(func=cmd_begin)
    s=sub.add_parser("status"); s.set_defaults(func=cmd_status)
    c=sub.add_parser("checkpoint"); c.add_argument("--expected-seq",type=int,required=True); c.add_argument("--phase"); c.add_argument("--unit",required=True); c.add_argument("--next-unit"); c.add_argument("--note",required=True); c.add_argument("--tool",default="unspecified"); c.add_argument("--model",default="unspecified"); c.set_defaults(func=cmd_checkpoint)
    r=sub.add_parser("resume"); r.add_argument("--tool",default="unspecified"); r.add_argument("--model",default="unspecified"); r.set_defaults(func=cmd_resume)
    f=sub.add_parser("complete"); f.add_argument("--expected-seq",type=int,required=True); f.add_argument("--phase"); f.add_argument("--unit",required=True); f.add_argument("--note",required=True); f.add_argument("--tool",default="unspecified"); f.add_argument("--model",default="unspecified"); f.set_defaults(func=cmd_complete)
    a=ap.parse_args(); a.func(a)
if __name__=="__main__": main()
