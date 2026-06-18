# 🤖 AI & ML — Topic-by-Topic Interview Guide
> CSE Fresher | Simple English | No Math | Placement Focused | 30 Min Read

---

## 📌 Topics Covered

| # | Topic |
|---|---|
| 1 | Machine Learning Basics |
| 2 | Classification |
| 3 | Classification vs Regression |
| 4 | Features vs Labels |
| 5 | Training Data vs Testing Data |
| 6 | Accuracy |
| 7 | Precision |
| 8 | Recall |
| 9 | F1 Score |
| 10 | XGBoost |
| 11 | NLP Basics |
| 12 | Tokenization |
| 13 | Sentiment Analysis |
| 14 | Text Classification |
| 15 | LLM Basics |
| 16 | Prompt Engineering |
| 17 | Hallucination |
| 18 | RAG |
| 19 | Fine-Tuning |
| — | Revision Sheet + Top 30 Q&A |

---

---

## 1. Machine Learning Basics

**Easy Definition:**
Machine Learning is teaching a computer to learn from data — without writing rules manually.
You give examples, the computer finds patterns on its own, and uses those patterns to predict new outcomes.

**Why it is used:**
- Too many patterns for a human to code manually
- Gets better with more data
- Works across many domains — healthcare, finance, language, images

**Real-World Example:**
> Gmail's spam filter — nobody wrote rules for every spam pattern.
> The model learned from millions of spam vs non-spam emails and now classifies on its own.

**30-Second Interview Answer:**
> Machine Learning is a branch of AI where systems learn from data to make predictions without being explicitly programmed.
> Instead of writing if-else rules, you train a model on historical data and it learns the patterns automatically.
> It has three types — Supervised, Unsupervised, and Reinforcement Learning.

**Common Follow-up Questions:**
- What are the types of ML? (Supervised / Unsupervised / Reinforcement)
- What is overfitting?
- How is ML different from traditional programming?

**One-Line Revision:**
> ML = Computer learns from data instead of following manually written rules.

---

### Types of ML (Must Know)

| Type | Data Needed | Goal | Example |
|---|---|---|---|
| **Supervised** | Input + correct answer (labelled) | Predict output | Disease: Yes/No |
| **Unsupervised** | Input only (no labels) | Find hidden groups | Customer segments |
| **Reinforcement** | Rewards and penalties | Maximize reward | Game AI, robots |

**Overfitting** = Model performs great on training data but poorly on new data.
It memorised instead of learning general patterns.
Fix: more data, simpler model, regularization, cross-validation.

---

## 2. Classification

**Easy Definition:**
Classification is a supervised ML task where the model predicts which **category** an input belongs to.
The output is always one of a fixed set of labels.

**Why it is used:**
When the answer is a category, not a number.
"Is this email spam?" "Does this patient have disease?" — these are classification problems.

**Real-World Example:**
> A bank classifies each loan application as **Approved** or **Rejected** based on income, credit score, and age.

**30-Second Interview Answer:**
> Classification is a supervised learning task where the model predicts which category or class an input belongs to.
> It learns from labelled data and draws a decision boundary to separate classes.
> Examples: spam detection, disease diagnosis, sentiment analysis.

**Common Follow-up Questions:**
- What is binary vs multi-class classification?
- What algorithms are used for classification?
- What is a confusion matrix?

**One-Line Revision:**
> Classification = predict a category (Yes/No, Spam/Ham, Disease/Healthy).

---

**Binary Classification** = Only 2 possible outputs (Yes/No, 0/1)
**Multi-class Classification** = 3 or more outputs (Dog/Cat/Bird, Diabetes/Hypertension/Normal)

**Common Classification Algorithms:**
Logistic Regression, Decision Tree, Random Forest, XGBoost, SVM, Naive Bayes, KNN

---

## 3. Classification vs Regression

**Easy Definition:**
Both are supervised learning.
**Classification** predicts a category. **Regression** predicts a number.

**Why it matters:**
Choose wrong type → wrong algorithm → wrong evaluation metric → bad results.

**Real-World Example:**
> Classification → "Will this patient get diabetes? Yes or No?"
> Regression → "What will this patient's blood sugar level be next month? → 145 mg/dL"

**30-Second Interview Answer:**
> Classification predicts a discrete category like Yes/No or Spam/Ham.
> Regression predicts a continuous number like price, temperature, or score.
> Same data — different questions lead to different problem types.

**Comparison Table:**

| | Classification | Regression |
|---|---|---|
| **Output** | Category / Label | Number |
| **Example answer** | Disease: Yes | Blood sugar: 145 |
| **Algorithms** | Logistic Regression, XGBoost, SVM | Linear Regression, Ridge, Lasso |
| **Evaluation** | Accuracy, Precision, Recall, F1 | MAE, RMSE, R² |

**Common Follow-up Questions:**
- Give an example of each from your project.
- Can the same algorithm do both? (Some can — Decision Tree, XGBoost)

**One-Line Revision:**
> Classification = predict a label. Regression = predict a number.

---

## 4. Features vs Labels

**Easy Definition:**
**Features** = The input data you feed the model (columns that describe the example).
**Labels** = The output you want the model to predict (the correct answer).

