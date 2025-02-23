import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data with config and benchmarks
sample_data = [
    {
        "modelName": "ModelA",
        "deploymentServer": "Server1",
        "description": "High-performance model",
        "llmProvider": "xAI",
        "llmModel": "Grok-A",
        "config": {
            "type": "advanced",
            "openai_auth_type": {"method": "api_key"},
            "openai_deployment_name": "deployA",
            "openai_api_base": "https://api.xai.com"
        },
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
        "config": {
            "type": "standard",
            "openai_auth_type": {"method": "oauth"},
            "openai_deployment_name": "deployB",
            "openai_api_base": "https://api.xai.com"
        },
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
    """Extract basic model information including config for table"""
    config_str = (
        f"Type: {model['config']['type']}, "
        f"Auth: {model['config']['openai_auth_type'].get('method', 'N/A')}, "
        f"Deployment: {model['config']['openai_deployment_name']}, "
        f"API Base: {model['config']['openai_api_base']}"
    )
    return {
        "Model Name": model["modelName"],
        "Server": model["deploymentServer"],
        "Description": model["description"],
        "Provider": model["llmProvider"],
        "LLM Model": model["llmModel"],
        "Endpoints": ", ".join(model["endpoints"]),
        "Config": config_str
    }


def get_benchmark_data(model, category):
    """Get benchmark data, handling different nesting structures"""
    if "category_benchmark" in model["metadata"]:
        return model["metadata"]["category_benchmark"].get(category, {})
    return model["metadata"].get(category, {})


def create_benchmark_table(data, category):
    """Create a table for a benchmark category with descriptions in brackets"""
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
                model_scores[metric] = f"{score} ({desc})" if desc else score
            else:
                model_scores[metric] = score_dict
        table_data[model["modelName"]] = model_scores

    return pd.DataFrame(table_data).T


def create_single_benchmark_chart(data, selected_categories):
    """Create a single bar chart for all selected benchmarks"""
    chart_data = []
    for category_key in selected_categories:
        for model in data:
            benchmark_data = get_benchmark_data(model, category_key)
            for metric, score_dict in benchmark_data.items():
                score = score_dict.get("score", score_dict) if isinstance(score_dict, dict) else score_dict
                score_value = float(score.strip("%")) if score and isinstance(score, str) else 0
                chart_data.append({
                    "Model": model["modelName"],
                    "Category": category_key.replace('_', ' ').title(),
                    "Metric": metric,
                    "Score": score_value
                })

    df = pd.DataFrame(chart_data)
    df["Category_Metric"] = df["Category"] + " - " + df["Metric"]

    fig = px.bar(
        df,
        x="Category_Metric",
        y="Score",
        color="Model",
        barmode="group",
        title="Benchmark Comparison Across Categories",
        labels={"Score": "Score (%)", "Category_Metric": "Category - Metric"},
        height=600
    )
    fig.update_layout(xaxis={'tickangle': 45})
    return fig


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

    # Sidebar Filters
    st.sidebar.header("Filters")

    # Model filter
    model_names = [model["modelName"] for model in sample_data]
    selected_models = st.sidebar.multiselect("Select Models", model_names, default=model_names)
    filtered_data = [model for model in sample_data if model["modelName"] in selected_models]

    # Category filter
    categories = [
        ("information_extraction", "Information Extraction"),
        ("language_understanding", "Language Understanding"),
        ("question_answering", "Question Answering"),
        ("logical_reasoning", "Logical Reasoning"),
        ("code_generation", "Code Generation")
    ]
    category_options = [title for _, title in categories]
    selected_categories = st.sidebar.multiselect("Select Categories", category_options, default=category_options)
    filtered_categories = [key for key, title in categories if title in selected_categories]

    # Basic Information Table
    st.header("Model Information")
    basic_info = [extract_basic_info(model) for model in filtered_data]
    st.dataframe(pd.DataFrame(basic_info), use_container_width=True)

    # Benchmark Tables
    st.header("Benchmark Results")
    st.markdown("*Descriptions appear in brackets next to scores when available*")

    for category_key in filtered_categories:
        exists = any(category_key in get_benchmark_data(model, category_key) or
                     category_key in model["metadata"] for model in filtered_data)
        if exists:
            category_title = next(title for key, title in categories if key == category_key)
            st.subheader(category_title)
            df = create_benchmark_table(filtered_data, category_key)
            height = min(400, max(100, len(df) * 35))
            st.dataframe(df, use_container_width=True, height=height)

    # Single Benchmark Chart
    if filtered_categories and filtered_data:
        st.header("Benchmark Visualization")
        fig = create_single_benchmark_chart(filtered_data, filtered_categories)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
