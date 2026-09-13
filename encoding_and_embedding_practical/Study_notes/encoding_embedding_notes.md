# Encoding & Embedding — Session Notes

---

## The One-Line Difference

| | Definition | Example Output |
|--|-----------|---------------|
| **Encoding** | Convert text to numbers — no meaning preserved | `[1, 0, 0, 0]` |
| **Embedding** | Convert text to numbers — meaning preserved | `[0.21, -0.45, 0.87, ...]` |

Encoding asks: *"what words exist?"*
Embedding asks: *"what do these words mean?"*

---

## Scalar vs Vector vs Matrix

```
Scalar  →  single number         →  5
Vector  →  list of numbers       →  [5, 10]
Matrix  →  grid of numbers       →  [[5, 10],
           (collection of rows)      [2,  4]]
```

In AI, all data — text, images, audio — gets converted to vectors and matrices before a model can use it.

---

## Encoding Methods (no meaning, just numbers)

### 1. One-Hot Encoding
Each word gets a vector with one `1` and rest `0s`.

Vocabulary: `[people, watch, movie]`
```
people → [1, 0, 0]
watch  → [0, 1, 0]
movie  → [0, 0, 1]
```
**Problem:** 50,000 word vocabulary = 50,000-dimension vectors. Mostly zeros (sparse). No meaning captured.

### 2. Bag of Words (BOW)
Count how many times each word appears in a document.
```
"I watch movie, you watch movie"
→ [I:1, watch:2, movie:2, you:1]
```
**Problem:** Loses word order. "Dog bit man" = "Man bit dog".

### 3. TF-IDF (Term Frequency — Inverse Document Frequency)
Weighs words by how important they are — common words like "the" get lower weight, rare domain words get higher weight.
**Used in:** keyword search, document ranking.

### 4. N-grams
Captures sequences of N words instead of single words.
`"New York"` as a bigram stays together instead of being split into `"New"` and `"York"`.

### 5. BM25
An improved version of TF-IDF used as a ranking algorithm.
**Used in:** RAG retrieval — the keyword search side of hybrid search.

### 6. GloVe (Global Vectors)
Count-based method using matrix factorization. First method that started capturing some word meaning.

---

## Why Encoding Is Not Enough

Three problems that encoding cannot solve:

**Problem 1 — No meaning**
"King" and "Queen" are completely unrelated in one-hot space. But semantically they are very close.

**Problem 2 — Sparse and huge**
50,000 words = 50,000 dimensions per vector. Wasteful and slow.

**Problem 3 — No context**
"Bank" (river bank) and "bank" (financial bank) get identical vectors. Context is ignored.

---

## Embedding (meaning preserved)

Embeddings are created by **neural networks** that learn from data. Similar meaning → similar vectors.

```
king   → [0.21, 0.89, -0.34, ...]
queen  → [0.19, 0.85, -0.31, ...]  ← very close to king
movie  → [0.91, -0.12, 0.67, ...]  ← far from king
```

Dense vectors (typically 384–1536 dimensions, all values used, no zeros).

### How similarity is measured after embedding:
- **Cosine similarity** — angle between two vectors (most common in RAG)
- **Dot product** — directional similarity
- **Euclidean distance** — straight-line distance in vector space

*Note: These methods compare embeddings — they don't create them.*

---

## Keyword Search vs Semantic Search

| | Keyword Search | Semantic Search |
|--|---------------|----------------|
| **How it works** | Exact word match | Meaning match |
| **Uses** | Encoding (TF-IDF, BM25) | Embeddings |
| **Query:** "affordable home loan" | Finds docs with those exact words | Finds docs about "cheap mortgage" too |
| **Good for** | Specific terms, codes, names | Conceptual questions, paraphrased queries |
| **Used in RAG** | BM25 retriever | Vector DB retriever |

**Real RAG systems use both** — called hybrid search. BM25 for exact matches, embeddings for semantic matches.

---

## Progression of Methods

```
One-Hot Encoding     → huge, sparse, no meaning
       ↓
Bag of Words / TF-IDF → smaller, still no meaning, loses order
       ↓
Word2Vec / GloVe     → dense, captures some meaning, one vector per word
       ↓
Transformers (BERT)  → dense, context-aware, same word = different vector per context
       ↓
SOTA Embedding Models → what RAG and Vector DBs use today
```

---

## Why This Matters for RAG

When you ask a RAG system a question:
1. Your question is converted to an embedding
2. The Vector DB finds chunks with similar embeddings (semantic search)
3. Those chunks are passed to the LLM as context
4. LLM generates the answer

Without embeddings → no semantic search → no RAG.

---

## Common Mistakes to Avoid

- Confusing *creating* embeddings (neural networks) with *comparing* embeddings (cosine similarity)
- Thinking one-hot encoding captures any meaning — it does not
- Thinking multi-hot encoding solves one-hot's problems — it still has no meaning and loses order
- Thinking "SIP" in a vector search always means Systematic Investment Plan — the model sees context, not intent

---

## Quick Reference

```
Scalar   = single number
Vector   = list of numbers → [0.2, 0.8, 0.1]
Matrix   = grid of numbers → collection of vectors

Encoding = numbers without meaning  → sparse vectors
Embedding = numbers with meaning    → dense vectors

Keyword search  = exact word match  → BM25
Semantic search = meaning match     → Vector DB + embeddings
```
