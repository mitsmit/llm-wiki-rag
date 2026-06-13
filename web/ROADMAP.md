# Wiki Web App — Roadmap

Tracks planned improvements to the main web app (`web/`). Same format as
[research-agent/ROADMAP.md](../research-agent/ROADMAP.md) — each item is
written to be filed as a GitHub issue as-is.

_Last updated: 2026-06-13_

---

## Status

- ✅ **"Ask a question" on the front page** ([AskBox.js](static/js/components/AskBox.js),
  wired into [DeskView.js](static/js/components/DeskView.js)) — streams a
  wiki-dump answer via the existing `/api/query/wiki` / `stream_wiki_answer`,
  with a link to Compare for RAG citations/save. Done 2026-06-13.

- ✅ **Brainstorming module** ([brainstorm.py](brainstorm.py),
  [BrainstormView.js](static/js/components/BrainstormView.js)) — submit an
  idea, 2-3 domain-expert agents support/critique/refine/question it across
  a parallel-streaming multi-round discussion, concluding via wrap-up or
  agent agreement into a synthesized verdict, savable to `wiki/analyses/`.
  Done 2026-06-13.

---

## Future Improvements

### A. ~~"Ask a question" on the front page~~ — done
- **Resolved 2026-06-13** by the Ask box in Status above
  ([AskBox.js](static/js/components/AskBox.js)).

### B. User accounts + per-user knowledge base
- **Context:** The wiki is currently a single shared KB with no auth — all
  of `raw/`, `wiki/`, `log.md`, and the RAG index are global. To support
  multiple users, each user's KB should start empty and grow only as *they*
  ingest sources — the value is proportional to what each user adds.
- **Proposal:** Add a login/auth module (sessions or per-user tokens), scope
  content paths per user (e.g. `users/<id>/raw/`, `users/<id>/wiki/`,
  `users/<id>/log.md`) and the RAG index accordingly, and update
  `wiki_data.py` / indexing / research-agent result paths to operate within
  a user's namespace. New users land on an empty Desk with onboarding
  copy explaining they need to add sources (via INGEST / Discover) to get
  value.
- **Size:** L — multi-tenancy touches `wiki_data.py`, the RAG index, and
  research-agent's `results/` paths.

### C. ~~Brainstorming module — expert-agent counterpoints~~ — done
- **Resolved 2026-06-13** by the Brainstorming module in Status above
  ([BrainstormView.js](static/js/components/BrainstormView.js)). Note: the
  shipped version identifies expert domains via a standalone LLM call on
  the idea itself (not wiki tags/concepts) — the module is intentionally
  ungrounded, so personas reason generally rather than citing the wiki.

- **SExpert personas**S improve idea stress-testing by providing specialised, domain-specific critique that goes beyond simple information retrieval. According to the proposed Brainstorming module in the roadmap, these personas enhance the process through the following mechanisms:
Targeted Domain Expertise: The system identifies relevant domains for a user's proposal based on existing wiki tags and concepts
. It then "spins up" one or more expert agent personas specifically tailored to those domains
.
Active Critique and Counterpoints: Unlike standard query modules that simply answer questions against the wiki, these personas are designed to critique, counter, or refine a user’s idea
. This provides a "stress-test" by actively seeking out weaknesses or alternative perspectives.
Structured Synthesis of Objections: The output from these expert agents is synthesized into a structured response that highlights agreements, objections, and refinements
. This allows the user to see exactly where their idea holds up and where it may fail under expert-level scrutiny.
Integration with Existing Knowledge: These stress-tests can be saved as wiki/analyses/ pages, allowing the results of the brainstorming session to be integrated back into the user's knowledge base for future reference
.
This approach is intended to fill a gap in the current system, where existing modules (like Query or Discover) help surface what is already known but do not help a user challenge their own original ideas


---

## Notes

All three items are intended for a later iteration — not started yet.

##  The Ugly: Pragmatic "Hacks"

The OpenAI Warm-up: The design includes a deliberate "warming" of the OpenAI client during the server's lifespan to prevent a CPython module-import deadlock that occurs when parallel requests try to initialize the client at the same time
.
The Bridge Module: The research_bridge.py uses a sys.path shim to import the research agent as a sibling directory
. While it works, it is a fragile way to handle internal dependencies compared to proper packaging.


## Suggested Improvements
Transition to Async: The current research agent integration uses a thread/queue bridge to turn synchronous code into a FastAPI stream
. Refactoring the research agent to be natively asynchronous would improve resource management.
Multi-Tenancy (As Planned): Moving from a global KB to per-user knowledge bases is essential if this is to be used by more than one person
.
Vector Database: If the wiki grows to thousands of documents, replacing the numpy-based VectorStore with a dedicated vector database (like Qdrant or Milvus) would improve search performance and persistence
.
Expert Personas: Implementing the Brainstorming module
 would elevate the tool from a passive search engine to an active intellectual partner.



 o implement the Brainstorming module, which is categorized as a large ("L") effort, you should follow the architectural patterns established by the existing modules like the research-agent