**Why it matters:**
Without the right features, no model will work well.
Without a label, you can't do supervised learning.

**Real-World Example:**
```
Features (Input)                    Label (Output)
Age | Blood Pressure | Sugar | BMI  →  Disease: Yes / No
```

**30-Second Interview Answer:**
> Features are the input variables — the information given to the model.
> Labels are the output — what the model is trained to predict.
> In a healthcare model, features are patient vitals and the label is disease present or not.

**Key Terms:**
- Features = also called **independent variables** or **X**
- Label = also called **dependent variable**, **target**, or **y**
- **Feature Engineering** = creating new or better features to improve model accuracy

**Common Follow-up Questions:**
- What features did you use in your project?
- How do you select which features to use?
- What is feature engineering?

**One-Line Revision:**
> Features = input (X). Label = output (y). Model learns to map X → y.

---

## 5. Training Data vs Testing Data

**Easy Definition:**
**Training data** = examples the model learns from.
**Testing data** = new unseen examples used to check how well it actually learned.

**Why it is used:**
If you test on the same data you trained on → model gets 100% but hasn't really learned.
The split reveals real performance on unseen data.

**Real-World Example:**
> Like a student studying from a textbook (training) and then sitting for an exam with new questions (testing).
> Getting 100% on practice questions doesn't mean you'll ace the real exam.

**30-Second Interview Answer:**
> We split our dataset — typically 80% for training and 20% for testing.
> The model learns patterns from training data.
> We evaluate its accuracy only on test data that it has never seen before.
> This gives us a realistic measure of performance.

**Common Follow-up Questions:**
- What is cross-validation?
- What split ratio did you use?
- What is the validation set?

> **Cross-validation** = Split data into k parts. Train on k-1, test on 1. Repeat k times. More reliable than single split.
> **Validation set** = A third split used during training to tune the model. Train → Validate → Test.

**One-Line Revision:**
> Train = model learns. Test = we check. Never test on training data.

---

## 6. Accuracy

**Easy Definition:**
Accuracy = percentage of total predictions that were correct.
The most basic evaluation metric.

**Why it is used:**
Quick, easy-to-understand measure of how often the model is right overall.

**Real-World Example:**
> Model predicts 90 out of 100 emails correctly → Accuracy = 90%.

**30-Second Interview Answer:**
> Accuracy is the ratio of correct predictions to total predictions.
> It is simple and intuitive but can be misleading with imbalanced data.
> For example, if 95% of patients are healthy, a model predicting "healthy" always gives 95% accuracy — but it's useless.

**When Accuracy Fails:**
> If dataset is imbalanced (one class is much more common), accuracy is not enough.
> Use Precision, Recall, and F1 instead.

**Common Follow-up Questions:**
- When is accuracy not a good metric?
- What is class imbalance?

**One-Line Revision:**
> Accuracy = correct predictions / total predictions. Unreliable on imbalanced data.

---

## 7. Precision

**Easy Definition:**
Precision = out of all the times the model said "Yes", how many were actually "Yes"?
It measures how trustworthy the model's positive predictions are.

**Why it is used:**
When **false positives are costly** — you don't want the model crying wolf.

**Real-World Example:**
> Spam filter — if the model marks too many legitimate emails as spam (false positives), users get angry.
> High precision = when model says "Spam", it's almost always actually spam.

**30-Second Interview Answer:**
> Precision measures how many of the model's positive predictions were actually correct.
> It is important when the cost of a false alarm is high.
> For example, in a spam filter, low precision means important emails are deleted.

**One-Line Revision:**
> Precision = when model says YES, is it usually right?

---

## 8. Recall

**Easy Definition:**
Recall = out of all the actual "Yes" cases, how many did the model correctly catch?
It measures how good the model is at finding all real positives.

**Why it is used:**
When **missing a real positive is dangerous** — you don't want to miss actual cases.

**Real-World Example:**
> Cancer detection — if the model misses real cancer patients (false negatives), that is life-threatening.
> High recall = model catches most actual cancer cases, even if it occasionally flags healthy people too.

**30-Second Interview Answer:**
> Recall measures how many actual positive cases the model correctly identified.
> It matters when missing a real case is more dangerous than a false alarm.
> In healthcare and disease detection, recall is usually the most important metric.

**Common Follow-up Questions:**
- When would you choose Recall over Precision?
- What is the trade-off between Precision and Recall?

> **Trade-off:** Increasing one usually decreases the other.
> Lowering the prediction threshold → catches more positives (higher Recall, lower Precision).
> Raising the threshold → fewer false alarms (higher Precision, lower Recall).

**One-Line Revision:**
> Recall = did the model catch all real positives? Critical in healthcare.

---

## 9. F1 Score

**Easy Definition:**
F1 Score is the **balance between Precision and Recall**.
It gives a single number that summarises both.
Used when you need to care about both — not just one.

**Why it is used:**
When data is imbalanced AND both false positives and false negatives matter.

**Real-World Example:**
> In healthcare, you want high recall (don't miss sick patients) but also reasonable precision (don't over-alarm).
> F1 Score captures this balance in one number.

