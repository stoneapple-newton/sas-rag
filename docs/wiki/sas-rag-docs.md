# SAS RAG Docs

Curated starter page imported from [`docs/raw/sas-rag-docs.md`](../raw/sas-rag-docs.md) on 2026-06-06.

Related:
- [Wiki Index](README.md)

Notes:
- SAFe PI Roadmap and Source Plan for a SAS RAG MCP App
- Executive summary
- For a SAS-focused RAG + MCP application, the highest-leverage starting point is a **small, high-trust corpus of official SAS programming references** rather than a broad scrape of every SAS-related artifact. SAS already publishes a programming documentation home for SAS 9.4 and SAS Viya, alongside product-specific manuals for Base SAS language concepts, macro language, DATA step statements, functions, formats/informats, SQL, DS2, FedSQL, component objects, CAS, and administrative guidance. Those references are exactly the kinds of syntax-heavy, example-rich materials that produce strong retrieval signals for coding assistants. citeturn10search6turn5search4turn5search7turn7search0turn10search0turn42search1turn36search0
- A lightweight **SAFe-style** operating model fits this sub-project well, but it should be adapted to your current scale. SAFe positions PI Planning as a cadence-based ART event, typically run as a **two-day planning event every 8–12 weeks**, and features are expected to be sized so they can be delivered within a PI. Because your team size and delivery capacity are unspecified, the most practical interpretation is a **single-product, role-hatted ART** with you as project owner and interim business owner/product manager, and with explicit scope control around corpus, retrieval, evaluation, and MCP surface. citeturn26view0turn27view0turn22search23
- Architecturally, the first version should be **retrieval-first, not execution-first**. The MCP spec is designed around **resources, prompts, and tools**; LangChain’s current retrieval guidance supports both standard and agentic RAG patterns; LangSmith provides dataset-based offline evaluation and online quality monitoring; and MarkItDown is well suited to turning PDFs and office documents into Markdown while preserving headings, lists, tables, and links for downstream chunking. That combination is a strong foundation for a trusted SAS reference server that can support your coding CLI or editor integrations. citeturn18search9turn18search13turn18search6turn18search2turn18search11turn18search14turn18search0turn18search1turn18search5turn18search8turn19search0
- The most important implementation discipline is **version-aware retrieval**. SAS 9.4 and older releases are documented under a fixed-lifecycle model, while the SAS Viya platform uses a more modern continuous-delivery approach; SAS also publishes explicit migration guidance from SAS 9.4. Your metadata and retrieval filters therefore need to preserve product family, major version, maintenance/release cadence, publication date, and source priority, or your assistant will mix incompatible answers across SAS 9.4, Viya 3.5, and current Viya platform documentation. citeturn12search14turn17search0turn17search2turn11search15
- Assumptions and scope
- This report treats your app as a **SAS reference and code-understanding service** implemented with LangChain and exposed through MCP. It assumes a lightweight SAFe-style planning model rather than a literal large ART, because SAFe’s public guidance is written for ART-level alignment and Agile teams, while your team size, infrastructure footprint, and staffing remain unspecified. citeturn26view0turn22search23

Open questions:
- What conclusions from the raw source should become durable project knowledge?
- Which SAFe stories should this page support?
