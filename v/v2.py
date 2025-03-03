import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# Sample data with 'source' and 'url' fields
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
                "informationExtraction": {
                    "IEBench": {"metric": {"score": "0.92", "source": "IE2024", "url": "https://ie2024.org",
                                           "additionalDetails": {"date": "2024-01"}}},
                    "NERTest": {"metric": {"score": "0.89", "source": "NER2023"}}
                },
                "languageUnderstanding": {
                    "MMLU": {"metric": {"score": "0.85", "source": "MMLU2023", "url": "https://mmlu.org"}},
                    "GLUE": {"metric": {"score": "0.87", "source": "GLUE2023"}}
                },
                "questionAnswering": {
                    "SQuAD": {"metric": {"score": "0.89", "source": "SQuAD2.0", "url": "https://squad.stanford.edu"}}
                },
                "logicalReasoning": {
                    "LogicTest": {"metric": {"score": "0.78", "source": "LT2024"}}
                },
                "codeGeneration": {
                    "HumanEval": {"metric": {"score": "0.82", "source": "HE2023", "url": "https://humaneval.org"}},
                    "MBPP": {"metric": {"score": "0.80", "source": "MBPP2023"}}
                },
                "textEmbeddingRetrieval": {
                    "TERBench": {"metric": {"score": "0.91", "source": "TER2024"}}
                }
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
                "informationExtraction": {
                    "IEBench": {"metric": {"score": "0.87", "source": "IE2024", "url": "https://ie2024.org"}}
                },
                "languageUnderstanding": {
                    "MMLU": {"metric": {"score": "0.79", "source": "MMLU2023"}}
                },
                "questionAnswering": {},
                "logicalReasoning": {
                    "LogicTest": {"metric": {"score": "0.85", "source": "LT2024"}},
                    "ReasonX": {"metric": {"score": "0.83", "source": "RX2023"}},
                    "ARG": {"metric": {"score": "0.80", "source": "ARG2023"}}
                },
                "codeGeneration": {
                    "HumanEval": {"metric": {"score": "0.94", "source": "HE2023", "url": "https://humaneval.org"}},
                    "CodeX": {"metric": {"score": "0.91", "source": "CX2023"}}
                },
                "textEmbeddingRetrieval": {
                    "TERBench": {"metric": {"score": "0.88", "source": "TER2024"}},
                    "EmbedTest": {"metric": {"score": "0.86", "source": "ET2023"}}
                }
            },
            "bionicsBenchmark": {}
        }
    }
]


def extract_basic_info(model):
    """Extract basic model information including config and features"""
    config = model.get('config', {})
    config_str = (
        f"Type: {config.get('type', 'N/A')}, "
        f"Auth: {config.get('openai_auth_type', {}).get('key', 'N/A')}, "
        f"Deployment: {config.get('openai_deployment_name', 'N/A')}, "
        f"API Base: {config.get('openai_api_base', 'N/A')}"
    )
    features = model.get('metadata', {}).get('feature', {})
    return {
        "Model Name": model.get("modelName", "N/A"),
        "Server": model.get("deploymentServer", "N/A"),
        "Description": model.get("description", "N/A"),
        "Provider": model.get("llmProvider", "N/A"),
        "LLM Model": model.get("llmModel", "N/A"),
        "Endpoints": ", ".join(model.get("endpoints", [])) if model.get("endpoints") else "N/A",
        "Config": config_str,
        "Creator": features.get("creator", "N/A"),
        "License": features.get("license", "N/A"),
        "Context Window": features.get("contextWindow", "N/A"),
        "Supported Modality": ", ".join(features.get("supportedModality", [])) if features.get(
            "supportedModality") else "N/A",
        "Version": features.get("version", "N/A")
    }


def get_benchmark_data(model, category):
    """Get benchmark data from externalBenchmark with fallback"""
    return model.get("metadata", {}).get("externalBenchmark", {}).get(category, {})


def create_benchmark_html_table(data, category):
    """Create an HTML table string with scores and source links"""
    all_metrics = set()

    for model in data:
        benchmark_data = get_benchmark_data(model, category)
        if benchmark_data:
            all_metrics.update(benchmark_data.keys())

    if not all_metrics:
        return None

    metrics = sorted(all_metrics - {"<benchmark_name>"})
    if not metrics:
        return None

    # Build HTML table
    html = """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            font-family: Arial, sans-serif;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
            vertical-align: middle;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        a {
            font-size: 12px;
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
    <table>
        <tr>
            <th>Model</th>
    """
    # Add metric headers
    for metric in metrics:
        html += f"<th>{metric}</th>"
    html += "</tr>"

    # Add data rows
    for model in data:
        html += f"<tr><td>{model['modelName']}</td>"
        benchmark_data = get_benchmark_data(model, category)
        for metric in metrics:
            if benchmark_data and metric in benchmark_data:
                metric_data = benchmark_data[metric].get("metric", {})
                score = metric_data.get("score", "N/A")
                source = metric_data.get("source", "N/A")
                url = metric_data.get("url", None)
                if score != "N/A" and score:
                    try:
                        score = f"{float(score) * 100}%"
                        if url:
                            cell_content = f"{score}<br><a href='{url}' target='_blank'>{source}</a>"
                        else:
                            cell_content = f"{score}<br>{source}"
                        html += f"<td>{cell_content}</td>"
                    except (ValueError, TypeError):
                        html += "<td>N/A</td>"
                else:
                    html += "<td>N/A</td>"
            else:
                html += "<td>N/A</td>"
        html += "</tr>"

    html += "</table>"
    return html


def create_single_benchmark_chart(data, selected_categories):
    """Create a bar chart for all selected benchmarks with multiple metrics"""
    chart_data = []
    for category_key in selected_categories:
        for model in data:
            benchmark_data = get_benchmark_data(model, category_key)
            if benchmark_data:
                for metric, score_dict in benchmark_data.items():
                    if metric != "<benchmark_name>":
                        metric_data = score_dict.get("metric", {})
                        score = metric_data.get("score", "N/A")
                        if score != "N/A" and score:
                            try:
                                score_value = float(score) * 100
                                chart_data.append({
                                    "Model": model["modelName"],
                                    "Category": category_key.replace('ation', '').replace('ing', '').title(),
                                    "Metric": metric,
                                    "Score": score_value
                                })
                            except (ValueError, TypeError):
                                continue

    if not chart_data:
        return None

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
        height=600,
        width=1200
    )
    fig.update_layout(
        xaxis={'tickangle': 45},
        bargap=0.2,
        legend_title_text='Model'
    )
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
    st.markdown("Explore multiple benchmarks per category with source links in cells using components.html")

    # Sidebar Filters
    st.sidebar.header("Filters")

    # Model filter
    model_names = [model["modelName"] for model in sample_data if model["modelName"]]
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
    st.markdown("*Scores with source links below in each cell (clickable if URL exists) using components.html.*")

    for category_key in filtered_categories:
        category_title = next(title for key, title in categories if key == category_key)
        st.subheader(category_title)
        html_table = create_benchmark_html_table(filtered_data, category_key)
        if html_table:
            components.html(html_table, height=min(400, max(100, len(filtered_data) * 50)))
        else:
            st.write("No valid benchmark data available for this category.")

    # Benchmark Chart
    if filtered_categories and filtered_data:
        st.header("Benchmark Visualization")
        fig = create_single_benchmark_chart(filtered_data, filtered_categories)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No valid benchmark data available for visualization.")

    # Raw JSON View
    if st.checkbox("Show Raw JSON"):
        st.subheader("Raw Data")
        st.json(filtered_data)


if __name__ == "__main__":
    main()
