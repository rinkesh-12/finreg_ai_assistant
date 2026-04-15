import os, json
from langsmith import Client
from langsmith.evaluation import evaluate, LangChainStringEvaluator
from langsmith.schemas import Example
from app.chatbot_chain import get_predictor

# Prefer LANGSMITH_API_KEY or LANGCHAIN_API_KEY.
client = Client()

# load dataset
with open("evaluation/faq_dataset.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

examples = []
for i, row in enumerate(dataset):
    # note: inputs must match target signature. Our predictor expects key "input"
    examples.append(Example(inputs={"input": row["question"]}, outputs={"answer": row["answer"]}))

# get your predictor (target function)
predict = get_predictor(faiss_folder="data/faiss_index")  # returns function(inputs:dict)->dict

# define a strict string match evaluator (row-level)
def strict_match(run, example):
    pred = (run.outputs.get("output") or "").strip()
    expected = (example.outputs.get("answer") or "").strip()
    score = 1 if pred.lower() == expected.lower() else 0
    return {"score": score, "reason": f"pred_len={len(pred)}, expected_len={len(expected)}"}

# langchain/ LangSmith off-the-shelf QA evaluator
qa_eval = LangChainStringEvaluator("qa")  # semantic QA evaluator (prebuilt). :contentReference[oaicite:8]{index=8}

# run evaluation
results = evaluate(
    predict,                    # target fn that accepts dict -> dict
    data=examples,              # list of langsmith.schemas.Example
    evaluators=[strict_match, qa_eval],
    experiment_prefix="RBI-NBFC-Eval",
    description="RAG vs RBI FAQ (small set)",
    client=client,
    upload_results=False        # set True to upload to LangSmith UI; False to run locally
)

print("Done. Results:", results)
