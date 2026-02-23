# HBnB

HBnB is a simplified AirBnB-like application designed to demonstrate software architecture, object-oriented design, and full-stack development principles.  

The project is structured in multiple phases, progressively moving from system design and modeling to implementation and persistence. It emphasizes clean architecture, separation of concerns, and maintainable code organization.

---

## Part 1 – UML Design

Part 1 focuses on the architectural and conceptual design of the system using UML diagrams.

This phase includes:

- A **High-Level Package Diagram** describing the layered architecture.
- A **Detailed Class Diagram** defining the core business entities.
- **Sequence Diagrams** illustrating how API calls interact across system layers.

The purpose of this phase is to establish a clear technical blueprint that will guide the implementation stages of the HBnB project.

# 🚀 Part 2 – Business Logic & API Foundation

In Part 2 of the HBnB project, the application transitions from architectural design to concrete implementation.

This phase focuses on:

- Building a modular project structure following a layered architecture (Presentation, Business Logic, Persistence).
- Implementing the core business entities: `User`, `Place`, `Review`, and `Amenity`.
- Enforcing data validation and entity relationships at the model level.
- Introducing UUID-based identifiers for scalability and security.
- Implementing an in-memory repository with a defined interface (Repository pattern).
- Applying the Facade pattern to centralize communication between layers.
- Preparing the application for RESTful API integration using Flask and Flask-RESTx.

At this stage, authentication and database persistence are not yet implemented.  
However, the architecture is fully prepared to integrate SQLAlchemy and JWT authentication in Part 3.

This part establishes a clean, scalable, and maintainable foundation for the HBnB application.