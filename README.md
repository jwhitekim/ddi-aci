# DDI-ACI

**An Agent-Computer Interface for LLM Agents Operating a Drug–Drug Interaction Prediction Model**

DDI-ACI is a model-specific agent-computer interface (ACI) that lets an LLM agent operate [DSN-DDI](https://github.com/microsoft/Drug-Interaction-Research/tree/DSN-DDI-for-DDI-Prediction), a drug–drug interaction (DDI) prediction model, and report its output faithfully. Neither DSN-DDI nor the OpenHands CodeActAgent is modified.

Paper: *DDI-ACI: An Agent-Computer Interface for LLM Agents Operating a Drug–Drug Interaction Prediction Model*, Jun-Hee Kim and Sang-Woong Lee (School of Computing, Gachon University).

[한국어 README](README_KO.md)

## Why

An LLM agent can run DSN-DDI successfully and still report a wrong answer. DSN-DDI outputs only a relation number (0–85). Turning that number into a sentence depends on repository conventions that produce no error when ignored:

- The description file (from SSI-DDI) has two numbering columns. DSN-DDI relation `t` maps to the row with `Interaction type == t + 1`, not to `DDI type N`.
- For 42 of the 86 relations (`Subject == 2`), the drug order in the sentence template is the reverse of the input order.
- Batching several pairs changes the predictions (the bipartite `GATConv` adds cross-pair edges), so pairs must be predicted one at a time.

DDI-ACI puts these rules inside the tool, so the agent gets a sentence with the correct direction and does not have to work them out from the files.

## Results (10 queries, Claude Sonnet 5.5)

All three conditions use the same LLM. Conditions B and C also share the same agent (OpenHands 0.62.0 CodeActAgent), task instruction, temperature 0.0 and default reasoning effort, with browsing and MCP tools disabled.

| | A. LLM only | B. Agent without ACI | C. Agent with DDI-ACI |
|---|---|---|---|
| **Success rate** | 10% | 70% | **100%** |
| Reached a result file | — | 10/10 | 10/10 |
| Avg. turns | — | 11.4 | 3.2 |
| Avg. prompt tokens (incl. cache reads) | — | 384,776 | 42,419 |
| Cost per query | $0.021 | $0.201 | $0.042 |

Success means the reported sentence has the same effect and the same drug direction as the model's top-1 prediction for the queried order. It measures agreement with the model output, not clinical validity. B obtained the right relation number in 10/10 queries but failed in three: in q01 and q02 it picked the preceding description row, and in q04 it reversed the drug roles.

Details: [`results/RESULTS.md`](results/RESULTS.md) · Evaluation spec: [`benchmarks/ddi/eval_spec.md`](benchmarks/ddi/eval_spec.md) · Answers side by side: [`results/v2/ANSWER_COMPARISON.md`](results/v2/ANSWER_COMPARISON.md)

### Limitations

This is a pilot study: one model (DSN-DDI), ten queries, one seed, and one run per query. The B–C difference is not statistically significant (exact McNemar test p = 0.25; three discordant queries favor C, none favor B). We did not test the reverse drug order or the seven symmetric `Subject = 3` types, and we did not separate the effects of C's tools and instructions. The task instruction and success criterion were finalized after a preliminary round of agent runs that is excluded from the reported results.

## Repository layout

| Path | Contents |
|---|---|
| `ddi-agent/` | Agent runner: launches OpenHands CodeActAgent for condition B or C (`run_agent.py`), config template, micro agent prompt for C |
| `ddi-tools/ddi/` | Tool interface the agent calls: the `ddi` Python package imported into the agent's IPython |
| `ddi-tools/server/` | Tool back end: prediction server wrapping the original DSN-DDI model and weights (Python 3.7) |
| `ddi-workspace/` | Execution environment: `ddi-runtime` image (B and C), `ddi-specialist` image (C), reproduction notes |
| `benchmarks/ddi/` | Evaluation: `run_infer.py` (run), `eval_infer.py` (score), `prompts/` (task instruction appended to every query), `data/` (questions, ground truth, relation map), `scripts/` |
| `results/` | Published results: scores per version (`v1/`, `v2/`), baseline A, raw v2 runs (`v2/raw/`) |
| `eval_outputs/` | New run outputs (not tracked by git) |
| `third_party/DSN-DDI/` | Original DSN-DDI repository (submodule) |
| `tests/` | Checks by target: `tools/` (`ddi` package, prediction server; run in containers), `workspace/` (OpenHands runtime), `layout/` (repository layout) |
| `openspec/` | Specs (`specs/`) and archived changes (`changes/archive/`) |

## The `ddi` skill

```python
res = ddi.predict("Warfarin", "Aspirin")
res["top"][0]["description"]
# 'Acetylsalicylic acid may increase the anticoagulant activities of Warfarin.'
```

| Function | Purpose |
|---|---|
| `resolve_drug(x)` | Name, synonym, DrugBank ID or SMILES → canonical drug |
| `predict(a, b, top_k=3)` | Top relations, per-relation probabilities, direction-aware sentences, warnings |
| `predict_many(pairs, relation=None)` | Predict many pairs one at a time, with an optional relation filter |
| `explain(rel, a, b)` | Relation number → direction-aware sentence |
| `save_results(res, path)` | Save results as a CSV for scoring |

It uses the transductive weights when both drugs are in the training set and otherwise switches to the inductive weights with a warning. It rejects unknown drugs and warns about atom features the model treats as unknown. Probabilities are per-relation sigmoids, so they do not sum to 1.

## Reproducing

Requirements: Linux, Docker with an NVIDIA GPU (the weights are stored as CUDA tensors), Python 3.12 for OpenHands.

```bash
# 1. Images
docker build -f ddi-workspace/Dockerfile -t ddi-runtime .                 # B and C
docker build -f ddi-workspace/Dockerfile.specialist -t ddi-specialist .   # C only

# 2. OpenHands environment
python3.12 -m venv .venv-openhands
.venv-openhands/bin/pip install -r ddi-agent/requirements.lock.txt
echo "AI_GATEWAY_API_KEY=..." > .env    # GEMINI_API_KEY is also needed for grading A

# 3. One query
.venv-openhands/bin/python ddi-agent/run_agent.py --condition C --task-suffix benchmarks/ddi/prompts/task_suffix.txt \
    --task "Warfarin이랑 Aspirin 상호작용 예측해줘" --out eval_outputs/try_C

# 4. Full evaluation
.venv-openhands/bin/python benchmarks/ddi/run_infer.py --condition C --workers 1
.venv-openhands/bin/python benchmarks/ddi/run_infer.py --condition B --workers 2
.venv-openhands/bin/python benchmarks/ddi/scripts/run_baseline_a.py
python3 benchmarks/ddi/eval_infer.py --runs-dir eval_outputs/ddi --out eval_outputs/ddi/scores

# Re-score the published v2 runs (results/v2/raw) into results/v2
python3 benchmarks/ddi/eval_infer.py
```

- Ground truth comes from the original DSN-DDI code, independent of the prediction server: `benchmarks/ddi/scripts/make_ground_truth.py` (see its docstring for the `docker run` command).
- The relation-number rule is checked against SSI-DDI pairs without using the rule itself: `benchmarks/ddi/scripts/verify_relation_map.py` (86/86 relations match, see [`benchmarks/ddi/data/relation_map/`](benchmarks/ddi/data/relation_map/README.md)).
- DSN-DDI reproduction (fold0 transductive ACC 0.973 vs. 0.969 reported): [`ddi-workspace/REPRODUCTION.md`](ddi-workspace/REPRODUCTION.md).

## Data and credits

- **DSN-DDI** — Li et al., *Briefings in Bioinformatics* 24(1), 2023. Model, weights and data from `microsoft/Drug-Interaction-Research` (commit `6f23522`).
- **SSI-DDI** — Nyamabo et al., *Briefings in Bioinformatics* 22(6), 2021. Relation descriptions (`Interaction_information.csv`).
- **DrugBank Vocabulary** (CC0) — drug names, via the copy in `ferrangoeh/DrugLinker`.
- **OpenHands** (0.62.0) and **CodeAct** — agent framework and action format.
- **SWE-agent** — the ACI concept this work extends.

This work was supported by the National Research Foundation of Korea (NRF) grant funded by the Korea government (MSIT) (RS-2025-00520064).

Most internal notes (`benchmarks/ddi/*.md`, `results/*.md`, `ddi-agent/SMOKE_TEST.md`, `ddi-workspace/REPRODUCTION.md`, code comments) are in Korean.
