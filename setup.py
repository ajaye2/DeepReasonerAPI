from setuptools import setup, find_packages

setup(
    name="reasonedge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pydantic",
        "openai",
        "typing-extensions",
        "reasoners @ git+https://github.com/ajaye2/llm-reasoners.git@main#egg=reasoners",
        "gunicorn",
        "azure-core==1.32.0",
        "azure-identity==1.19.0",
        "requests",
        "langchain",
        "chainlit",
        "pydantic==2.10.1"
    ],
    author="Abubakarr Jaye",
    description="A Deep Reasoning library with multiple reasoning algorithms",
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    package_data={
        "reasonedge": ["py.typed"],
    },
)