**30-Second Interview Answer:**
> F1 Score is the harmonic mean of Precision and Recall.
> It is the best metric when data is imbalanced and both metrics matter equally.
> A high F1 Score means the model is good at both finding positives and being accurate about them.

**Simple Rule:**
```
Use Accuracy  → when classes are balanced
Use Recall    → when missing positives is dangerous (healthcare)
Use Precision → when false alarms are costly (spam filter)
Use F1        → when you need balance between both on imbalanced data
```

**One-Line Revision:**
> F1 = balance of Precision and Recall. Best metric for imbalanced datasets.

---

---

## 10. XGBoost

**Easy Definition:**
XGBoost (eXtreme Gradient Boosting) is a powerful ML algorithm that builds many decision trees **one after another**, where each new tree fixes the mistakes of the previous one.
It is one of the most accurate and widely used algorithms for structured data.

**Why it is used:**
- Very high accuracy on tabular/structured data (CSV, Excel, patient records)
- Handles missing values automatically
- Doesn't overfit easily
- Fast

**Real-World Example:**
> Banks use XGBoost for credit risk scoring.
> Insurance companies use it to predict claim fraud.
> Hospitals use it to predict patient readmission risk.

**30-Second Interview Answer:**
> XGBoost is an ensemble algorithm that uses boosting — it builds decision trees sequentially.
> Each tree corrects the errors of the previous one.
> It is popular because it gives high accuracy, handles missing values, has built-in regularisation, and provides feature importance.
> On Kaggle ML competitions, XGBoost wins the majority of structured data problems.

---

### How XGBoost Works (Simple)

Think of it as a **team correcting each other's mistakes:**

```
Tree 1 → makes some wrong predictions
Tree 2 → focuses on what Tree 1 got wrong → corrects those
Tree 3 → focuses on what Tree 2 still got wrong → corrects more
...
Final answer → all trees vote together → very accurate
```

This is called **Boosting** — sequential, error-correcting tree building.

---

### XGBoost vs Decision Tree

| | Decision Tree | XGBoost |
|---|---|---|
| **Number of trees** | 1 | Many (100s) |
| **Overfitting** | Overfits easily | Controlled by regularisation |
| **Accuracy** | Low-moderate | High |
| **Missing values** | Needs handling | Handles automatically |
| **Speed** | Fast | Slower but worth it |

---

### XGBoost vs Random Forest

| | Random Forest | XGBoost |
|---|---|---|
| **How trees built** | Independently (parallel) | Sequentially (one corrects previous) |
| **Technique** | Bagging | Boosting |
| **Accuracy** | Good | Usually better |
| **Overfitting risk** | Low | Low (regularisation) |
| **When to use** | Quick baseline | When you need best accuracy |

---

### Key Terms to Know

| Term | Simple Meaning |
|---|---|
| `n_estimators` | Number of trees to build |
| `max_depth` | How deep each tree grows |
| `learning_rate` | How much each tree corrects (small = careful = better) |
| **Feature importance** | Which input features mattered most for predictions |
| **Regularisation** | Built-in penalty that prevents overfitting |

---

### Advantages of XGBoost
- ✅ Very high accuracy on structured/tabular data
- ✅ Handles missing values natively
- ✅ Built-in regularisation — prevents overfitting
- ✅ Feature importance — tells you which features matter
- ✅ Fast (parallel processing)
- ✅ Works out of the box with minimal tuning

### Limitations of XGBoost
- ❌ Not great for image, audio, or raw text data (use CNNs, RNNs, Transformers)
- ❌ Slower than a single decision tree
- ❌ Many parameters — takes effort to tune perfectly
- ❌ Harder to explain than a simple decision tree

**Common Follow-up Questions:**
- What is boosting vs bagging?
- Why XGBoost over Random Forest?
- What is feature importance?
- What is overfitting and how does XGBoost prevent it?

**One-Line Revision:**
> XGBoost = many trees built sequentially, each correcting the previous one. Best for tabular data.

---

---

## 11. NLP Basics

**Easy Definition:**
NLP (Natural Language Processing) is the field of AI that enables computers to understand and work with human language — text or speech.
Computers understand numbers, not words — NLP converts text into a form machines can process.

**Why it is used:**
- Analyse customer reviews, social media, medical reports at scale
- Build chatbots, search engines, translation systems
- Extract meaning from unstructured text data

**Real-World Example:**
> Google Search — doesn't just match keywords, understands what you actually mean.
> Amazon reviews — automatically classified as helpful/unhelpful, positive/negative.

**30-Second Interview Answer:**
> NLP is a branch of AI that enables computers to understand, process, and generate human language.
> Core tasks include tokenization, sentiment analysis, text classification, and named entity recognition.
> It is used in chatbots, spam filters, voice assistants, and translation.

**Common Follow-up Questions:**
- What is tokenization?
- What is stopword removal?
- Name 3 NLP applications.

**One-Line Revision:**
> NLP = AI for understanding and working with human language (text and speech).

---

## 12. Tokenization

**Easy Definition:**
Tokenization is the process of **splitting text into smaller pieces called tokens**.
A token can be a word, part of a word, or a character.
It is always the first step in any NLP pipeline.

