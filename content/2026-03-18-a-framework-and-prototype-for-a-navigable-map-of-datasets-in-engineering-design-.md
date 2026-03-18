# A Framework and Prototype for a Navigable Map of Datasets in Engineering Design and Systems Engineering

Engineering design and systems engineering have always been data-rich disciplines—think sketches, CAD files, simulation results, test logs, requirements documents, supplier data, maintenance records, and more. But here's the paradox: despite being flooded with data, engineers often struggle to find the *right* data at the *right* time. Information is siloed across tools, buried in folders, or locked in proprietary formats. As systems grow more complex (hello, megaprojects and AI-augmented design), this data fragmentation becomes a serious bottleneck. A new paper presents a timely solution: a **navigable map of datasets**—a unified, searchable, semantically organized view of all engineering data across the entire system lifecycle. Imagine having a Google Maps for your project's data, where you can zoom from high-level system views down to individual test reports, and everything in between is connected and discoverable.

## The Data Sprawl Problem in Engineering

Modern engineering projects generate petabytes of data spread across:
- **Conceptual phase**: Market studies, stakeholder needs, concept sketches
- **Design phase**: CAD models, FEA results, BOMs, design reviews
- **Implementation**: Manufacturing specs, supplier quotes, quality reports
- **Verification & Validation**: Test plans, results, deviation records
- **Operations & Maintenance**: As-built records, field performance data, service bulletins

Each phase uses different tools (SolidWorks, ANSYS, JAMA, DOORS, Excel, SharePoint, PLM systems). Data lives in different databases, file systems, and cloud services. There's no single "map" that shows you what exists, where it lives, how it relates to other artifacts, and whether it's trustworthy. Engineers waste hours hunting for data, often duplicating work because they can't find existing information. This isn't just inefficient—it risks errors, delays, and suboptimal decisions.

## What's a "Navigable Map" of Datasets?

The proposed framework is more than a fancy search engine. It's a **knowledge graph** of datasets, enriched with metadata and semantic relationships. Key components:

- **Dataset registry**: Each dataset (file, database table, API endpoint) gets a unique identifier and rich metadata: title, description, creation date, owner, format, access rights, quality metrics.
- **Semantic tagging**: Datasets are tagged with ontologies (e.g., "structural analysis," "thermal performance," "requirement specification") and linked to engineering concepts (components, subsystems, functions).
- **Provenance tracking**: The map records where each dataset came from, how it was derived (e.g., "simulation output from model X"), and what transformations it underwent.
- **Versioning & lineage**: You can see how a dataset evolved over time and trace its ancestry—critical for audits and impact analysis.
- **Search & navigation**: A user-friendly interface (think Google Maps + facets) lets you browse by phase, discipline, component, or keyword. You can zoom out to see all datasets in a subsystem, or zoom in to a specific test result.
- **Quality indicators**: The map highlights datasets with known issues (missing metadata, low confidence, outdated) so users know what to trust.

The prototype demonstrates this with a real-world aerospace case study, ingesting data from multiple tools and presenting it through a web-based navigator.

## Key Benefits: From Discovery to Decision-Making

This navigable map transforms how engineers interact with data:

- **Find anything, fast**: No more digging through shared drives or asking colleagues. You locate datasets by what they represent, not by where someone saved them.
- **Understand context**: Seeing relationships (e.g., "this simulation uses that material property dataset from 2019") helps assess relevance and reliability.
- **Avoid duplication**: Before starting a new analysis, you can check if similar work already exists—saving weeks of effort.
- **Impact analysis**: When a requirement changes, the map shows all downstream datasets that might need updating.
- **Compliance & audit**: Traceability from requirements to verification evidence becomes automatic, satisfying standards like ISO 15288 or DO-178C.
- **Knowledge retention**: When team members leave, their data contributions remain discoverable and understood, preventing "tribal knowledge" loss.

## Challenges and Prototype Insights

Building such a map isn't trivial. The biggest hurdles are:
- **Heterogeneous sources**: Each tool exports data differently; creating connectors is labor-intensive.
- **Semantic alignment**: Getting different disciplines to use common ontologies requires negotiation and sometimes custom mappings.
- **Scalability**: Large programs have millions of datasets; the graph database must handle complex queries quickly.
- **Adoption**: Engineers need to see value before they'll consistently tag and register their data.

The prototype addresses these with:
- A flexible ingestion layer that accepts CSV, JSON, XML, and direct database connections.
- An ontology that extends existing standards (e.g., ISO 15926) with project-specific extensions.
- A Neo4j graph backend optimized for traversals.
- A simple web UI with faceted search and visual graph exploration.

Early feedback from industry partners is positive: they recognize the "pain" it solves and are willing to pilot it on live projects.

## The Bigger Vision: Data-Centric Engineering

This framework is part of a larger shift toward **data-centric engineering**—where data is a first-class citizen throughout the lifecycle. It aligns with digital twin initiatives, model-based systems engineering (MBSE), and the growing use of AI/ML for design optimization. By making data discoverable and trustworthy, organizations can:
- Accelerate design cycles through reuse
- Improve decision-making with comprehensive evidence
- Enable AI-driven analysis across previously siloed datasets
- Reduce risk via better traceability

## Conclusion

The proliferation of data in engineering design and systems engineering doesn't have to be a curse. With a navigable map—a unified, semantic, searchable view of all datasets—engineers can finally harness the information they need, when they need it. The framework and prototype described in this paper show that it's technically feasible and delivers tangible value. As projects grow more complex and collaboration becomes more distributed, having a "GPS for your data" may become as essential as CAD or requirements management tools. The future of engineering isn't just about building smarter products; it's about working smarter with the data we already have. (◕‿◕)♡