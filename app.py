import gradio as gr
import os
from sidekick import Sidekick
from session_manager import cleanup_all_stale_sessions, list_session_files, cleanup_session_dir

# Purge any leftover temporary session files on server start
cleanup_all_stale_sessions()


async def setup() -> Sidekick:
    """Initialize a new Sidekick agent session with browser and tool setup."""
    sk = Sidekick()
    await sk.setup()
    return sk


async def process_message(sidekick: Sidekick, message: str, success_criteria: str, history: str):
    """Execute a superstep against the Sidekick agent, update logs, and list generated downloadable files."""
    if not sidekick:
        sidekick = await setup()
    results = await sidekick.run_superstep(message, success_criteria, history)
    files = list_session_files(sidekick.sidekick_id)
    return results, files, sidekick


async def reset(sidekick: Sidekick = None):
    """Reset the session with a fresh Sidekick agent instance and purge previous session artifacts."""
    if sidekick:
        cleanup_session_dir(sidekick.sidekick_id)
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", "", [], new_sidekick


def free_resources(sidekick: Sidekick) -> None:
    """Gracefully free browser and background resources when the session is discarded."""
    if sidekick:
        print("Cleaning up agent resources...")
        try:
            sidekick.cleanup()
        except Exception as e:
            print(f"Exception during cleanup: {e}")




# Custom CSS for the Professional Minimalist Theme
custom_css = """
:root, .dark {
    --background-fill-primary: #ffffff !important;
    --background-fill-secondary: #f9fafb !important;
    --block-background-fill: #ffffff !important;
    --block-label-text-color: #111827 !important;
    --input-background-fill: #ffffff !important;
    --input-placeholder-color: #9ca3af !important;
    --body-text-color: #1f2937 !important;
    --border-color-primary: #e5e7eb !important;
    --input-border-color: #d1d5db !important;
}

body, .gradio-container, .dark body, .dark .gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #fdfdfd !important;
    color: #1f2937 !important;
}

.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* Header */
h1 {
    font-weight: 700 !important;
    color: #111827 !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0.2rem !important;
    font-size: 2.2rem !important;
}

#header p, #header em {
    color: #4b5563 !important;
    font-style: normal !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    margin-top: 4px !important;
}

/* Hide Gradio default footer (API links, branding) */
footer {
    display: none !important;
}

/* Custom Log Window Styling - THE PAKKOKEINO */
#log-window {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    height: 650px !important;
    overflow-y: auto !important;
    padding: 0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}

.log-entry {
    padding: 20px 25px;
    border-bottom: 1px solid #f3f4f6;
    animation: fadeIn 0.3s ease-out;
}

.log-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
}

.log-time {
    color: #6b7280;
}

.log-role {
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 2px 8px;
    border-radius: 4px;
}

.role-user { color: #374151; background: #f3f4f6; }
.role-agent { color: #111827; background: #e5e7eb; border-left: 3px solid #111827; }
.role-eval { color: #047857; background: #ecfdf5; font-weight: 700; }

.log-content {
    font-size: 0.95rem;
    line-height: 1.6;
    color: #1f2937;
    white-space: pre-wrap;
}

.feedback-box {
    font-style: italic;
    color: #065f46;
    border-left: 3px solid #10b981;
    padding-left: 15px;
    margin-top: 10px;
    background: #f0fdf4;
    padding: 10px 15px;
    border-radius: 0 6px 6px 0;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Inputs & Buttons */
.left-panel {
    margin-right: 15px !important;
}

.left-panel .gr-group,
.left-panel .block,
.left-panel div[data-testid="textbox"],
.left-panel .gr-form,
.left-panel .gr-box {
    background: #ffffff !important;
    background-color: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
}

label, label span, .block-label {
    color: #111827 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    background: transparent !important;
}

textarea, input, .gr-input, .gr-textbox {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 6px !important;
    font-size: 0.92rem !important;
    line-height: 1.5 !important;
}

textarea:focus, input:focus {
    border-color: #111827 !important;
    box-shadow: 0 0 0 1px #111827 !important;
}

.gr-group {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    padding: 18px !important;
}

button.primary {
    background: #111827 !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
}

button.primary:hover {
    background: #374151 !important;
    transform: translateY(-1px) !important;
}

.reset-btn {
    min-width: 140px !important;
    background: #f9fafb !important;
    color: #374151 !important;
    border: 1px solid #d1d5db !important;
    margin-top: 15px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

.reset-btn:hover {
    background: #e5e7eb !important;
    color: #111827 !important;
    border-color: #9ca3af !important;
}

/* Capabilities Section */
.skills-container {
    display: grid;
    grid-template-columns: 1fr;
    gap: 12px;
    margin-top: 20px;
}

.skill-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 12px 15px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    transition: all 0.2s ease;
}

.skill-card:hover {
    border-color: #111827;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}

.skill-icon {
    font-size: 1.2rem;
    background: #f3f4f6;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    flex-shrink: 0;
}

.skill-info h4 {
    margin: 0 !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #111827 !important;
}

.skill-info p {
    margin: 2px 0 0 0 !important;
    font-size: 0.82rem !important;
    color: #4b5563 !important;
    line-height: 1.4 !important;
}

.preset-row {
    display: flex !important;
    gap: 6px !important;
    margin-bottom: 12px !important;
    flex-wrap: wrap !important;
}

.preset-btn {
    background: #f9fafb !important;
    color: #374151 !important;
    border: 1px solid #d1d5db !important;
    font-size: 0.76rem !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    padding: 3px 8px !important;
    transition: all 0.15s ease !important;
}

.preset-btn:hover {
    background: #e5e7eb !important;
    color: #111827 !important;
    border-color: #9ca3af !important;
}

#download-center,
#download-center .file-preview-holder,
#download-center .file-item,
#download-center .file-parts,
#download-center .file,
#download-center table,
#download-center tbody,
#download-center tr,
#download-center td {
    background: #ffffff !important;
    background-color: #ffffff !important;
    color: #111827 !important;
    border-color: #e5e7eb !important;
}

#download-center .file-name,
#download-center .file-size,
#download-center a,
#download-center span,
#download-center p {
    color: #111827 !important;
    font-weight: 500 !important;
}

#download-center .download-button,
#download-center button,
#download-center svg {
    color: #111827 !important;
    fill: #111827 !important;
}

.section-title {
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #111827 !important;
    margin-bottom: 6px !important;
}

.tip-box {
    padding: 14px 16px !important;
    margin-top: 15px !important;
    background: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
}

.tip-box p {
    font-size: 0.85rem !important;
    color: #374151 !important;
    margin: 0 !important;
    line-height: 1.5 !important;
}
"""