**Why it is used:**
Computers can't process raw sentences — you must break text into tokens first, then convert to numbers.

**Real-World Example:**
```
Sentence: "I love machine learning"

Word tokens:   ["I", "love", "machine", "learning"]

Character tokens: ["I", " ", "l", "o", "v", "e", ...]

Subword tokens (used in LLMs): ["I", "love", "ma", "chine", "learn", "ing"]
```

**30-Second Interview Answer:**
> Tokenization is the process of breaking text into smaller units called tokens.
> It is the first step in any NLP pipeline — you cannot feed raw sentences to a model.
> Word tokenization splits by spaces. Subword tokenization, used in LLMs, splits rare words into known pieces.

**Why Subword Tokenization?**
> A word like "unbelievable" may not be in the vocabulary.
> Subword splits it into "un" + "believ" + "able" — all known pieces.
> This way, even new/rare words can be handled.

**Common Follow-up Questions:**
- What happens after tokenization?
- What are stopwords?
- What is stemming vs lemmatization?

> **Stopwords** = Common words removed before processing (is, the, a, an, of)
> **Stemming** = Cut word to root crudely — "running" → "run", "better" → "bett"
> **Lemmatization** = Convert to proper dictionary root — "running" → "run", "better" → "good"

**One-Line Revision:**
> Tokenization = split text into tokens. First step of every NLP pipeline.

---

## 13. Sentiment Analysis

**Easy Definition:**
Sentiment Analysis detects the **emotion or opinion** in a piece of text.
Output is usually: Positive, Negative, or Neutral.

**Why it is used:**
- Understand customer feedback at scale
- Monitor brand reputation on social media
- Analyse product reviews automatically

**Real-World Example:**
> Amazon — millions of product reviews come in daily.
> Sentiment analysis automatically tags them as positive/negative and generates the star rating summary.

**30-Second Interview Answer:**
> Sentiment Analysis is an NLP task that classifies text based on the emotional tone — positive, negative, or neutral.
> It is a text classification problem where the model is trained on labelled review data.
> Use cases include product review analysis, social media monitoring, and patient feedback analysis.

**Common Follow-up Questions:**
- How is sentiment analysis implemented?
- What are the challenges? (Sarcasm, context, slang)
- Give a real-world example.

**Challenges:**
- Sarcasm: "Oh great, another delay." → actually Negative
- Context: "This movie is sick!" → Positive (slang)
- Negation: "Not bad" → Positive (tricky to parse)

**One-Line Revision:**
> Sentiment Analysis = classify text as Positive, Negative, or Neutral.

---

## 14. Text Classification

**Easy Definition:**
Text Classification assigns a **predefined label or category** to a piece of text.
Sentiment Analysis is a special case of text classification.
But text classification covers many more tasks.

**Why it is used:**
Automates categorisation of large volumes of text that humans cannot manually sort.

**Real-World Example:**
> Email spam detection → Spam / Not Spam
> News article tagging → Sports / Politics / Tech / Entertainment
> Hospital ticket routing → Emergency / Routine / Billing

**30-Second Interview Answer:**
> Text Classification is an NLP task where a model assigns a category to an input text.
> The pipeline is: tokenize → remove stopwords → convert to vectors (TF-IDF or embeddings) → feed to ML model.
> Common applications include spam detection, sentiment analysis, and topic categorisation.

**Basic Pipeline:**
```
Raw Text
   ↓ Tokenize
   ↓ Remove stopwords
   ↓ Stemming / Lemmatization
   ↓ Vectorization (TF-IDF or Word Embeddings)
   ↓ ML Model (Logistic Regression / Naive Bayes / XGBoost)
   ↓ Predicted Label
```

**Key NLP Terms for Interviews:**

| Term | Simple Meaning |
|---|---|
| **TF-IDF** | Gives high score to words that are frequent in one doc but rare overall |
| **Bag of Words** | Represent text as word counts — ignores word order |
| **Word Embeddings** | Words as number vectors — similar words are close together |
| **Word2Vec** | A popular embedding model — "king" − "man" + "woman" ≈ "queen" |
| **Naive Bayes** | Probability-based classifier — very popular for text |

**One-Line Revision:**
> Text Classification = assign a category label to text using NLP pipeline + ML model.

---

---

## 15. LLM Basics

**Easy Definition:**
LLM (Large Language Model) is a very large AI model trained on billions of words of text.
It can understand and generate human-like text across many tasks — writing, summarising, answering, translating, coding.

**Why it is used:**
One general model replaces many specific models.
No task-specific training needed for most use cases.

**Real-World Example:**
> ChatGPT — write an email, summarise a document, debug code, explain a concept — all with one model.

**30-Second Interview Answer:**
> An LLM is a large AI model trained on massive text datasets using the Transformer architecture.
> It can perform many language tasks — Q&A, summarisation, translation, and code generation — without task-specific training.
> Examples include GPT-4, Gemini, Claude, and Llama.

---

### Examples of LLMs

| LLM | Company | Key Note |
|---|---|---|
| **GPT-4 / ChatGPT** | OpenAI | Most widely used |
| **Gemini** | Google DeepMind | Powers Google AI features |
| **Claude** | Anthropic | Long context, safety-focused |
| **Llama 3** | Meta | Open-source — can run locally |
| **Mistral** | Mistral AI | Small but powerful open model |

