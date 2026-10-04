from __future__ import annotations
from crewai import Agent, Crew, Process, Task
from core.llm import build_llm

ROLES = [
    ("Technical SEO Architect", "Find technical SEO, crawlability, indexation, metadata, schema and mobile issues.", "Be precise and prioritize high-impact fixes."),
    ("Keyword & Content Strategist", "Turn the page topic and audit evidence into search intent, keyword clusters, headings and content opportunities.", "Never invent business facts. Clearly label assumptions."),
    ("On-Page SEO Copywriter", "Produce premium title, meta description, H1/H2 structure, CTA copy and content improvements.", "Write concise, human-first copy that matches search intent."),
    ("UX & Premium Web Designer", "Improve hierarchy, readability, conversion UX, accessibility and visual premium quality.", "Recommend implementation-ready design tokens and component changes."),
    ("Authority & Growth Strategist", "Recommend ethical internal-linking, content clusters, digital PR and authority-building actions.", "Do not recommend spam, link schemes, cloaking or deceptive tactics."),
    ("SEO QA & Release Reviewer", "Audit the proposed plan for factual safety, technical completeness, conflicts and measurable acceptance criteria.", "Reject unsupported claims and produce a clean release checklist."),
]

def build_crew(api_key: str, model: str):
    llm = build_llm(api_key, model=model)
    agents = [Agent(role=r, goal=g, backstory=b, llm=llm, verbose=False, allow_delegation=False) for r,g,b in ROLES]
    return agents

def run_seo_crew(api_key: str, model: str, audit_json: str, business_context: str, target_keywords: str) -> dict[str, str]:
    agents = build_crew(api_key, model)
    context = f"AUDIT JSON:\n{audit_json}\n\nBUSINESS CONTEXT:\n{business_context}\n\nTARGET KEYWORDS:\n{target_keywords}"
    tasks = []
    outputs = {}
    prompts = [
        "Create a prioritized technical SEO remediation list with severity, evidence and acceptance criteria.",
        "Create primary/secondary keyword intent clusters and a content architecture based only on supplied evidence.",
        "Write optimized title, meta description, H1, H2 outline, CTA microcopy and FAQ ideas. Keep claims generic unless supplied.",
        "Create a premium UX/UI upgrade specification: layout hierarchy, typography scale, spacing, components, accessibility and responsive behavior.",
        "Create a 30/60/90-day ethical growth plan covering internal links, content clusters, PR/outreach and measurement.",
        "Review all preceding recommendations and return a final implementation checklist, risks, dependencies and KPIs."
    ]
    previous = ""
    for idx, (agent, prompt) in enumerate(zip(agents, prompts)):
        task = Task(
            description=f"{context}\n\nPREVIOUS OUTPUTS:\n{previous}\n\nYOUR ASSIGNMENT:\n{prompt}\nReturn structured Markdown with headings and bullets.",
            expected_output="Actionable, evidence-aware Markdown.", agent=agent)
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
        result = crew.kickoff()
        text = str(result)
        key = ["technical","keywords","copy","ux","growth","qa"][idx]
        outputs[key] = text
        previous += f"\n\n--- {key.upper()} ---\n{text[:7000]}"
    return outputs
