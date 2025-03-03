import streamlit as st
import pandas as pd
import plotly.express as px

# Your JSON data
sample_data = [
    {
        "modelName": "AlphaModel",
        "deploymentServer": "Server1",
        "description": "Advanced language processing model",
        "llmProvider": "xAI",
        "llmModel": "Grok-3",
        "config": {
            "type": "standard",
            "openai_auth_type": {"key": "api_key"},
            "openai_deployment_name": "alpha-deploy",
            "openai_api_base": "https://api.xai.com"
        },
        "endpoints": ["chat", "completions", "embeddings"],
        "metadata": {
            "feature": {
                "creator": "xAI Team",
                "license": "MIT",
                "contextWindow": "8192",
                "supportedModality": ["text", "code"],
                "version": "3.1"
            },
            "externalBenchmark": {
                "informationExtraction": {"IEBench": {"metric": {"score": "0.92", "source": "IE2024"}}},
                "languageUnderstanding": {"MMLU": {"metric": {"score": "0.85", "source": "MMLU2023"}}},
                "questionAnswering": {"SQuAD": {"metric": {"score": "0.89", "source": "SQuAD2.0"}}},
                "logicalReasoning": {"LogicTest": {"metric": {"score": "0.78", "source": "LT2024"}}},
                "codeGeneration": {"HumanEval": {"metric": {"score": "0.82", "source": "HE2023"}}},
                "textEmbeddingRetrieval": {"TERBench": {"metric": {"score": "0.91", "source": "TER2024"}}}
            },
            "bionicsBenchmark": {}
        }
    },
    {
        "modelName": "BetaModel",
        "deploymentServer": "Server2",
        "description": "Specialized code generation model",
        "llmProvider": "BetaCorp",
        "llmModel": "CodeMaster",
        "config": {
            "type": "optimized",
            "openai_auth_type": {"key": "token"},
            "openai_deployment_name": "beta-deploy",
            "openai_api_base": "https://api.betacorp.com"
        },
        "endpoints": ["chat", "completions"],
        "metadata": {
            "feature": {
                "creator": "Beta Team",
                "license": "Apache 2.0",
                "contextWindow": "4096",
                "supportedModality": ["code", "text"],
                "version": "1.5"
            },
            "externalBenchmark": {
                "informationExtraction": {"IEBench": {"metric": {"score": "0.87", "source": "IE2024"}}},
                "languageUnderstanding": {"MMLU": {"metric": {"score": "0.79", "source": "MMLU2023"}}},
                "questionAnswering": {"SQuAD": {"metric": {"score": "0.83", "source": "SQuAD2.0"}}},
                "logicalReasoning": {"LogicTest": {"metric": {"score": "0.85", "source": "LT2024"}}},
                "codeGeneration": {"HumanEval": {"metric": {"score": "0.94", "source": "HE2023"}}},
                "textEmbeddingRetrieval": {"TERBench": {"metric": {"score": "0.88", "source": "TER2024"}}}
            },
            "bionicsBenchmark": {}
        }
    },
    {
        "modelName": "GammaModel",
        "deploymentServer": "Server3",
        "description": "General purpose AI assistant",
        "llmProvider": "GammaAI",
        "llmModel": "Assist-1",
        "config": {
            "type": "basic",
            "openai_auth_type": {"key": "secret"},
            "openai_deployment_name": "gamma-deploy",
            "openai_api_base": "https://api.gammaai.com"
        },
        "endpoints": ["chat"],
        "metadata": {
            "feature": {
                "creator": "Gamma Team",
                "license": "GPL",
                "contextWindow": "16384",
                "supportedModality": ["text"],
                "version": "2.0"
            },
            "externalBenchmark": {
                "informationExtraction": {"IEBench": {"metric": {"score": "0.88", "source": "IE2024"}}},
                "languageUnderstanding": {"MMLU": {"metric": {"score": "0.91", "source": "MMLU2023"}}},
                "questionAnswering": {"SQuAD": {"metric": {"score": "0.93", "source": "SQuAD2.0"}}},
                "logicalReasoning": {"LogicTest": {"metric": {"score": "0.82", "source": "LT2024"}}},
                "codeGeneration": {"HumanEval": {"metric": {"score": "0.76", "source": "HE2023"}}},
                "textEmbeddingRetrieval": {"TERBench": {"metric": {"score": "0.85", "source": "TER2024"}}}
            },
            "bionicsBenchmark": {}
        }
    }
]