---

### Traditional ML vs LLM

| | Traditional ML (XGBoost) | LLM |
|---|---|---|
| **Data type** | Structured tables (CSV) | Text, code, images |
| **Training** | One specific task | General text → many tasks |
| **Output** | Number or category | Full text response |
| **Size** | Small (MB) | Huge (GB to TB) |
| **Use** | Disease prediction | Q&A, summarisation, coding |

**Common Follow-up Questions:**
- Name 3 LLMs.
- What is hallucination in LLMs?
- What is RAG?
- What is fine-tuning?

**One-Line Revision:**
> LLM = massive model trained on billions of words. Understands and generates human-like text.

---

## 16. Prompt Engineering

**Easy Definition:**
Prompt Engineering is the skill of **writing clear and specific instructions to an LLM** to get accurate and useful responses.
The way you phrase your input (prompt) directly affects the quality of the output.

**Why it is used:**
LLMs are very powerful but vague prompts give vague answers.
Well-crafted prompts unlock much better results — without changing the model.

**Real-World Example:**

| Weak Prompt | Better Prompt |
|---|---|
| "Explain ML" | "Explain machine learning in 3 simple points for a CSE fresher" |
| "Write code" | "Write a Python function to classify disease using XGBoost with comments" |
| "Summarise this" | "Summarise this patient report in 2 sentences, focus on risk factors" |

**30-Second Interview Answer:**
> Prompt Engineering is the practice of crafting effective inputs to get accurate outputs from an LLM.
> Since LLMs are sensitive to how questions are phrased, a well-structured prompt dramatically improves response quality.
> Techniques include zero-shot, few-shot, and chain-of-thought prompting.

**Types of Prompting (Know These):**

| Type | What it is | Example |
|---|---|---|
| **Zero-shot** | Ask directly with no examples | "Translate this to Hindi: ..." |
| **Few-shot** | Give 2-3 examples first, then ask | Show examples → model follows pattern |
| **Chain-of-thought** | Ask model to "think step by step" | Better for reasoning and math |

**Common Follow-up Questions:**
- What is zero-shot vs few-shot prompting?
- How does prompt quality affect LLM output?

**One-Line Revision:**
> Prompt Engineering = write better instructions → get better answers from LLMs.

---

## 17. Hallucination

**Easy Definition:**
Hallucination is when an LLM **confidently generates false or made-up information** that sounds believable.
The model doesn't know what it doesn't know — it always generates something, even when it's wrong.

**Why it happens:**
LLMs are trained to generate statistically likely next words — not to verify facts.
They don't access real-time data or databases by default.

**Real-World Example:**
> Ask ChatGPT: "List the publications of Professor XYZ"
> If Professor XYZ doesn't exist, ChatGPT may generate convincing but completely fake paper titles and journals.

**30-Second Interview Answer:**
> Hallucination is when an LLM produces factually incorrect information with high confidence.
> It happens because the model generates plausible-sounding text based on training patterns, not actual facts.
> It is a major limitation of LLMs in high-stakes domains like healthcare and law.
> RAG is the main solution — it grounds the model's answers in real documents.

**How to Reduce Hallucination:**
- Use RAG — give the model real documents to read from
- Tell the model to say "I don't know" when unsure
- Verify outputs with trusted sources

**Common Follow-up Questions:**
- What is hallucination in LLMs?
- How do you solve hallucination?
- What is RAG?

**One-Line Revision:**
> Hallucination = LLM confidently gives wrong answers. Solved by RAG and verification.

---

## 18. RAG (Retrieval-Augmented Generation)

**Easy Definition:**
RAG is a technique where you **give the LLM your own documents as context** before asking a question.
Instead of relying on training memory (which may be outdated or wrong), the LLM reads your real documents and answers from them.

**Why it is used:**
- Reduces hallucination — model answers from real sources
- No need to retrain the model — just plug in your documents
- Allows LLMs to work with private, updated data

**Real-World Example:**
> A hospital chatbot that answers from actual medical guidelines and patient records — not from the LLM's training memory.

**How RAG Works (Simple):**
```
User asks: "What is the patient's latest blood pressure reading?"
       ↓
RAG system searches your documents/database
       ↓
Finds: "BP reading on 15 June: 140/90 mmHg"
       ↓
Sends to LLM: [found document] + [user question]
       ↓
LLM answers from real document: "Latest BP is 140/90 (15 June)"
```

**30-Second Interview Answer:**
> RAG stands for Retrieval-Augmented Generation.
> It is a technique where relevant documents are retrieved from a database and passed to the LLM along with the user's question.
> The LLM answers using those real documents instead of relying on training memory.
> RAG reduces hallucination and allows LLMs to work with private or updated data without retraining.

**RAG vs Fine-Tuning:**

| | RAG | Fine-Tuning |
|---|---|---|
| **What changes** | Nothing in model — feeds documents at query time | Model weights are updated |
| **Cost** | Low | High (GPU compute) |
| **Updates** | Easy — just add/change documents | Hard — retrain every time |
| **Best for** | Answering from your documents | Teaching model a new style/domain |

