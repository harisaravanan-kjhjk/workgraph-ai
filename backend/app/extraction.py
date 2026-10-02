def extract_entities(description: str):

    skills = []
    tools = []

    description_lower = description.lower()

    skill_keywords = {
        "authentication": "Authentication",
        "python": "Python",
        "java": "Java",
        "api": "API Development",
        "machine learning": "Machine Learning",
        "database": "Database",
        "networking": "Networking"
    }

    tool_keywords = {
        "redis": "Redis",
        "postgresql": "PostgreSQL",
        "mysql": "MySQL",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "git": "Git",
        "fastapi": "FastAPI"
    }

    for keyword, skill in skill_keywords.items():
        if keyword in description_lower:
            skills.append(skill)

    for keyword, tool in tool_keywords.items():
        if keyword in description_lower:
            tools.append(tool)

    return {
        "skills": skills,
        "tools": tools
    }


if __name__ == "__main__":
    result = extract_entities(
        "Developed Python API and optimized Redis caching using Docker"
    )

    print(result)