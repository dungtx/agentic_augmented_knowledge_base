# LLM resources for later

## Capture
- https://github.com/run-llama/llama_index - OCR/capture capability with data modelling

## Memory
- https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph - LangChain agent thinking system

## Agents
- https://www.langchain.com/ - Agent creation SDK

## Workflows
- Sample workflow:
```
My typical workflow:

    Plugin for getting info from Jira
    Plugin for ui analysis based on components from my codebase - proposes which components to reuse, add, modify, missing colors other things
    Plugin for planning - technical plan like from junior how to do it step by step, references, % of success, questions, features to support in the future

    Each step produces artifact.
    Each artifact can be referenced in the next step (you chain ui analysis with plan etc.
    Each step is a new session to reset the context.

Planning can be done by higher models, implementation sonnet with advisor

I am changing architecture, features are 100% built by AI. Once the specification is created, reviewed and fixed, the code is usally high quality and doesn't require fixes (sometimes subtle ones, refactoring)

For now we are using the lowest teams plan, which is 1.5x pro. Android development, so keep in mind that it might work differently somewhere else. We have a lot of spaghetti logic, testing and other things beside coding

Plugin for creating plugins - I started with that. Let AI read standards, what things can be in plugin and then workflow of creating a plugin (asking user the questions how the workflow is gonna work, what to remember about, what to focus one, any artifacts to be generated). This plugin allowed me to create new plugins much faster

i also created a plugin for brainstorming. Really good for complicated cases where you do not want one solution, but multiple ideas. Few ideas based on prompt, few ideas that might be related to prompt's topic, but not directly (might be useful, sometimes proposes things that would never appear due to too focused prompt), known algorithms or standards we can reuse
```
- https://github.com/isvlasov/rageatc-oss - Guided thinking for LLM