**Common Follow-up Questions:**
- What is RAG?
- How is RAG different from fine-tuning?
- Why use RAG in healthcare?

**One-Line Revision:**
> RAG = retrieve real documents → feed to LLM → accurate answers without retraining.

---

## 19. Fine-Tuning

**Easy Definition:**
Fine-Tuning is taking a pre-trained LLM and **continuing its training on your specific domain data**.
The model already knows general language — fine-tuning teaches it the style, vocabulary, and patterns of your specific field.

**Why it is used:**
When you need the model to behave differently — use specific terminology, follow a certain style, or answer in a domain-specific way.

**Real-World Example:**
> A general LLM fine-tuned on medical records and clinical notes becomes a **Medical LLM** that understands clinical language, abbreviations, and terminology much better than the base model.

**30-Second Interview Answer:**
> Fine-tuning is the process of training a pre-trained LLM further on domain-specific data.
> It adapts the model's behaviour to a particular use case — like medical Q&A or legal document analysis.
> It requires GPU compute and labelled examples, unlike RAG which just needs documents.

**Fine-Tuning vs RAG — Quick Comparison:**

| | RAG | Fine-Tuning |
|---|---|---|
| **Changes model?** | No | Yes |
| **Cost** | Low | High |
| **Use when** | You have documents to search | You want different model behaviour |
| **Fresher needs to know?** | Concept + definition | High-level only |

**Common Follow-up Questions:**
- What is fine-tuning vs RAG?
- When would you fine-tune instead of using RAG?

**One-Line Revision:**
> Fine-tuning = retrain LLM on your data to change its behaviour. Expensive but powerful.

---
---

# 📋 One-Page Revision Sheet

