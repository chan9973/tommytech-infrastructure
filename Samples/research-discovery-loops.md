# 🧪 Research Discovery - `/loop` Use Cases

## Why Use `/loop` for Research?

Research is dynamic! New papers are published daily across arXiv, Nature, Science, and other venues. Instead of manually checking repeatedly, set up automatic discovery loops that:

- ✅ Catch breakthroughs before everyone else
- ✅ Stay updated on your field's hottest topics
- ✅ Never miss a conference deadline or paper drop
- ✅ Cross-reference multiple sources automatically

---

## Sample 1: Daily AI/ML Paper Discovery 📰

What we just created above monitors:
- **Sources:** arXiv (cs.LG, cs.AI, cs.CL categories)
- **Frequency:** Every day at the same time
- **Output:** Curated summary of top new papers with links

```python
schedule='every 1d'  # or '6h', 'every 2h', etc.
prompt='Search arXiv for new papers in Machine Learning and AI categories...'
```

---

## Sample 2: Competitor Research Monitor 🏆

Track what major companies or competitors are publishing/doing.

```python
cronjob(
    action='create',
    schedule='every 2h',
    prompt='Search for publications, patents, and blog posts from OpenAI, Anthropic, Google DeepMind, Meta AI, and xAI in the last 6 hours. Highlight any breakthrough announcements, new model releases, or research paper drops.'
)
```

**Use cases:**
- Know when a competitor releases a new model
- Track patent filings in your field
- Monitor industry news from key players

---

## Sample 3: Cross-Source Research Aggregator 📊

Combine multiple research databases.

```python
cronjob(
    action='create',
    schedule='daily',
    prompt='Check three sources for new content in [YOUR FIELD]:
      1. arXiv preprints (cs.* categories)
      2. Google Scholar recent citations
      3. Nature/Science news
     
 Cross-reference findings: if a paper appears on multiple platforms, verify significance and summarize in a unified report.'
)
```

---

## Sample 4: Conference & Journal Alerts 🔔

Monitor when important conferences or journals are accepting submissions.

```python
cronjob(
    action='create',
    schedule='every 12h',
    prompt='Check for CFP (Call for Papers) announcements in AI/ML conferences: NeurIPS, ICLR, ICML, CVPR, ACL, EMNLP. If any are open and accepting submissions, list deadline, submission link, and key tracks with their topics.'
)
```

---

## Sample 5: Grant/Funding Opportunity Monitor 💰

Never miss a funding deadline!

```python
cronjob(
    action='create',
    schedule='every 24h',
    prompt='Monitor NSF, NIH, EU Horizon, and other major grant databases for new funding calls. Prioritize those matching [your research area]. Note application deadlines (30/60/90 days out) and page counts.'
)
```

---

## Sample 6: Tutorial & Course Discovery 🎓

Find the latest tutorials, workshops, and courses in your field.

```python
cronjob(
    action='create',
    schedule='every day',
    prompt='Search for new tutorials, workshops, MOOCs, and video courses in [your topic] on platforms like Coursera, edX, fast.ai, Hugging Face Courses, and PyTorch Ecosystem. Filter for free or highly-rated options only.'
)
```

---

## Sample 7: Newsletter & Briefing Monitor 📧

Track industry newsletters that send daily/weekly updates.

```python
cronjob(
    action='create',
    schedule='daily',
    prompt='Check AI newsletters: The Batch (Benjal), TWIML, Alpha Signal, Unsupervised, Import AI. Summarize the top stories from each and check if any have subscriber polls or community discussions.'
)
```

---

## Sample 8: Twitter/X & Social Media Research Monitor 🐦

Catch hot topics and researcher discussions before papers are published.

```python
cronjob(
    action='create',
    schedule='hourly',
    prompt='Search Twitter/X for mentions of researchers in [your field] (e.g., Yoshua Bengio, Yann LeCun, Sam Altman). If anyone posts about a 'new result', 'breakthrough', or 'first time', flag it and link to their thread.'
)
```

---

## Sample 9: Dataset Discovery 🔬

Find new datasets released for research.

```python
cronjob(
    action='create',
    schedule='daily',
    prompt='Search datasets like Hugging Face Datasets, Kaggle Competitions, and GitHub repositories for newly published datasets in [your field]. Note their size, license type, and key features.'
)
```

---

## Sample 10: Software & Tool Updates 🛠️

Monitor when new research tools are released.

```python
cronjob(
    action='create',
    schedule='every day',
    prompt='Check Hugging Face, GitHub Trending, and arXiv for new open-source projects in [your field] that gained >50 stars in the last 24 hours. Provide links and brief feature summaries.'
)
```

---

## Creating Your Research Discovery Loop

**Step 1:** Define your research focus

```python
# Example: NLP + Machine Learning
research_focus='NLP, machine learning, large language models'
```

**Step 2:** Choose sources to monitor

```python
sources = [
    'arXiv',
    'Twitter X', 
    'Google Scholar',
    'Nature AI',
    'industry newsletters'
]
```

**Step 3:** Set appropriate frequency

- **Breaking news:** every 1-2 hours
- **Daily updates:** once per day
- **Weekly digest:** 2-3 times/week

**Step 4:** Write your prompt

```python
cronjob(
    action='create',
    schedule='every day',
    prompt=f'Search for new research in {research_focus}. Check sources: {sources}. 
            Summarize top finds and provide links to full papers/reports.'
)
```

---

## Pro Tips for Research Loops

1. **Cross-reference automatically** - Use one loop to verify findings across multiple sources
2. **Set smart alerts** - Don't alert on everything; set thresholds (e.g., only cite if >50 citations in 24h)
3. **Archive results** - Save outputs to an Obsidian note or research journal
4. **Use wikilinks** - Link to [[Obsidian notes]] you create from the discovery findings
5. **Tag by relevance** - Add tags like #breakthrough, #review-worthy, #read-later

---

## Example: Obsidian Integration Workflow

```python
cronjob(
    action='create',
    schedule='daily',
    prompt='Scan arXiv for new papers in cs.LG. For each interesting paper:
      1. Extract metadata (title, authors, abstract)
      2. Note key contributions
      3. Link to our [[ML-Research]] note in Obsidian
     
      Save output as E:/tommy vault/tommy vault/Read & Write/research/new-discoveries-{{date}}.md'
)
```

This creates a persistent research discovery stream directly into your knowledge base! 📚✨

---

## Want to See It Run?

**Try this now:**
1. I'll run the arXiv discovery loop we created
2. You'll see it automatically scan daily
3. Each result gets saved to your local workspace

**Need a custom research monitor?** Tell me:
- Your field/topic of interest
- Which sources matter most to you
- How often you need updates

I can also help you design **personalized research discovery pipelines**! 🔬🚀
