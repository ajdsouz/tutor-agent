# tutor-agent - An Agentic Educational Tutor

## Installation

The tutor agent can be installed using the following command:
```bash
uv sync tutor-agent
```

## Usage
To run the agent, run the following command.

### Adding documents to the database

To add documents to the database, use the following command
```bash
tutor-agent add-document path/to/document
```

### Retrieving documents

To search and retrieve relevant document (chunks), use the following command

```bash
tutor-agent search "query"
```

### Generating explanations

Using an LLM, you can generate explanations for your questions. These explanations can be augmented using Retrieval 
from the previous step or using websearch. These explanations / sources are cached. 

```bash
tutor-agent explain "query"
```
 
### Generating Progress Report

```bash
# command to get progress report, maybe should be per suibject/ module / ?

tutor-agent progress-check [module]:[submodule] #? we should check if this is possible!
```