```
╔══════════════════════════════════════════════════════════════════════╗
║              AI/ML PLACEMENT — QUICK REVISION SHEET                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  ML BASICS                                                            ║
║  ML = Computer learns from data, no manual rules                      ║
║  Supervised = Labelled data → predict output                          ║
║  Unsupervised = No labels → find groups                               ║
║  Reinforcement = Agent learns by reward/penalty                       ║
║  Overfitting = Great on training, bad on new data                     ║
╠══════════════════════════════════════════════════════════════════════╣
║  CLASSIFICATION & METRICS                                             ║
║  Classification = predict a category (Yes/No, label)                  ║
║  Regression = predict a number (price, score)                         ║
║  Features = Input (X) | Label = Output (y)                            ║
║  Train = learn | Test = evaluate on unseen data                       ║
║  Accuracy = correct/total (bad for imbalanced data)                   ║
║  Precision = when model says YES, is it usually right?                ║
║  Recall = did model catch all real positives? (critical in health)    ║
║  F1 = balance of Precision + Recall                                   ║
║  Confusion Matrix: TP, TN, FP, FN                                     ║
╠══════════════════════════════════════════════════════════════════════╣
║  XGBOOST                                                              ║
║  eXtreme Gradient Boosting                                            ║
║  Builds trees SEQUENTIALLY — each fixes previous errors               ║
║  Boosting (XGBoost) ≠ Bagging (Random Forest)                         ║
║  Handles missing values | Has regularisation | Feature importance      ║
║  Best for structured/tabular data                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  NLP                                                                  ║
║  NLP = AI for human language                                          ║
║  Tokenization = split text into tokens (first step always)            ║
║  Stopwords = remove is/the/a | Lemmatize > Stemming                   ║
║  TF-IDF = word importance score                                        ║
║  Sentiment = Positive / Negative / Neutral                            ║
║  Text Classification = assign a label to text                         ║
╠══════════════════════════════════════════════════════════════════════╣
║  LLMs                                                                 ║
║  LLM = Large Language Model, trained on billions of words             ║
║  GPT-4, Gemini, Claude, Llama, Mistral                                ║
║  Prompt Engineering = write better inputs → better outputs            ║
║  Hallucination = LLM confidently gives wrong answer                   ║
║  RAG = retrieve real docs → give to LLM → accurate answers           ║
║  Fine-Tuning = retrain LLM on your domain data (expensive)            ║
║  Context Window = max text LLM can read at once                       ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

# 🎯 Top 30 AI Interview Questions for Freshers

---

### Machine Learning (Q1–Q8)

**Q1: What is Machine Learning?**
> ML is teaching a computer to learn patterns from data without writing rules manually.
> You give examples, the model learns, and it predicts for new inputs.

**Q2: What are the 3 types of Machine Learning?**
> Supervised (labelled data, predict output), Unsupervised (no labels, find patterns), Reinforcement (agent learns by reward/penalty).

**Q3: What is overfitting? How do you prevent it?**
> Overfitting = model performs great on training data but poorly on new data.
> Prevention: more data, simpler model, regularisation, cross-validation.

**Q4: What is the difference between training data and testing data?**
> Training data = model learns from it. Testing data = unseen data used to evaluate real performance.

**Q5: What is cross-validation?**
> Split data into k folds. Train on k-1, test on 1. Repeat k times. More reliable than a single train-test split.

**Q6: What are features and labels?**
> Features = input columns (X). Labels = output column (y). Model learns to map features → label.

**Q7: What is the difference between supervised and unsupervised learning?**
> Supervised = labelled data, predict output. Unsupervised = no labels, discover hidden structure.

**Q8: What is underfitting?**
> Model is too simple to capture patterns — performs poorly even on training data.
> Fix: use a more complex model, add more features.

---

### Classification & Metrics (Q9–Q16)

**Q9: What is the difference between classification and regression?**
> Classification = predict a category (yes/no). Regression = predict a number (price, blood sugar value).

**Q10: What is binary vs multi-class classification?**
> Binary = 2 classes (disease/no disease). Multi-class = 3+ classes (dog/cat/bird).

**Q11: What is a confusion matrix?**
> A table showing TP (correct yes), TN (correct no), FP (false alarm), FN (missed real case).

**Q12: What is accuracy and when is it not useful?**
> Accuracy = correct predictions / total. Not useful when classes are imbalanced.
> Example: 95% healthy patients → always predicting healthy = 95% accuracy but useless.

**Q13: What is Precision?**
> Of all predictions where model said "Yes", how many were actually "Yes"?
> Use when false positives are costly (spam filter).

**Q14: What is Recall?**
> Of all actual "Yes" cases, how many did the model correctly detect?
> Use when missing a real positive is dangerous (disease detection, cancer screening).

**Q15: What is F1 Score?**
> Harmonic mean of Precision and Recall. Best metric for imbalanced datasets when both matter.

**Q16: When would you choose Recall over Precision?**
> In healthcare — missing a real sick patient is life-threatening, so high Recall is prioritised over Precision.

---

### XGBoost (Q17–Q21)

**Q17: What is XGBoost?**
> eXtreme Gradient Boosting. Builds decision trees sequentially — each corrects errors of the previous.
> High accuracy, handles missing values, prevents overfitting, gives feature importance.

**Q18: What is the difference between Boosting and Bagging?**
> Bagging = build trees independently in parallel, average results (Random Forest).
> Boosting = build trees sequentially, each corrects previous errors (XGBoost).

**Q19: Why XGBoost over a single Decision Tree?**
> Single tree overfits easily and is less accurate.
> XGBoost uses many trees, regularisation, and sequential error correction → much more accurate and reliable.

**Q20: Why XGBoost over Random Forest?**
> Random Forest uses bagging — trees independent, accuracy averaged.
> XGBoost uses boosting — trees sequential, errors corrected → usually higher accuracy.
> XGBoost also has built-in regularisation and feature importance.

**Q21: What is feature importance in XGBoost?**
> XGBoost tells you which input features contributed most to predictions.
> Useful for explainability — helps doctors/analysts trust and understand the model.

---

### NLP (Q22–Q26)

**Q22: What is NLP? Give 3 applications.**
> NLP = AI for human language understanding and generation.
> Applications: Chatbots, Sentiment Analysis, Machine Translation, Spam Detection, Voice Assistants.

**Q23: What is tokenization?**
> Breaking text into smaller pieces called tokens.
> First step of every NLP pipeline. Computers can't process raw sentences — must tokenize first.

**Q24: What is the difference between stemming and lemmatization?**
> Stemming = crude cut to root ("better" → "bett") — fast but sometimes wrong.
> Lemmatization = proper dictionary root ("better" → "good") — accurate but slower.

**Q25: What is TF-IDF?**
> Term Frequency–Inverse Document Frequency.
> Gives high score to words that are common in one document but rare across all documents.
> Identifies the most meaningful/unique words in text.

**Q26: What is sentiment analysis?**
> Classifying text as Positive, Negative, or Neutral based on the emotional tone.
> Used in review analysis, social media monitoring, customer feedback systems.

---

### LLMs (Q27–Q30)

**Q27: What is an LLM? Give examples.**
> Large Language Model — trained on billions of words, can understand and generate human text.
> Examples: GPT-4, Gemini, Claude, Llama, Mistral.

**Q28: What is hallucination in LLMs? How do you handle it?**
> When LLM generates confident but factually wrong information.
> Handled by: RAG (give real documents), asking model to say "I don't know", verification.

**Q29: What is RAG?**
> Retrieval-Augmented Generation. Retrieve relevant documents from a database → pass to LLM with the question.
> LLM answers from real documents, not training memory. Reduces hallucination, no retraining needed.

**Q30: What is fine-tuning? How is it different from RAG?**
> Fine-tuning = continue training the LLM on domain-specific data. Changes the model. Expensive.
> RAG = feed documents at query time. Model unchanged. Cheap and flexible.

---

# ⚡ 5-Minute Revision Notes

```
Before interview, read only this section:

ML:
- Learn from data, no manual rules
- Supervised/Unsupervised/Reinforcement
- Overfitting = great on train, bad on test
- Train 80% / Test 20%

Metrics:
- Accuracy = correct/total (bad for imbalanced)
- Precision = when I say YES, am I right?
- Recall = did I catch all real YESes? (healthcare = prioritise this)
- F1 = balance of both

XGBoost:
- Sequential trees, each fixes previous errors = Boosting
- Bagging (Random Forest) = parallel trees, average
- Handles missing values, regularisation, feature importance
- Best for structured/tabular data

