# Encoding — Practical Session (Final)

---

## What This Session Covered

Hands-on implementation of TF-IDF using sklearn, vocabulary concepts, and an introduction to Word2Vec — why it's different from all encoding methods before it.

---

## Why Vocabulary Matters

Before converting text to numbers, you need a vocabulary — the complete list of unique words across all your documents.

```
Documents:
D1: "I love India"
D2: "I love Generative AI"
D3: "I hate manual programming"

Vocabulary: [I, love, India, Generative, AI, hate, manual, programming]
```

Every document gets converted into a vector of this vocabulary size. Words not in the vocabulary are ignored — this is the **Out-of-Vocabulary (OOV) problem**.

---

## TF-IDF in Code

```python
from sklearn.feature_extraction.text import TfidfVectorizer

docs = [
    "people watch cricket",
    "cricket give comment",
    "people give command",
    "watch cricket people"
]

# Create vectorizer object
tfidf = TfidfVectorizer()

# fit_transform = fit() + transform() in one step
# fit()      → learns vocabulary from data
# transform() → converts data to vectors
# fit_transform() → does both at once on same dataset
tfidf_vectors = tfidf.fit_transform(docs)

# Get the actual numbers
print(tfidf_vectors.toarray())

# Check vocabulary
print(tfidf.get_feature_names_out())

# Iterate through vectors
for vector in tfidf_vectors:
    print(vector)
```

**Output shape:** `(4 documents, N unique words)` — one row per document, one column per vocabulary word.

**Important:** Use `fit_transform()` on training data only. On new/test data use `transform()` alone — never fit on test data.

---

## fit() vs transform() vs fit_transform()

| Method | What it does | When to use |
|--------|-------------|-------------|
| `fit()` | Learns vocabulary/stats from data | Training data only |
| `transform()` | Converts data to vectors using learned vocab | New/test data |
| `fit_transform()` | Both at once | Training data only |

---

## TF-IDF Formula Recap

```
TF  = count of word in this document / total words in this document
IDF = log(total documents / documents containing this word)
TF-IDF = TF × IDF
```

**Example from session:**
- "people" appears in 2 of 4 documents → IDF = log(4/2) = 0.69
- "cricket" appears in 3 of 4 documents → IDF = log(4/3) = 0.28

"people" gets higher weight than "cricket" because it's more distinctive.

---

## N-grams — What They Are and Why to Skip Them

N-grams capture sequences of N words instead of single words.

```
Sentence: "New York City"
Unigrams (n=1): ["New", "York", "City"]
Bigrams  (n=2): ["New York", "York City"]
Trigrams (n=3): ["New York City"]
```

**Why your mentor said skip it:**
N-grams are a classic NLP concept — useful for traditional text processing pipelines. As an AI Engineer, your focus is building on top of pre-trained models (LLMs, embeddings). Those models already handle context and word relationships far better than N-grams ever could. Deep NLP is a different career path.

**Know the concept. Don't go deep on it.**

---

## Word2Vec — Why It's Different

Everything before Word2Vec (one-hot, BOW, TF-IDF) had one problem in common: **no meaning captured.**

Word2Vec was the breakthrough that changed this.

### How features are learned

In one-hot encoding, features = words directly. Simple, fixed, hand-crafted.

In Word2Vec, features are **learned from data** through a neural network:
- The model is trained to predict a word from its surrounding context (or context from a word)
- Through millions of these predictions, the model learns that "king" and "queen" appear in similar contexts
- So their vectors end up close together in vector space

**The features emerge from the data — they are not predefined.**

```
king  → [0.50, 0.21, -0.12, ...]
queen → [0.48, 0.19, -0.11, ...]  ← very similar
dog   → [0.91, -0.44, 0.87, ...]  ← far from king
```

### The famous example
```
king - man + woman ≈ queen
```
This only works because Word2Vec captures relationships between concepts, not just word presence.

### Two techniques (covered in next session)
- **CBOW** (Continuous Bag of Words) — predict center word from context
- **Skip-gram** — predict context words from center word

---

## Comparing All Encoding Methods

| Method | Meaning? | Order? | Sparse? | Use Case |
|--------|---------|--------|---------|----------|
| One-Hot | ❌ | ❌ | ✅ | Basic categorical encoding |
| Bag of Words | ❌ | ❌ | ✅ | Text classification |
| TF-IDF | ❌ | ❌ | ✅ | Keyword search, BM25, RAG retrieval |
| Word2Vec | ✅ | ❌ | ❌ | Word similarity, semantic tasks |
| Transformers | ✅ | ✅ | ❌ | LLMs, RAG, everything modern |

---

## What AI Engineers Actually Use

**TF-IDF / BM25** → keyword search side of RAG hybrid retrieval

**Embeddings (from Transformer models)** → semantic search side of RAG

You don't need to implement these from scratch. You need to understand:
- What they do and why
- Which one to use when
- How to call them with sklearn / sentence-transformers / LangChain

---

## Quick Reference — sklearn Classes

```python
from sklearn.feature_extraction.text import CountVectorizer   # Bag of Words
from sklearn.feature_extraction.text import TfidfVectorizer   # TF-IDF

# Both follow same pattern:
vectorizer = CountVectorizer()       # or TfidfVectorizer()
X_train = vectorizer.fit_transform(train_docs)   # learn + convert
X_test  = vectorizer.transform(test_docs)         # convert only

vectorizer.get_feature_names_out()  # see vocabulary
X_train.toarray()                   # see actual numbers
```

---

## Your Mini-Project (Do This Now)

Build a simple similarity search using TF-IDF:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 5 Indian finance sentences
docs = [
    "RBI sets the repo rate to control inflation",
    "SEBI regulates the stock market in India",
    "SIP allows monthly investment in mutual funds",
    "NSE and BSE are the two major stock exchanges",
    "ELSS qualifies for tax deduction under Section 80C"
]

query = "how to save tax in India"

vectorizer = TfidfVectorizer()
doc_vectors = vectorizer.fit_transform(docs)
query_vector = vectorizer.transform([query])

similarities = cosine_similarity(query_vector, doc_vectors)
best_match = docs[similarities.argmax()]
print(f"Best match: {best_match}")
```

Run this. See which sentence matches "how to save tax in India". Then try a different query and see if the result makes sense.
