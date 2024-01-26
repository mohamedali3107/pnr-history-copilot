from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="2d55bceb2c064158b5e78f805f7b298c",
    api_version="2023-07-01-preview",
    azure_endpoint="https://ama-openai-uks.openai.azure.com/",
    timeout=10.0
)