NLP:
- Tokenize first → remove stopwords → stem/lemmatize → TF-IDF → model
- Sentiment = Positive/Negative/Neutral
- TF-IDF = words rare overall but frequent in doc = important

LLMs:
- GPT-4, Gemini, Claude, Llama
- Hallucination = confident wrong answers
- RAG = retrieve docs → give to LLM → accurate
- Fine-tuning = retrain model on domain data
- Prompt Engineering = better input → better output
```

---

# 🕐 1-Minute Explanations

---

**Machine Learning (1 min):**
> Machine Learning is teaching a computer to learn from data without writing explicit rules.
> It has 3 types: Supervised learning uses labelled data to predict outputs like disease yes or no.
> Unsupervised learning finds hidden patterns in unlabelled data like customer groups.
> Reinforcement learning uses rewards and penalties to train an agent.
> The key idea is: give data, model learns patterns, model predicts on new data.

---

**Classification (1 min):**
> Classification is a supervised ML task where the model predicts which category an input belongs to.
> Binary classification has two outputs like Yes/No. Multi-class has more, like disease type.
> We evaluate it using Accuracy, Precision, Recall, and F1 Score.
> Recall is most important in healthcare because missing a real sick patient is more dangerous than a false alarm.

---

**XGBoost (1 min):**
> XGBoost stands for eXtreme Gradient Boosting.
> It builds many decision trees one after another — each tree fixes the mistakes of the previous one.
> This is called Boosting, which is different from Bagging used in Random Forest.
> XGBoost is popular because it gives high accuracy on structured data, handles missing values automatically, has built-in regularisation, and provides feature importance to explain predictions.

---

**NLP (1 min):**
> NLP stands for Natural Language Processing — the branch of AI for understanding human language.
> The basic pipeline is: tokenize the text, remove stopwords, apply lemmatization, convert to vectors using TF-IDF or embeddings, then feed into a classifier.
> Key tasks are sentiment analysis, text classification, and chatbots.
> Real-world uses include Gmail spam filter, Amazon review analysis, and Google Translate.

---

**LLMs (1 min):**
> LLM stands for Large Language Model — massive AI trained on billions of words that understands and generates human-like text.
> Examples are GPT-4, Gemini, Claude, and Llama.
> Key challenge is hallucination — the model confidently gives wrong answers.
> RAG solves this by retrieving real documents and giving them to the LLM as context.
> Prompt Engineering is the skill of writing clear instructions to get better responses from LLMs.

---

# ✅ What Interviewers Expect vs ❌ Don't Ask

---

## ✅ Interviewers EXPECT Freshers to Know

| Topic | What They Expect |
|---|---|
| ML types | Supervised / Unsupervised / Reinforcement + one example each |
| Overfitting | Definition + how to prevent |
| Features & Labels | What they are + example from your project |
| Accuracy vs Recall | Why Recall matters more in healthcare |
| F1 Score | What it is and when to use it |
| Confusion matrix | TP, TN, FP, FN — what each means |
| XGBoost | What it is, why over Decision Tree, boosting vs bagging |
| Feature importance | What it tells us |
| Tokenization | What it is + why it's the first NLP step |
| Sentiment analysis | Definition + real-world example |
| TF-IDF | Simple explanation |
| LLM | Definition + 3 examples |
| Hallucination | What it is + how to handle it |
| RAG | What it is + how it differs from fine-tuning |
| Prompt Engineering | What it is + example |
| Project explanation | Problem → Data → Algorithm choice → Metrics → Result |

---

## ❌ Interviewers Usually DON'T Ask Freshers

| Topic | Why They Skip It |
|---|---|
| Backpropagation math | Too advanced |
| Gradient Descent derivation | Research level |
| Transformer attention math | Specialist topic |
| XGBoost loss function | Advanced internals |
| BERT / GPT architecture depth | Research level |
| Hyperparameter tuning strategies | Experience level |
| Custom neural network design | Deep learning specialisation |
| MLOps / Model deployment | Usually a separate role |
| Exact F1 formula | Knowing the concept is enough |
| Kullback-Leibler divergence | PhD level |

---

## 💡 Golden Rules for AI Questions in Interviews

```
1. Always link to your project:
   "In our healthcare project, we used XGBoost because..."

2. Be honest about depth:
   "I know XGBoost conceptually and used it in my project.
    I haven't implemented it from scratch."

3. Know WHY you chose your algorithm:
   "We tried Logistic Regression, Random Forest, and XGBoost.
    XGBoost gave the best F1 score on our imbalanced dataset."

4. Know your metric choice:
   "We used Recall as the primary metric because missing a sick
    patient is more dangerous than a false alarm."

5. Know your limitations:
   "Our model has limitations — the training data was limited to
    one hospital, so it may not generalise to all populations."

6. For LLMs — just the concept is enough:
   "I understand what LLMs are, how RAG works conceptually,
    and the hallucination problem. We used RAG in our chatbot feature."
```

---

> 📌 Part of [Placement-Preparation-Hub](https://github.com/Omkar4112/Placement-Preparation-Hub)
> Topics: ML | Classification | XGBoost | NLP | LLMs | CSE Fresher Placement Guide