def extract_basic_info(model):
    """Extract basic model information including config and features for table"""
    config_str = (
        f"Type: {model['config']['type']}, "
        f"Auth: {model['config']['openai_auth_type'].get('key', 'N/A')}, "
        f"Deployment: {model['config']['openai_deployment_name']}, "
        f"API Base: {model['config']['openai_api_base']}"
    )
    features = model.get('metadata', {}).get('feature', {})
    return {
        "Model Name": model["modelName"],
        "Server": model["deploymentServer"],
        "Description": model["description"],
        "Provider": model["llmProvider"],
        "LLM Model": model["llmModel"],
        "Endpoints": ", ".join(model["endpoints"]),
        "Config": config_str,
        "Creator": features.get("creator", ""),
        "License": features.get("license", ""),
        "Context Window": features.get("contextWindow", ""),
        "Supported Modality": ", ".join(features.get("supportedModality", [])),
        "Version": features.get("version", "")
    }


def get_benchmark_data(model, category):
    """Get benchmark data from externalBenchmark structure"""
    return model["metadata"]["externalBenchmark"].get(category, {})


def create_benchmark_table(data, category):
    """Create a table for a benchmark category with sources in brackets"""
    all_metrics = set()
    table_data = {}

    # Collect all unique metrics across models
    for model in data:
        benchmark_data = get_benchmark_data(model, category)
        all_metrics.update(benchmark_data.keys())

    # Build table data
    for model in data:
        model_scores = {}
        benchmark_data = get_benchmark_data(model, category)
        for metric in all_metrics:
            if metric in benchmark_data:
                score = benchmark_data[metric]["metric"]["score"]
                source = benchmark_data[metric]["metric"]["source"]
                model_scores[metric] = f"{float(score) * 100}% ({source})"
            else:
                model_scores[metric] = "N/A"
        table_data[model["modelName"]] = model_scores

    return pd.DataFrame(table_data).T


def create_single_benchmark_chart(data, selected_categories):
    """Create a single bar chart for all selected benchmarks"""
    chart_data = []
    for category_key in selected_categories:
        for model in data:
            benchmark_data = get_benchmark_data(model, category_key)
            for metric, score_dict in benchmark_data.items():
                score = score_dict["metric"]["score"]
                score_value = float(score) * 100  # Convert to percentage
                chart_data.append({
                    "Model": model["modelName"],
                    "Category": category_key.replace('ation', '').replace('ing', '').title(),
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
    st.markdown("Compare benchmarks across models with sources in brackets")

    # Sidebar Filters
    st.sidebar.header("Filters")

    # Model filter
    model_names = [model["modelName"] for model in sample_data]
    selected_models = st.sidebar.multiselect("Select Models", model_names, default=model_names)
    filtered_data = [model for model in sample_data if model["modelName"] in selected_models]

    # Category filter
    categories = [
        ("informationExtraction", "Information Extraction"),
        ("languageUnderstanding", "Language Understanding"),
        ("questionAnswering", "Question Answering"),
        ("logicalReasoning", "Logical Reasoning"),
        ("codeGeneration", "Code Generation"),
        ("textEmbeddingRetrieval", "Text Embedding Retrieval")
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
    st.markdown("*Sources appear in brackets next to scores*")

    for category_key in filtered_categories:
        exists = any(bool(get_benchmark_data(model, category_key)) for model in filtered_data)
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
