# External Diagnosis — v5.1.0

Role: reproduce/verify the failure, narrow hypotheses with evidence, identify the smallest supported root cause and classify it. Do not repair production code.

Enter through `python Workplan/scripts/tools/external.py acquire --tool "<provider/tool>" --model "<model>"`. Follow the returned ticket, checkpoint verified semantic units and request only bounded context. Never execute human `approve.py`.

Classify one: IMPLEMENTATION_DEFECT, TASK_DEFECT, PLAN_DEFECT, EVALUATION_DEFECT, SCOPE_AMBIGUITY, EXTERNAL_BLOCKER, UNKNOWN.
