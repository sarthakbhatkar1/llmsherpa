import streamlit as st
import pandas as pd
import json

# Sample JSON data (you can replace this with your actual JSON)
data = [
    {
        "modelName": "",
        "deploymentServer": "",
        "description": "",
        "llmProvider": "",
        "llmModel": "",
        "config": {
            "type": "",
            "openai_auth_type": {},
            "openai_deployment_name": "",
            "openai_api_base": ""
        },
        "endpoints": ["chat", "completions"],
        "metadata": {
            "feature": {
                "creator": "",
                "license": "",
                "contextWindow": "",
                "supportedModality": [""],
                "version": ""
            },
            "externalBenchmark": {
                "informationExtraction": {"<benchmark_name>": {"metric": {"score": "", "source": ""}}},
                "languageUnderstanding": {"<benchmark_name>": {"metric": {"score": "", "source": ""}}},
                "questionAnswering": {"<benchmark_name>": {"metric": {"score": "", "source": ""}}},
                "logicalReasoning": {"<benchmark_name>": {"metric": {"score": "", "source": ""}}},
                "codeGeneration": {"<benchmark_name>": {"metric": {"score": "", "source": ""}}},
                "textEmbeddingRetrieval": {"<benchmark_name>": {"metric": {"score": "", "source": ""}}}
            },
            "bionicsBenchmark": {}
        }
    }
]


# Function to flatten nested JSON for easier display
def flatten_json(json_data):
    flat_data = []
    for item in json_data:
        flat_item = {
            'modelName': item.get('modelName', ''),
            'deploymentServer': item.get('deploymentServer', ''),
            'description': item.get('description', ''),
            'llmProvider': item.get('llmProvider', ''),
            'llmModel': item.get('llmModel', ''),
            'config_type': item.get('config', {}).get('type', ''),
            'endpoints': ', '.join(item.get('endpoints', [])),
            'creator': item.get('metadata', {}).get('feature', {}).get('creator', ''),
            'license': item.get('metadata', {}).get('feature', {}).get('license', ''),
            'contextWindow': item.get('metadata', {}).get('feature', {}).get('contextWindow', ''),
            'supportedModality': ', '.join(item.get('metadata', {}).get('feature', {}).get('supportedModality', [])),
            'version': item.get('metadata', {}).get('feature', {}).get('version', '')
        }
        flat_data.append(flat_item)
    return flat_data


# Streamlit app
def main():
    st.title('Model Dashboard')

    # Convert JSON to DataFrame
    flat_data = flatten_json(data)
    df = pd.DataFrame(flat_data)

    # Sidebar with filters
    st.sidebar.header('Filters')

    # Model Name filter
    model_names = ['All'] + sorted(df['modelName'].unique().tolist())
    selected_model = st.sidebar.selectbox('Model Name', model_names)

    # LLM Provider filter
    llm_providers = ['All'] + sorted(df['llmProvider'].unique().tolist())
    selected_provider = st.sidebar.selectbox('LLM Provider', llm_providers)

    # Deployment Server filter
    servers = ['All'] + sorted(df['deploymentServer'].unique().tolist())
    selected_server = st.sidebar.selectbox('Deployment Server', servers)

    # Endpoints filter
    endpoints = ['All'] + sorted(df['endpoints'].unique().tolist())
    selected_endpoints = st.sidebar.selectbox('Endpoints', endpoints)

    # Apply filters
    filtered_df = df.copy()
    if selected_model != 'All':
        filtered_df = filtered_df[filtered_df['modelName'] == selected_model]
    if selected_provider != 'All':
        filtered_df = filtered_df[filtered_df['llmProvider'] == selected_provider]
    if selected_server != 'All':
        filtered_df = filtered_df[filtered_df['deploymentServer'] == selected_server]
    if selected_endpoints != 'All':
        filtered_df = filtered_df[filtered_df['endpoints'] == selected_endpoints]

    # Display filtered data
    st.subheader('Filtered Models')
    st.dataframe(filtered_df)

    # Display total count
    st.write(f'Total models found: {len(filtered_df)}')

    # Option to view raw JSON for selected row
    if not filtered_df.empty and len(filtered_df) == 1:
        if st.checkbox('Show raw JSON for selected model'):
            st.json(data[df.index[filtered_df.index[0]]])

    # Download button for filtered data
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name='filtered_models.csv',
        mime='text/csv',
    )


if __name__ == '__main__':
    main()
