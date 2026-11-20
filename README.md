# THUFIR - A VIrtual Ethics Advisor
**THUFIR** is a hybrid machine ethics system that helps users navigate moral dilemmas.

It integrates an LLM to converse with users and a mdodified version of the HERA Python library for moral reasoning.

THUFIR is currently not publicly available as a web-app, but can be run locally by cloning the repo and providing access to an LLM through API keys.


## Setup

The application requires GNU/Linux or Windows with WSL (Windows Subsystem for Linux). Python dependencies are managed using [uv](https://docs.astral.sh/uv/).

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ethico.git
   cd ethico
   ```

2. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
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
   python3 setup.py install
   cd ..
   deactivate
   ```

6. **Run the application:**
   ```bash
   uv run reflex run
   ```

   The application will typically be accessible at `http://localhost:3000`.