# Startup check for Hugging Face
if os.environ.get("SPACE_ID"):
    print("Detected Hugging Face environment. Ensuring Playwright is installed...")
    os.system("playwright install chromium")

head_html = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
    /* Ensure no unwanted artifacts */
    #log-window { scroll-behavior: smooth; }
</style>
"""

def load_preset_1():
    return (
        "Conduct a comprehensive market and architecture analysis of the top 3 Enterprise AI Agent frameworks (LangGraph, AutoGen, CrewAI). Compare their orchestration architectures, scalability, and security features. Generate a 16:9 PowerPoint presentation deck (.pptx), an Executive PDF brief, and an Excel comparison matrix.",
        "Generate an Executive PowerPoint presentation 'ai_agent_presentation.pptx', a styled Executive PDF 'ai_agent_executive_brief.pdf', and an Excel sheet 'ai_agent_matrix.xlsx' with strategic recommendations."
    )

def load_preset_2():
    return (
        "Perform an executive due diligence investigation on Microsoft's and Alphabet's latest quarterly AI revenue, Capex investments, and enterprise AI product roadmap. Synthesize key business risks and growth drivers into an Executive PowerPoint deck and PDF brief.",
        "Provide a clear comparison, key risk factors, and generate an executive PowerPoint presentation 'due_diligence_deck.pptx' and an executive PDF brief 'due_diligence_brief.pdf' summarizing strategic findings."
    )

def load_preset_3():
    return (
        "Analyze and benchmark Postgres with pgvector vs dedicated vector databases (Pinecone, Qdrant, Milvus) for enterprise RAG applications. Compare query latency, cost at scale, and operational complexity. Generate a PowerPoint briefing deck and an Excel workbook with the evaluation scores.",
        "Deliver a structured feature comparison, cost breakdown, and generate a PowerPoint presentation 'vector_db_benchmark.pptx' and an Excel workbook 'vector_db_benchmark.xlsx' with the evaluation scores."
    )

with gr.Blocks(title="Sidekick AI", theme=gr.themes.Base(primary_hue="slate", neutral_hue="slate"), css=custom_css, head=head_html) as ui:
    with gr.Row(elem_id="header", equal_height=False):
        with gr.Column(scale=4):
            gr.Markdown("# ⚡ Sidekick AI Agent (Enterprise Edition)\n*Full Automation Agent for the Modern Enterprise.*")
        with gr.Column(scale=1, min_width=150):
            reset_button = gr.Button("Reset session", variant="stop", elem_classes="reset-btn")

    sidekick = gr.State(delete_callback=free_resources)

    with gr.Row():
        with gr.Column(scale=1, min_width=320, elem_classes="left-panel"):
            with gr.Group():
                gr.Markdown("<div style='font-size: 0.8rem; font-weight: 600; color: #4b5563; margin-bottom: 6px;'>⚡ Executive Quick-Presets:</div>")
                with gr.Row(elem_classes="preset-row"):
                    preset_btn_1 = gr.Button("📊 Market & Pricing Matrix", size="sm", elem_classes="preset-btn")
                    preset_btn_2 = gr.Button("🏢 Company Due Diligence", size="sm", elem_classes="preset-btn")
                    preset_btn_3 = gr.Button("⚖️ Tech Stack Benchmark", size="sm", elem_classes="preset-btn")

                message = gr.Textbox(
                    label="Requirements",
                    lines=5,
                    placeholder="What should I do for you?",
                    value="Conduct a competitive market and architecture analysis of the top 3 Enterprise AI Agent frameworks (LangGraph, AutoGen, CrewAI). Compare their orchestration models, production scalability, and security posture. Generate a 16:9 PowerPoint deck and an Executive PDF brief."
                )
                success_criteria = gr.Textbox(
                    label="Success Criteria",
                    lines=3,
                    placeholder="Define your success criteria",
                    value="Generate a 16:9 PowerPoint presentation 'ai_agent_presentation.pptx' and an Executive PDF 'ai_agent_executive_brief.pdf' with executive comparison cards, trade-offs, and an actionable strategic recommendation."
                )
                go_button = gr.Button("Execute Task", variant="primary")
            
            gr.HTML("""
            <div class="skills-container">
                <div class="section-title">Agent Capabilities</div>
                <div class="skill-card">
                    <div class="skill-icon">🌐</div>
                    <div class="skill-info">
                        <h4>Autonomous Browsing</h4>
                        <p>Navigates and interacts with websites to extract real-time data.</p>
                    </div>
                </div>
                <div class="skill-card">
                    <div class="skill-icon">🔍</div>
                    <div class="skill-info">
                        <h4>Deep Search</h4>
                        <p>Performs multi-step web searches to find specific information.</p>
                    </div>
                </div>
                <div class="skill-card">
                    <div class="skill-icon">📊</div>
                    <div class="skill-info">
                        <h4>PowerPoint, PDF & Excel Export</h4>
                        <p>Generates styled 16:9 .pptx decks, Executive PDF briefs, and .xlsx workbooks.</p>
                    </div>
                </div>
                <div class="skill-card">
                    <div class="skill-icon">⚙️</div>
                    <div class="skill-info">
                        <h4>Code Execution</h4>
                        <p>Runs Python logic for complex calculations and data processing.</p>
                    </div>
                </div>
                <div class="skill-card">
                    <div class="skill-icon">📚</div>
                    <div class="skill-info">
                        <h4>Factual Research</h4>
                        <p>Accesses Wikipedia and structured sources for verified facts.</p>
                    </div>
                </div>
                <div class="skill-card">
                    <div class="skill-icon">🔔</div>
                    <div class="skill-info">
                        <h4>Smart Notifications</h4>
                        <p>Can alert you via push notifications when long-running tasks finish.</p>
                    </div>
                </div>
            </div>
            """)

            gr.HTML("<div class='tip-box'><p>🚀 <strong>Autonomous Enterprise Agent:</strong> Capable of end-to-end multi-step web browsing, verified research, Python computation, PowerPoint (.pptx) & PDF report generation, and structured strategic synthesis.</p></div>")

        with gr.Column(scale=3):
            # Custom HTML instead of Gr.Chatbot
            log_window = gr.HTML(label="Logs & Output", elem_id="log-window", value="")
            
            # Download Center for generated PowerPoint, Excel & PDF deliverables
            download_files = gr.File(
                label="📥 Session Deliverables (PowerPoint .pptx, PDF Briefs & Excel)",
                file_count="multiple",
                interactive=False,
                elem_id="download-center"
            )

    preset_btn_1.click(load_preset_1, [], [message, success_criteria])
    preset_btn_2.click(load_preset_2, [], [message, success_criteria])
    preset_btn_3.click(load_preset_3, [], [message, success_criteria])

    ui.load(setup, [], [sidekick], api_name=False)
    
    message.submit(
        process_message, [sidekick, message, success_criteria, log_window], [log_window, download_files, sidekick], api_name=False
    )
    success_criteria.submit(
        process_message, [sidekick, message, success_criteria, log_window], [log_window, download_files, sidekick], api_name=False
    )
    go_button.click(
        process_message, [sidekick, message, success_criteria, log_window], [log_window, download_files, sidekick], api_name=False
    )
    reset_button.click(reset, [sidekick], [message, success_criteria, log_window, download_files, sidekick], api_name=False)


if __name__ == "__main__":
    ui.queue(default_concurrency_limit=2, max_size=10).launch(
        show_error=True,
        show_api=False,
        share=False,
        ssr_mode=False
    )
