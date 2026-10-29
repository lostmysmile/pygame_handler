# ERD (Entity Relationship Diagram)

## Status: not applicable to the current codebase

An ERD describes a persistent data model—typically database tables or records, their keys, and cardinality constraints. The current `pygame_handler` source does not define a database schema or an ORM model layer, and `pyproject.toml` does not declare a database/ORM dependency.

For that reason, this page intentionally does **not** invent an ERD. The core relationships in the current implementation are in-memory object ownership and references, which are documented as UML class relationships in [UML diagrams](uml.md).

Examples of current runtime objects include:

- A `Game` owning a `Scenes_handler` and a `Window`.
- A `Scene` owning an `EntitiesHandler` and a scene-local `EventsHandler`.
- An `EntitiesHandler` holding entity objects.
- Event registries holding callback registration records.

These are useful class/object relationships, but they are not database entities: the current code does not assign them persistence keys, define foreign-key constraints, or store them in a database.

## When an ERD becomes appropriate

Add a real ERD if the project introduces persistent records such as saved games, levels, user profiles, inventory, or asset metadata in a database. Before drawing it, identify:

1. Each persistent entity and its purpose.
2. The primary key for each entity.
3. Foreign-key relationships and relationship cardinality (one-to-one, one-to-many, or many-to-many).
4. Required/optional fields, uniqueness constraints, and delete/update behavior.
5. Which data is durable and which remains transient runtime state.

Once those decisions are backed by an actual persistence design, add a Mermaid `erDiagram` or another ERD format here. Until then, use the [UML class diagram](uml.md#1-class-diagram) to understand the current in-memory model.
