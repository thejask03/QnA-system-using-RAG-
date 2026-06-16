<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

    <div align="center">
        <h1>🚀 Dynamic Multimodal RAG QnA System</h1>
        <p><strong>A production-ready Retrieval-Augmented Generation (RAG) system utilizing LlamaIndex (for data ingestion and retrieval), local HuggingFace Embeddings, and Google Gemini.</strong></p> (for final text generation).
        <p>
            <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python Version">
            <img src="https://img.shields.io/badge/LlamaIndex-0.10+-orange.svg" alt="LlamaIndex Version">
            <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg" alt="Streamlit">
            <img src="https://img.shields.io/badge/LLM-Gemini_2.5_Flash-green.svg" alt="Gemini">
        </p>
    </div>

    <hr>

    <h2>📋 Overview</h2>
    <p>
        This repository features a robust, enterprise-grade <strong>Retrieval-Augmented Generation (RAG)</strong> architecture engineered to turn unstructured data chunks (PDFs, txt files) into a private, context-aware query engine. It wraps advanced data ingestion pipelines into an interactive, sleek <strong>Streamlit</strong> web UI dashboards.
    </p>
    <p>
        Unlike naive RAG implementations, this project solves two massive real-world deployment challenges: 
        <strong>API rate-limiting bottlenecks (429 errors)</strong> and <strong>cloud-sync filesystem locking (WinError 5 Access Denied)</strong>.
    </p>

    <h2>✨ Key Features</h2>
    <ul>
        <li>
            <strong>🔄 Dynamic Context Ingestion:</strong> Features an on-the-fly data pipeline that actively sweeps stale caches, writes incoming web file buffers securely onto disk, and automatically triggers index rebuilding when a user drops a new file.
        </li>
        <li>
            <strong>🛡️ 429 Quota-Exceeded Immunity:</strong> Uses a hybrid open-source stack. Document tokenization and vector calculations are executed entirely on your local machine CPU using <code>bge-small-en-v1.5</code> via HuggingFace. This results in <strong>0 network embedding calls</strong> and virtually unlimited free document parsing.
        </li>
        <li>
            <strong>🧠 Advanced Reasoning Engine:</strong> Leverages the up-to-date <code>gemini-2.5-flash</code> API strictly as a final context-synthesizer, producing structured, hyper-accurate responses devoid of generic LLM hallucinations.
        </li>
        <li>
            <strong>🪟 Windows &amp; OneDrive Protection:</strong> Implements defensive <code>os.chmod</code> and <code>stat.S_IWRITE</code> file permission sweeps to prevent crashes caused by background cloud sync engines (like Microsoft OneDrive) locking runtime database components.
        </li>
    </ul>
