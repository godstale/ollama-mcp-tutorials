# What's new in LangGraph v1

**LangGraph v1 is a stability-focused release for the agent runtime.** It keeps the core graph APIs and execution model unchanged, while refining type safety, docs, and developer ergonomics.

It's designed to work hand-in-hand with [LangChain v1](/oss/python/releases/langchain-v1) (whose `create_agent` is built on LangGraph) so you can start high-level and drop down to granular control when needed.

<CardGroup cols={1}>
  <Card title="Stable core APIs" icon="diagram-project">
    Graph primitives (state, nodes, edges) and the execution/runtime model are unchanged, making upgrades straightforward.
  </Card>

  <Card title="Reliability, by default" icon="database">
    Durable execution with checkpointing, persistence, streaming, and human-in-the-loop continues to be first-class.
  </Card>

  <Card title="Seamless with LangChain v1" icon="link">
    LangChain's `create_agent` runs on LangGraph. Use LangChain for a fast start; drop to LangGraph for custom orchestration.
  </Card>
</CardGroup>

To upgrade,

<CodeGroup>
  ```bash pip theme={null}
  pip install -U langgraph
  ```

  ```bash uv theme={null}
  uv add langgraph
  ```
</CodeGroup>

## Deprecation of `create_react_agent`

The LangGraph [`create_react_agent`](https://reference.langchain.com/python/langgraph/agents/#langgraph.prebuilt.chat_agent_executor.create_react_agent) prebuilt has been deprecated in favor of LangChain's [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent). It provides a simpler interface, and offers greater customization potential through the introduction of middleware.

* For information on the new [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) API, see the [LangChain v1 release notes](/oss/python/releases/langchain-v1#create-agent).
* For information on migrating from [`create_react_agent`](https://reference.langchain.com/python/langgraph/agents/#langgraph.prebuilt.chat_agent_executor.create_react_agent) to [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent), see the [LangChain v1 migration guide](/oss/python/migrate/langchain-v1#create-agent).

## Reporting issues

Please report any issues discovered with 1.0 on [GitHub](https://github.com/langchain-ai/langgraph/issues) using the [`'v1'` label](https://github.com/langchain-ai/langgraph/issues?q=state%3Aopen%20label%3Av1).

## Additional resources

<CardGroup cols={3}>
  <Card title="LangGraph 1.0" icon="rocket" href="https://blog.langchain.com/langchain-langchain-1-0-alpha-releases/">
    Read the announcement
  </Card>

  <Card title="Overview" icon="book" href="/oss/python/langgraph/overview" arrow>
    What LangGraph is and when to use it
  </Card>

  <Card title="Graph API" icon="diagram-project" href="/oss/python/langgraph/graph-api" arrow>
    Build graphs with state, nodes, and edges
  </Card>

  <Card title="LangChain Agents" icon="robot" href="/oss/python/langchain/agents" arrow>
    High-level agents built on LangGraph
  </Card>

  <Card title="Migration guide" icon="arrow-right-arrow-left" href="/oss/python/migrate/langgraph-v1" arrow>
    How to migrate to LangGraph v1
  </Card>

  <Card title="GitHub" icon="github" href="https://github.com/langchain-ai/langgraph">
    Report issues or contribute
  </Card>
</CardGroup>

## See also

* [Versioning](/oss/python/versioning) – Understanding version numbers
* [Release policy](/oss/python/release-policy) – Detailed release policies

***

<Callout icon="pen-to-square" iconType="regular">
  [Edit the source of this page on GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/python/releases/langgraph-v1.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Connect these docs programmatically](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
</Tip>


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.langchain.com/llms.txt