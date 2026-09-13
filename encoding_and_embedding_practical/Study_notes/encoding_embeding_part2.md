# Encoding — Mathematical Intuition (Part 2)

---

## What This Session Covered

How encoding methods actually work mathematically — One-Hot, Bag of Words, and TF-IDF — with their limitations and why each one led to the next.

---

## One-Hot Encoding

Each word in your vocabulary gets a unique position. That word is `1`, everything else is `0`.

**Vocabulary:** `[cat, sat, mat]`
```
cat → [1, 0, 0]
sat → [0, 1, 0]
mat → [0, 0, 1]
```

**Vector dimension = vocabulary size.** If vocabulary has 10,000 words → each vector is 10,000 numbers long, almost all zeros. This is called a **sparse vector**.

**Problems:**
- Huge and wasteful — 10,000 dimensions for one word
- No meaning — "cat" and "kitten" are completely unrelated
- No word order captured

---

## Bag of Words (BOW)

Count how many times each word appears in a sentence/document.

**Sentences:**
- D1: "Dog bites man"
- D2: "Man bites dog"

**Vocabulary:** `[bites, dog, man]`

| | bites | dog | man |
|--|-------|-----|-----|
| D1 | 1 | 1 | 1 |
| D2 | 1 | 1 | 1 |

**Both sentences give identical vectors** — BOW cannot tell "Dog bites man" from "Man bites dog."

**Library:** `CountVectorizer` from `sklearn`

```python
from sklearn.feature_extraction.text import CountVectorizer

docs = ["Dog bites man", "Man bites dog"]
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(docs)
print(vectorizer.get_feature_names_out())  # vocabulary
print(X.toarray())                          # vectors
```

**Problems:**
- Loses word order completely
- No semantic meaning — "like" and "love" are unrelated
- Out-of-vocabulary (OOV) problem — new words not in training vocab are ignored
- Still sparse

---

## TF-IDF (Term Frequency — Inverse Document Frequency)

Fixes BOW's biggest problem: common words like "the", "is", "a" get counted as important just because they appear everywhere.

**TF-IDF idea:** A word is important if it appears frequently in *one* document but rarely across *all* documents.

```
TF  = (count of word in this document) / (total words in this document)
IDF = log(total documents / documents containing this word)

TF-IDF = TF × IDF
```

**Why log?** Without log, a word appearing 100 times would seem 10x more important than one appearing 10 times — too extreme. Log dampens this effect and keeps weights balanced.

**Example:**
- "the" appears in every document → IDF is near 0 → low TF-IDF weight
- "RBI" appears in only 2 finance documents → IDF is high → high TF-IDF weight

**Library:** `TfidfVectorizer` from `sklearn`

```python
from sklearn.feature_extraction.text import TfidfVectorizer

docs = ["RBI sets the repo rate", "The bank lends money"]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)
print(X.toarray())
```

**Used in:** Keyword search, BM25 (RAG retrieval), document ranking

**Problems:**
- Still no semantic meaning — "affordable" and "cheap" are unrelated
- Still loses word order
- Sparse vectors

---

## Comparing All Three

| Method | Captures Order? | Captures Meaning? | Vector Type | Used In |
|--------|----------------|-------------------|-------------|---------|
| One-Hot | No | No | Sparse | Old NLP |
| Bag of Words | No | No | Sparse | Classical NLP, text classification |
| TF-IDF | No | No | Sparse | Keyword search, BM25, RAG retrieval |
| Embeddings | Yes | Yes | Dense | Semantic search, RAG, LLMs |

**None of the encoding methods capture meaning.** That's why embeddings were invented.

---

## The Key Limitation All Three Share

```
"Dog bites man"  →  BOW/TF-IDF  →  [1, 1, 1]
"Man bites dog"  →  BOW/TF-IDF  →  [1, 1, 1]  ← identical!

"affordable loan"  →  TF-IDF  →  some vector
"cheap mortgage"   →  TF-IDF  →  completely different vector  ← no relation!
```

Encoding treats each word as independent. It has no idea that "affordable" and "cheap" mean similar things. This is the fundamental problem that Word2Vec and Transformers solved.

---

## Why This Matters for RAG

In a RAG system, you need to find relevant documents for a user's question. Two options:

**Keyword search (BM25/TF-IDF):**
- Fast, exact word matching
- Misses "cheap mortgage" when user asks "affordable loan"

**Semantic search (Embeddings):**
- Slower, meaning-based matching
- Finds "cheap mortgage" for "affordable loan" query

**Production RAG uses both** — called hybrid search. TF-IDF/BM25 for exact matches, embeddings for semantic matches. That's why understanding encoding is not optional even in the LLM era.

---

## Interview Questions from This Session

**Q: What is TF-IDF and why is IDF needed?**
TF measures how often a word appears in a document. IDF penalizes words that appear in every document (like "the"), so they don't dominate. Together they identify words that define a specific document.

**Q: What is the difference between BOW and TF-IDF?**
BOW counts raw word frequency. TF-IDF weights that frequency by how rare the word is across all documents — giving more importance to distinctive words.

**Q: What is a sparse vector?**
A vector where most values are zero. One-hot and BOW produce sparse vectors — a 10,000 word vocabulary means a 10,000 dimension vector with one or a few non-zero values. Wasteful in memory and computation.

---

## Quick Reference

```
One-Hot    → presence/absence only → [1, 0, 0, 0]
BOW        → word count            → [2, 1, 0, 3]
TF-IDF     → weighted word count   → [0.82, 0.21, 0, 0.54]
Embeddings → meaning               → [0.21, -0.45, 0.87, ...]

CountVectorizer  → BOW in sklearn
TfidfVectorizer  → TF-IDF in sklearn
```
