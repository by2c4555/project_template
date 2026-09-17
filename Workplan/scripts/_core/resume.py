from .state import load_state
from .paths import WORK_DIR
import json

def project_resume():
    st=load_state(); out={'resume_status':'READY','state_seq':st['state_seq'],'stage':st.get('lifecycle_stage'),'project_state':st.get('project_state'),'cycle':st.get('active_cycle'),'active_task':st.get('active_task'),'human_approval_required':False}
    pa=st.get('pending_approval')
    if pa:
        out.update({'resume_status':'HUMAN_APPROVAL_REQUIRED','approval_id':pa['approval_id'],'challenge':pa['challenge'],'risk_kind':pa['risk_kind'],'requested_action':pa['requested_action'],'human_approval_required':True})
        return out
    wid=st.get('active_work')
    if wid:
        meta=json.loads((WORK_DIR/wid/'WORK.json').read_text())
        out.update({'active_work':wid,'role':meta.get('role'),'checkpoint_seq':meta.get('checkpoint_seq'),'next_unit':meta.get('next_unit'),'reconciliation':'VERIFY_WORKTREE_AND_EVIDENCE'})
    else:
        out['next_action']=st.get('next_action') or 'FOLLOW_STAGE_PROTOCOL'
    return out
