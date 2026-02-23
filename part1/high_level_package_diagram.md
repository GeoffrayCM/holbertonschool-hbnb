```mermaid

flowchart TB

%% ========= PRESENTATION LAYER =========
subgraph P["Presentation Layer"]
  direction TB
  API["API / Endpoints(Controllers / Routes)"_.
  SVC["Services(Request handling)"]
  API --> SVC
end

%% ========= BUSINESS LOGIC LAYER =========
subgraph B["Business Logic Layer"]
  direction TB
  FACADE["HBnB Facade(Unified interface)"]
  MODELS["Domain Models(User, Place, Review, Amenity)\n+ Business Rules"]
  FACADE --> MODELS
end

%% ========= PERSISTENCE LAYER =========
subgraph D["Persistence Layer"]
  direction TB
  REPO["Repositories / Storage(Data access abstraction)"]
  DB["Database(Persistent storage)"]
  REPO --> DB
end

%% ========= LAYER COMMUNICATION (DEPENDENCIES) =========
SVC -->|Calls Facade| FACADE
MODELS -->|CRUD / Data operations| REPO
