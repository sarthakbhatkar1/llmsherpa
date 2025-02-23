import streamlit as st
import json
import pandas as pd

# Sample data with multiple entries
sample_data = [
    {
        "modelName": "ModelA",
        "deploymentServer": "Server1",
        "description": "High-performance model",
        "llmProvider": "xAI",
        "llmModel": "Grok-A",
        "config": {"type": "advanced", "openai_auth_type": {}, "openai_deployment_name": "deployA",
                   "openai_api_base": "https://api.xai.com"},
        "endpoints": ["chat", "completions"],
        "metadata": {
            "information_extraction": {"EntityRec": "85%", "RelationExt": "82%"},
            "language_understanding": {"MMLU": {"score": "78%"}, "GPQA": {"score": "82%"}},
            "question_answering": {"MGSM": {"score": "75%"}, "TriviaQA": {"score": "80%"}},
            "logical_reasoning": {"LogicTest": "88%", "ARG": "85%"},
            "code_generation": {"HumanEval": {"score": "91%"}, "MBPP": {"score": "87%"}}
        }
    },
    {
        "modelName": "ModelB",
        "deploymentServer": "Server2",
        "description": "Efficient model",
        "llmProvider": "xAI",
        "llmModel": "Grok-B",
        "config": {"type": "standard", "openai_auth_type": {}, "openai_deployment_name": "deployB",
                   "openai_api_base": "https://api.xai.com"},
        "endpoints": ["chat", "completions"],
        "metadata": {
            "information_extraction": {"EntityRec": "88%", "RelationExt": "79%"},
            "language_understanding": {"MMLU": {"score": "82%"}, "GPQA": {"score": "79%"}},
            "question_answering": {"MGSM": {"score": "80%"}, "TriviaQA": {"score": "83%"}},
            "logical_reasoning": {"LogicTest": "85%", "ARG": "82%"},
            "code_generation": {"HumanEval": {"score": "87%"}, "MBPP": {"score": "90%"}}
        }
    },
    {
        "modelName": "ModelC",
        "deploymentServer": "Server3",
        "description": "Balanced model",
        "llmProvider": "xAI",
        "llmModel": "Grok-C",
        "config": {"type": "hybrid", "openai_auth_type": {}, "openai_deployment_name": "deployC",
                   "openai_api_base": "https://api.xai.com"},
        "endpoints": ["chat", "completions"],
        "metadata": {
            "information_extraction": {"EntityRec": "86%", "RelationExt": "84%"},
            "language_understanding": {"MMLU": {"score": "80%"}, "GPQA": {"score": "81%"}},
            "question_answering": {"MGSM": {"score": "78%"}, "TriviaQA": {"score": "82%"}},
            "logical_reasoning": {"LogicTest": "87%", "ARG": "83%"},
            "code_generation": {"HumanEval": {"score": "89%"}, "MBPP": {"score": "88%"}}
        }
    }
]


def extract_basic_info(model):
    """Extract basic model information for table"""
    return {
        "Model Name": model["modelName"],
        "Server": model["deploymentServer"],
        "Description": model["description"],
        "Provider": model["llmProvider"],
        "LLM Model": model["llmModel"],
        "Endpoints": ", ".join(model["endpoints"])
    }


def create_benchmark_table(data, category):
    """Create a dynamic table for a benchmark category"""
    all_metrics = set()
    for model in data:
        all_metrics.update(model["metadata"][category].keys())

    table_data = {}
    for model in data:
        model_scores = {}
        for metric in all_metrics:
            score = model["metadata"][category].get(metric, {})
            model_scores[metric] = score.get("score", score) if isinstance(score, dict) else score
        table_data[model["modelName"]] = model_scores

    return pd.DataFrame(table_data).T


def main():
    # Page config
    st.set_page_config(
        page_title="Dynamic Model Benchmark Dashboard",
        page_icon="📋",
        layout="wide"
    )

    # Title
    st.title("Dynamic Model Benchmark Dashboard")
    st.markdown("Compare benchmarks across multiple AI models in tabular format")

    # Sidebar
    st.sidebar.header("Options")
    uploaded_file = st.sidebar.file_uploader("Upload JSON file", type=['json'])

    # Load data
    data = json.load(uploaded_file) if uploaded_file else sample_data

    # Model selection
    model_names = [model["modelName"] for model in data]
    selected_models = st.sidebar.multiselect("Select Models", model_names, default=model_names)
    filtered_data = [model for model in data if model["modelName"] in selected_models]

    # Basic Information Table
    st.header("Model Information")
    basic_info = [extract_basic_info(model) for model in filtered_data]
    st.dataframe(pd.DataFrame(basic_info), use_container_width=True)

    # Benchmark Tables
    st.header("Benchmark Results")
    categories = [
        ("information_extraction", "Information Extraction"),
        ("language_understanding", "Language Understanding"),
        ("question_answering", "Question Answering"),
        ("logical_reasoning", "Logical Reasoning"),
        ("code_generation", "Code Generation")
    ]

    for category_key, category_title in categories:
        if filtered_data and category_key in filtered_data[0]["metadata"]:
            st.subheader(category_title)
            df = create_benchmark_table(filtered_data, category_key)
            st.dataframe(df, use_container_width=True)

    # Raw data view
    with st.expander("View Raw JSON Data"):
        st.json(filtered_data)


if __name__ == "__main__":
    main()