.
The first steps to implement this feature would involve the following:
1. Backend Scaffolding and Infrastructure
Create a new dedicated module: Following the pattern of research-agent/, you should establish a new directory (e.g., brainstorm-agent/) to house the multi-agent orchestration logic
.
Implement a Bridge Module: Create a web/brainstorm_bridge.py file to handle sys.path shims and internal imports, similar to how the research_bridge.py integrates the research agent into the web server
.
Define Agent Personas: Develop the prompt logic required to "spin up" expert personas based on specific technical domains
.
2. Domain Identification Logic
Leverage Existing Metadata: Build a function that utilizes wiki_data.py to analyze a user's proposal against the page tags and concepts currently indexed in the wiki
.
Domain Mapping: Create a mapping system that translates these identified tags into specific expert agent configurations
.
3. API and Streaming Integration
Create a New Route: Add web/routes/brainstorm.py to the FastAPI backend to handle POST requests for new brainstorming sessions
.
Implement NDJSON Streaming: Use the established thread-and-queue pattern from routes/research.py to bridge the synchronous multi-agent orchestration into a streaming NDJSON response
. This ensures the user can see the critique and refinements in real-time as the different agents respond
.
4. Frontend Development
Develop the View Component: Create a new React component (e.g., BrainstormView.js) in static/js/components/ that reuses the streaming render patterns found in ComparePanel.js or ResearchView.js
.
Update the Router: Register the new module in the hash-based router within static/js/app.js (e.g., adding a #/brainstorm path)
.
5. Persistence and Synthesis
Structured Output: Program the system to synthesize the various agent counterpoints into a standard format featuring agreements, objections, and refinements
.
Save to Wiki: Integrate with the logic in routes/analyses.py to allow users to save the final brainstorming results as new pages in the wiki/analyses/ directory
.


While the proposed Brainstorming module will be "similar in shape" to the existing research-agent, its multi-agent orchestration introduces several key structural and functional differences:
1. Persona-Based Parallelism vs. Linear Search
The current research-agent follows a largely linear process: it expands a query, searches external sources (arXiv and the web), dedupes candidates, and ranks a reading list
. In contrast, the Brainstorming module will utilize a multi-agent orchestration where the system "spins up" one or more "expert agent" personas
. This suggests a parallel or conversational structure where multiple specialized agents provide diverse perspectives simultaneously, rather than a single agent performing a sequence of search tasks.
2. Internal Domain Mapping vs. External Query Expansion
The research-agent structure focuses on query expansion to find external information
. The Brainstorming module differs by first identifying relevant domains specifically from your wiki tags and concepts
. This makes the orchestration highly dependent on the existing internal knowledge base to select which expert personas are required for a given proposal.
3. Synthesis of Diverse Perspectives
A major structural difference lies in the final stage of the orchestration:
Research-agent: Outputs a curated "Top 10 Reading List" based on a ranking of discovered papers and articles
.
Brainstorming module: Requires a synthesis step to consolidate the "agreements, objections, and refinements" provided by the various expert agents into a single, structured response
. This implies a "manager" or "aggregator" agent role within the orchestration that does not exist in the research-agent's current structure.
4. Integration with the "Analyses" Workflow
While both modules can write to the wiki, their outputs serve different purposes in the knowledge base:
research-agent results are used to select items for the raw/ directory to be ingested
.
The Brainstorming module is designed to produce results that are potentially filable as wiki/analyses/ pages
. This aligns it more closely with the routes/analyses.py logic used by the Compare view to save high-level reasoning and critiques
.
Despite these differences, the technical "bridge" to the web server will likely remain the same. Just as the research-agent uses a background thread and a queue to stream NDJSON tokens to the FastAPI backend, the Brainstorming module is expected to adopt this pattern to handle its long-running multi-agent tasks without blocking the main server process.

Based on the roadmap for the Brainstorming module and the existing architectural patterns in the sources, the prompt logic required to define specialized agent personas involves a combination of dynamic domain mapping, role-based instruction, and structured output constraints.
The necessary prompt logic can be broken down into the following components:
1. Domain-Driven Context Injection
The system first identifies relevant domains by scanning the page_tags and technical concepts extracted by wiki_data.py
. The prompt logic must then:
Inject Domain Expertise: Use the identified tags to pull relevant excerpts or summaries from the wiki to "prime" the agent with the user's specific internal knowledge base
.
Persona Identification: Map these tags to specific professional identities (e.g., a "Distributed Systems Architect" or a "Security Researcher") to set the specialized tone and expertise level for the agent
.
2. Role-Based Behavioral Instructions
Similar to the RAG_SYSTEM_PROMPT or the rules in the research agent's CLAUDE.md, the persona prompt must define clear behavioral boundaries
:
Critical Lens: Explicitly instruct the agent to adopt a skeptical or refining mindset rather than a purely generative one
.
Counterpoint Generation: Mandate the generation of counter-arguments or "stress-tests" for the user's proposal
.
Constructive Refinement: Require the agent to not just point out flaws but to suggest specific technical refinements based on the domain expertise
.
3. Structured Synthesis Constraints
To ensure the multi-agent orchestration can be consolidated into a coherent response, the prompt logic must enforce a strict output schema
:
Categorized Feedback: Instructions should require the agent to segment its response into three specific categories: Agreements, Objections, and Refinements
.
Markdown Formatting: Following the pattern in generation.py, the prompt should enforce markdown rules to ensure the results are "wiki-ready" and can be saved as a wiki/analyses/ page
.
4. Precedents in Existing Logic
The system already uses sophisticated prompt logic that can serve as a template for these personas:
The RAG Model: The RAG_SYSTEM_PROMPT already handles complex requirements like citation-by-path rules and "Sources used" sections, which could be adapted to ensure personas cite relevant wiki documents when critiquing an idea
.
The Research Agent Model: The research-agent/CLAUDE.md provides a blueprint for "behavioral rules" and "output format" that the new brainstorming module is intended to emulate
.
By combining these elements, the system can "spin up" personas that feel like distinct experts grounded in the specific technical context of your personal wiki