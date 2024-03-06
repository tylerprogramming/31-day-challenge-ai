import autogen

api_keys = ["sk-1231231"]
base_urls = ["http://localhost:8001"]
api_type = "openai"
api_version = "api-preview-01"

config_list = autogen.get_config_list(
    api_keys,
    base_urls,
    api_type,
    api_version
)

print(config_list)
