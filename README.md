# 🚀 Dynamic RAG QnA System

A production-ready Retrieval-Augmented Generation (RAG) system engineered using LlamaIndex, local HuggingFace Embeddings, and Google Gemini to converse dynamically with technical documents and phase diagrams.

---

## 📋 Overview

This project is a highly robust, enterprise-grade **Retrieval-Augmented Generation (RAG)** system built to transform unstructured technical text and PDF manuals into a private, interactive knowledge base. It features an optimized hybrid architecture that eliminates API cost bottlenecks and insulates local operations against typical operating system file locks.

Unlike naive RAG templates, this application is custom-engineered to solve two critical real-world deployment challenges:
1. **API Rate-Limiting Bottlenecks (429 Errors):** Overridden by decoupling the vector embedding lifecycle from commercial cloud APIs.
2. **Cloud-Sync Filesystem Locking (WinError 5 Access Denied):** Patched by implementing robust local file permission overrides that prevent crashes inside cloud-synced folders.

---

## ✨ Key Features

* **🔄 Dynamic Context Ingestion:** Implements an on-the-fly data pipeline that clears old caches and re-indexes new files in real-time as users upload them via the web interface.
* **🛡️ 429 Quota-Exceeded Immunity:** Runs an open-source, local embedding pipeline utilizing `bge-small-en-v1.5` via HuggingFace. Vector mapping executes entirely on the host CPU with **zero network API overhead**, allowing for free, unlimited document parsing.
* **🧠 Advanced Reasoning Engine:** Integrates the up-to-date `gemini-2.5-flash` model solely as a final response synthesizer, ensuring hyper-accurate, perfectly formatted contextual answers devoid of typical LLM hallucinations.
