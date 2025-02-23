import streamlit as st
import json
import pandas as pd

# Sample data reflecting the structure with descriptions
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
            "language_understanding": {
                "MMLU": {"score": "78%", "description": "Multi-task language understanding"},
                "GPQA": {"score": "82%", "description": "General-purpose question answering"}
            },
            "question_answering": {
                "MGSM": {"score": "75%", "description": "Math problem solving"},
                "TriviaQA": {"score": "80%"}
            },
            "logical_reasoning": {"LogicTest": "88%", "ARG": "85%"},
            "code_generation": {
                "HumanEval": {"score": "91%", "description": "Code completion accuracy"},
                "MBPP": {"score": "87%"}
            }
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
            "category_benchmark": {
                "information_extraction": {"EntityRec": "88%", "RelationExt": "79%"},
                "language_understanding": {
                    "MMLU": {"score": "82%", "description": "Multi-task language understanding"},
                    "GPQA": {"score": "79%", "description": "General-purpose QA"}
                },
                "question_answering": {
                    "MGSM": {"score": "80%", "description": "Mathematical reasoning"},
                    "TriviaQA": {"score": "83%"}
                },
                "logical_reasoning": {"LogicTest": "85%", "ARG": "82%"},
                "code_generation": {
                    "HumanEval": {"score": "87%", "description": "Programming tasks"},
                    "MBPP": {"score": "90%"}
                }
            }
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


def get_benchmark_data(model, category):
    """Get benchmark data, handling different nesting structures"""
    if "category_benchmark" in model["metadata"]:
        return model["metadata"]["category_benchmark"].get(category, {})
    return model["metadata"].get(category, {})


def create_benchmark_table(data, category):
    """Create a dynamic table for a benchmark category with descriptions in brackets"""
    all_metrics = set()
    for model in data:
        benchmark_data = get_benchmark_data(model, category)
        all_metrics.update(benchmark_data.keys())

    table_data = {}
    for model in data:
        model_scores = {}
        benchmark_data = get_benchmark_data(model, category)
        for metric in all_metrics:
            score_dict = benchmark_data.get(metric, {})
            if isinstance(score_dict, dict):
                score = score_dict.get("score", "")
                desc = score_dict.get("description", "")
                # Combine score and description in brackets if description exists
                model_scores[metric] = f"{score} ({desc})" if desc else score
            else:
                model_scores[metric] = score_dict
        table_data[model["modelName"]] = model_scores

    df = pd.DataFrame(table_data).T
    return df


def main():
    # Page config
    st.set_page_config(
        page_title="Dynamic Model Benchmark Dashboard",
        page_icon="📋",
        layout="wide"
    )

    # Title
    st.title("Dynamic Model Benchmark Dashboard")
    st.markdown("Compare benchmarks across models with descriptions in brackets")

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
    st.markdown("*Descriptions appear in brackets next to scores when available*")
    categories = [
        ("information_extraction", "Information Extraction"),
        ("language_understanding", "Language Understanding"),
        ("question_answering", "Question Answering"),
        ("logical_reasoning", "Logical Reasoning"),
        ("code_generation", "Code Generation")
    ]

    for category_key, category_title in categories:
        exists = any(category_key in get_benchmark_data(model, category_key) or
                     category_key in model["metadata"] for model in filtered_data)
        if exists:
            st.subheader(category_title)
            df = create_benchmark_table(filtered_data, category_key)
            # Adjust height based on number of rows
            height = min(400, max(100, len(df) * 35))  # Adjusted height for single-line display
            st.dataframe(df, use_container_width=True, height=height)

    # Raw data view
    with st.expander("View Raw JSON Data"):
        st.json(filtered_data)


if __name__ == "__main__":
    main()

