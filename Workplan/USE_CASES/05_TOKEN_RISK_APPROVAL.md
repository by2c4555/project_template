# Token-Risk Approval

A deterministic risk gate creates one pending `APPROVAL_xxxx`. AI obtains it with `tools/approve_req.py --id ...`, displays the challenge, and stops. Human runs `python Workplan/scripts/approve.py -- NNNNNN`. AI checks `approve_res.py`. AI never invokes the human script.
