# v4.0.1 Provider Binding Patch

Replace the matching files in an existing Project Template v4.0.1 workspace.

## Required runtime files

- `EXECUTE/MODEL_BINDINGS.json`
- `EXECUTE/PROJECT_CONFIG.md`
- `scripts/configure_models.py`
- `scripts/validate_v4.py`
- `.github/agents/planner512k.agent.md`
- `.github/agents/builder128k.agent.md`
- `.github/agents/builder256k.agent.md`

## Documentation updates

- `README.md`
- `CHANGELOG.md`

## Example: force Planner and Builders through OpenRouter

```bash
python scripts/configure_models.py \
  --planner-model "Claude Opus 4.7" --planner-provider openrouter --planner-context 1048576 \
  --builder128-model "Qwen3 Coder Next" --builder128-provider openrouter --builder128-context 262144 \
  --builder256-model "Qwen3 Coder Next" --builder256-provider openrouter --builder256-context 262144
```

Then run:

```bash
python scripts/validate_v4.py
```

Expected after successful binding:

```text
STRUCTURE_VALIDATION: PASS
ARCHITECTURE_VALIDATION: PASS
POLICY_VALIDATION: PASS
MODEL_BINDING_VALIDATION: PASS
RUNTIME_READY: YES
TEMPLATE_VALID: PASS (v4.0.1)
```

To force the Copilot copy of the Planner model instead, change only:

```text
--planner-provider copilot
```

This produces:

```text
Claude Opus 4.7 (copilot)
```

The provider/vendor identifier is part of the binding and must match the identifier recognized by VS Code.
