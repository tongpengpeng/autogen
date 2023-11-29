import sys
import autogen

config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)
print(config_list_gpt4)
llm_config = {
    "config_list": config_list_gpt4,
    "cache_seed": 42,
    "temperature": 0,
    "timeout": 120
}

user = autogen.UserProxyAgent(
    name='Admin',
    system_message='A human admin',
    code_execution_config=False,
    human_input_mode='NEVER',
    function_map={

    },
    is_termination_msg=lambda x: True if x.get("content") is not None and "TERMINATE" in x.get("content") else False
)

searcher = autogen.AssistantAgent(
    name='Searcher',
    system_message="Searcher. 今年是2023年，你是一个通用搜索引擎，负责资料的查询",
    llm_config={
        "config_list": config_list_gpt4,
        "functions": [
            {
                "name": "report_search",
                "description": "你是一个专业的搜索引擎，写报告之前可以搜索一下其他的报告形式，重点，分析问题的方式",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keywords": {
                            "type": "string",
                            "description": "假如要写一篇报告，结合行业报告所需生成搜索关键词，要求：关键词少于5个，关键词之间使用空格隔开"
                        }
                    },
                    "required": ["keywords"]
                }
            }
        ]
    },
    is_termination_msg=lambda x: True if x.get("content") is not None and "TERMINATE" in x.get("content") else False
)