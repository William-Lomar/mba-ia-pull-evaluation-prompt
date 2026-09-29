"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    check_env_vars(["LANGSMITH_API_KEY"])

    prompt_name = "leonanluppi/bug_to_user_story_v1"
    output_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v1.yml"

    if output_path.exists():
        print(f"⏭️  Arquivo já existe, pulando: {output_path}")
        return 0

    print_section_header(f"Fazendo pull: {prompt_name}")

    prompt = hub.pull(prompt_name)

    messages = prompt.messages
    system_msg = next((m.prompt.template for m in messages if m.__class__.__name__ == "SystemMessagePromptTemplate"), "")
    human_msg = next((m.prompt.template for m in messages if m.__class__.__name__ == "HumanMessagePromptTemplate"), "")

    data = {
        "bug_to_user_story_v1": {
            "description": "Prompt para converter relatos de bugs em User Stories",
            "system_prompt": system_msg,
            "user_prompt": human_msg,
            "version": "v1",
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }

    if save_yaml(data, str(output_path)):
        print(f"✅ Prompt salvo em: {output_path}")
    else:
        print("❌ Falha ao salvar o prompt.")
        return 1

    return 0


def main():
    """Função principal"""
    return pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
