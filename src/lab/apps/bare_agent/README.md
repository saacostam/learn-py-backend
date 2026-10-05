# Bare Agent

A small AI agent built from scratch as a learning project.

The goal is to understand how an agent works underneath the abstractions provided by agent frameworks. The project explores the basic agent loop: receiving context, deciding whether to use a tool or finish, using the result to continue, and eventually producing a final response.

It also explores the ideas around agents as long-running processes, including queues, workers, state, retries, and recovery.

The implementation is intentionally simple and focused on learning the concepts rather than building a production-ready agent.

## Concepts

- Tool calling
- Agent loops
- ReAct-style agent behavior
- Agent state
- Queues and workers
- Retries and recovery
- Idempotency
- Failure handling
- In-memory execution

The eventual goal is to compare this from-scratch approach with an equivalent implementation using an agent framework such as LangGraph.
