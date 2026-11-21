# THUFIR - A Virtual Ethics Advisor
## Setup

The application requires GNU/Linux or Windows with WSL (Windows Subsystem for Linux). Python dependencies are managed using [uv](https://docs.astral.sh/uv/).

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ntua-el21040/ethico.git
   cd ethico
   ```

2. **Install uv and essential packages** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   sudo apt install -y build-essential python3-dev unzip
   ```

3. **Install project dependencies:**
   ```bash
   uv sync --locked
   ```
   This creates a virtual environment (`.venv`) and installs the dependencies specified in `pyproject.toml` and `uv.lock`.

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to provide your OpenAI API key and Supabase configuration.

5. **Install the HERA ethics engine:**

   HERA needs to be set up manually after entering the virtual environment:
   ```bash
   source .venv/bin/activate
   cd ethics_engine
   chmod +x ./cudd-3.0.0/configure
   python3 setup.py install
   cd ..
   deactivate
   ```

6. **Run the application:**
   ```bash
   uv run reflex run
   ```

   The application will typically be accessible at `http://localhost:3000`.


## System Description

The system is designed as an interactive and transparent ethics advisor. It combines an LLM-powered chatbot, which elicits information about moral dilemmas from users, with a deterministic ethics engine that formally models and evaluates those dilemmas.

The system aims to help users understand and evaluate moral dilemmas, as well as explore the ethical theories that can be applied to moral decision-making.

### Scope

The system is limited to moral dilemmas that can be represented within HERA's formalism. The LLM-powered chatbot is responsible for identifying and enforcing these constraints during user interactions.

A dilemma must satisfy the following conditions to be modeled and evaluated:

1. **Binary choice:** The dilemma involves exactly two alternatives: performing an action or refraining from it.
2. **Known action:** The action under consideration is clearly identified.
3. **Known consequences:** The consequences of the action are known.
4. **Known causal relationships:** The causal links between the action and its consequences are established.
5. **Comparable utilities:** The utility of each consequence can be ranked relative to the others.
6. **Identifiable moral patients:** The individuals or entities affected by the action are known.
7. **Identifiable agent goals:** The agent's goals can be determined from the dilemma's description.
8. **Deterministic outcomes:** Probabilistic or uncertain outcomes are excluded; each consequence either occurs or does not.

Dilemmas that do not satisfy these conditions fall outside the system's scope and cannot be formally evaluated.

## **Ethical Frameworks**

The system implements two ethical principles:

- **Act Utilitarianism:** Evaluates actions according to their consequences for overall utility.
- **Kantian Humanity Principle:** Evaluates whether an action respects persons as ends in themselves rather than treating them merely as means.

These principles were selected because they represent distinct ethical approaches and can produce divergent evaluations of the same dilemma.