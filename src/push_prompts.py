"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    full_name = f"{username}/{prompt_name}"

    print_section_header(f"Fazendo push: {full_name}")

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_data["system_prompt"]),
        ("human", prompt_data["user_prompt"]),
    ])

    client = Client()
    client.push_prompt(
        full_name,
        object=prompt,
        is_public=True,
        description=prompt_data.get("description", ""),
        tags=prompt_data.get("tags", []),
    )

    print(f"✅ Push realizado: {full_name}")
    return True


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []
    for field in ["system_prompt", "user_prompt"]:
        if not prompt_data.get(field, "").strip():
            errors.append(f"Campo obrigatório vazio: {field}")
    if "TODO" in prompt_data.get("system_prompt", ""):
        errors.append("system_prompt ainda contém TODOs")
    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"])

    from pathlib import Path
    yaml_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"

    raw = load_yaml(str(yaml_path))
    if not raw:
        return 1

    # Suporta tanto chave raiz quanto flat
    prompt_data = raw.get("bug_to_user_story_v2")

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Prompt inválido:")
        for e in errors:
            print(f"   - {e}")
        return 1

    success = push_prompt_to_langsmith("bug_to_user_story_v2", prompt_data)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
