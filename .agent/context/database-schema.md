# Database Schema: Sidekick AI Agent

## Status: Stateless / In-Memory Session Architecture

Sidekick AI Agent is currently architected as a **stateless, session-isolated application**:
- **Persistence Model:** In-memory checkpoints using LangGraph's `MemorySaver`.
- **Session Lifecycle:** Ephemeral per Gradio session. Sessions are initialized upon UI load and garbage collected on session disconnect via `delete_callback=free_resources`.
- **External Database:** None currently attached.

---

## Planned Future Database Schema (Persistent Memory Roadmap)

When migrating to persistent user history and knowledge retention (e.g., SQLite / PostgreSQL + `pgvector`), the following schema structure is planned:

### `users`
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Unique user identifier |
| `email` | VARCHAR | User email |
| `created_at` | TIMESTAMP | Registration timestamp |
| `preferences` | JSONB | Saved user preferences & default criteria |

### `sessions`
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Session ID |
| `user_id` | UUID (FK -> users.id) | Owning user |
| `title` | VARCHAR | Auto-generated session title |
| `created_at` | TIMESTAMP | Creation time |
| `updated_at` | TIMESTAMP | Last interaction time |

### `agent_messages`
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Message ID |
| `session_id` | UUID (FK -> sessions.id) | Associated session |
| `role` | VARCHAR | `user`, `worker`, `evaluator`, `tool` |
| `content` | TEXT | Message body |
| `metadata` | JSONB | Tool calls, execution duration, tokens |
| `created_at` | TIMESTAMP | Timestamp |

### `knowledge_vectors` (ChromaDB / pgvector)
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID (PK) | Vector document ID |
| `session_id` | UUID | Associated session (optional) |
| `content` | TEXT | Extracted text chunk |
| `embedding` | VECTOR(1536) | OpenAI text-embedding-3-small vector |
| `source_url` | TEXT | Source URL / document reference |
