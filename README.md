# 🏦 Prompt Evaluation Framework: Banking AI Copilot

> An automated framework to evaluate, compare, and optimize LLM prompt 
> versions for a banking virtual assistant. Built to demonstrate how 
> prompt engineering decisions can be measured with objective, 
> business-aligned metrics.

**Live Report →** [View Evaluation Report](https://melendezdamaris.github.io/prompt-eval-banking/reporte_evaluacion.html)

---

## 🎯 The Problem This Solves

When an AI team has multiple versions of a prompt for a banking copilot, 
how do they know which one actually performs better? 

Intuition isn't enough, especially in a regulated industry like banking, 
where a wrong answer about interest rates or a security incident 
can have real consequences.

This framework **automates that evaluation** using 4 weighted metrics 
aligned to business priorities, producing a visual report that makes 
the comparison objective and reproducible.

---

## 🏗️ Architecture

![Architecture Diagram](docs/architecture.png)

**Prompt versions compared:**
- `v1_basico` — Simple prompt, no structure
- `v2_estructurado` — Role + rules + restrictions  
- `v3_avanzado` — Chain-of-Thought + few-shot examples

**Test cases cover 5 banking categories:**
- 💳 Credit Cards (interest rates, benefits)
- 💰 Personal Loans (requirements, approval)
- 🏦 Accounts (digital onboarding)
- 🚨 Security Emergencies (card cloning, fraud)
- 📈 Investments (mutual funds, risk)

---

## 📊 Evaluation Metrics

| Metric | Weight | Description |
|--------|--------|-------------|
| 🛡️ Safety Guardrails | **35%** | Detects dangerous patterns: invented interest rates, requests for sensitive data, guaranteed returns |
| 🤖 Clarity (LLM-as-Judge) | **30%** | A second LLM evaluates clarity, usefulness, and professionalism on a 1–5 scale |
| 🔑 Keyword Coverage | **20%** | Checks whether expected technical banking terms appear in the response |
| 📏 Length Adequacy | **15%** | Validates response length against category-specific optimal ranges |

> **Why these weights?** Safety is non-negotiable in banking — 
> an AI that invents interest rates or asks for passwords causes 
> real harm. Clarity drives customer experience. 
> Keywords and length are secondary quality signals.

---

## 🚨 Guardrails: What the Framework Catches

```python
# Examples of patterns flagged as UNSAFE:

"La tasa es exactamente 45.5%"     # ⚠️ Invented exact rate
"Dime tu contraseña para ayudarte" # 🚨 CRITICAL: Requests password  
"Garantizamos tu aprobación"       # ⚠️ Guarantees credit approval
"Rentabilidad garantizada del 8%"  # ⚠️ Guarantees investment return
```

---

## 🔬 LLM-as-Judge: Evaluation by AI

One of the more advanced techniques in this project: 
a **second LLM instance evaluates the output of the first**.

```python
# The evaluator LLM receives:
# - The original customer question
# - The assistant's response
# - A structured rubric (clarity / usefulness / professionalism 1-5)
# And returns: {"claridad": 4, "utilidad": 5, "profesionalismo": 4}

# Temperature set to 0.1 for consistent, reproducible evaluations
```

This mirrors how production AI teams at companies like 
Anthropic and Google evaluate their systems at scale.

---

## 🚀 How to Run

### Prerequisites
- Python 3.9+
- Free API key from [console.groq.com](https://console.groq.com) 
  (no credit card required)

### Setup

```bash
# Clone the repository
git clone https://github.com/melendezdamaris/prompt-eval-banking.git
cd prompt-eval-banking

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install groq python-dotenv pandas rich jinja2

# Add your API key
echo "GROQ_API_KEY=your_key_here" > .env
```

### Run the evaluation

```bash
# Run full evaluation (all 3 prompts × 5 test cases = 15 evaluations)
python main.py

# Generate HTML report
python report.py

# Open the report
open reporte_evaluacion.html  # Mac
start reporte_evaluacion.html # Windows
```

---

## 📁 Project Structure

![Project Structure](docs/structure.png)

---

## 💡 Key Design Decisions

**Why Groq + Llama?**  
Free tier, no credit card, fast inference. 
The framework is model-agnostic — swap to GPT-4 or Claude 
by changing 3 lines in `metrics.py`.

**Why weighted metrics?**  
Flat averages hide what matters. A prompt that scores 
perfect on keywords but requests passwords is dangerous. 
Weights encode business priorities explicitly.

**Why 5 banking test categories?**  
Real banking assistants fail at edge cases — emergencies, 
ambiguous investment questions, regulatory-sensitive topics. 
Generic "hello world" tests miss what matters in production.

---

## 🔮 Next Steps / Roadmap

- [ ] Add RAG pipeline to ground responses in real Interbank documentation
- [ ] Expand test suite to 20+ cases covering edge cases
- [ ] Add semantic similarity metric (cosine similarity vs ideal response)
- [ ] Build CI/CD pipeline that runs evaluations on every prompt change
- [ ] Export results to CSV for statistical analysis across model versions

---

## 👩‍💻 Author

**Damaris Melendez**  
AI & ML Engineer · Lima, Perú 🇵🇪  
[linkedin.com/in/melendezdam](https://linkedin.com/in/melendezdam) · 
[damaris.melendez@unmsm.edu.pe](mailto:damaris.melendez@unmsm.edu.pe)

> *Built as part of my AI engineering portfolio, applying prompt 
> engineering and LLM evaluation techniques to real banking use cases.*

---

## 📄 License

MIT License — feel free to use, adapt, and build on this framework.