# 🧠 GitEcho

**GitEcho** is a command-line tool that uses AI to summarize Git diffs or commits into clear, human-readable explanations. Great for Pull Request descriptions, commit summaries, or changelogs.

## 🚀 Features

- 🔍 Summarizes code diffs using OpenAI or a local LLM (Ollama, LM Studio)
- 🧑‍💻 Plain-English output for PRs or documentation
- 🔐 Fully privacy-respecting with local inference mode

---

## 🔧 Installation

```bash
git clone https://github.com/yourname/gitecho.git
cd gitecho
pip install -r requirements.txt
```

---

## ⚙️ Usage

### 🔹 With OpenAI (default)

```bash
export OPENAI_API_KEY=your-api-key
python gitecho.py
```

### 🔹 With Local LLM (Ollama, LM Studio, etc.)

```bash
python gitecho.py --local --endpoint http://localhost:11434
```

---

## 🔐 Privacy Notice

> By default, GitEcho sends your Git diff to OpenAI's API.  
> To keep all processing local, use the `--local` flag with your preferred self-hosted model.

---

## 📄 Example Output

```text
====== AI Summary ======

Refactored login logic to use helper function `validate_user_input()`. Updated `home.html` with cleaner copy and improved accessibility attributes. Removed unused imports from `auth.py`.
```

---

## 📁 .env.example

```env
OPENAI_API_KEY=sk-xxxxx
```

---

## 📝 License

MIT License. See `LICENSE`.

---

## ❤️ Contributing

Pull requests welcome. Please open an issue for bugs or feature requests.
