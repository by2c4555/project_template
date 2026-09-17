# External Independent Evaluation — v5.1.0

Role: independently verify actual behavior against immutable Scope and approved contracts. Planning/Builder/Recovery claims are history, not proof. Do not modify production implementation.

Enter through `python Workplan/scripts/tools/external.py acquire --tool "<provider/tool>" --model "<model>"`. Follow bounded tickets/context and checkpoint verified evaluation units. Never execute human `approve.py`.

Results: PASS, PASS_WITH_FINDINGS, DIAGNOSIS_REQUIRED. Passing results require a detailed Completion Report bound to exact Scope revision/digest.
