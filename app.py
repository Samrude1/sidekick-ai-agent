import gradio as gr
import os
from sidekick import Sidekick


async def setup():
    sk = Sidekick()
    await sk.setup()
    return sk


async def process_message(sidekick, message, success_criteria, history):
    # Pass the instance to running superstep
    # history is now a raw HTML string
    results = await sidekick.run_superstep(message, success_criteria, history)
    return results, sidekick


async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", "", new_sidekick


def free_resources(sidekick):
    print("Cleaning up browser resources...")
    try:
        if sidekick:
            sidekick.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


# Custom CSS for the Professional Minimalist Theme
custom_css = """
body, .gradio-container {
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
    color: #9ca3af;
}

.log-role {
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 2px 8px;
    border-radius: 4px;
}

.role-user { color: #4b5563; background: #f3f4f6; }
.role-agent { color: #111827; background: #e5e7eb; border-left: 3px solid #111827; }
.role-eval { color: #059669; background: #ecfdf5; }

.log-content {
    font-size: 0.95rem;
    line-height: 1.6;
    color: #374151;
    white-space: pre-wrap;
}

.feedback-box {
    font-style: italic;
    color: #065f46;
    border-left: 2px solid #10b981;
    padding-left: 15px;
    margin-top: 10px;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Inputs & Buttons */
.left-panel {
    margin-right: 15px !important;
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
    font-weight: 500 !important;
    padding: 10px 20px !important;
}

button.primary:hover {
    background: #374151 !important;
    transform: translateY(-1px) !important;
}

.reset-btn {
    min-width: 140px !important;
    background: transparent !important;
    border: 1px solid #d1d5db !important;
    margin-top: 25px !important;
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
    font-size: 0.8rem !important;
    color: #6b7280 !important;
    line-height: 1.4 !important;
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
                message = gr.Textbox(
                    label="Requirements",
                    lines=6,
                    placeholder="What should I do for you?",
                    value="Find me the top 3 best-rated gyms in Vantaa, Finland."
                )
                success_criteria = gr.Textbox(
                    label="Success Criteria",
                    lines=3,
                    placeholder="Define your success criteria",
                    value="Provide a list of 3 gyms with their address and average rating."
                )
                go_button = gr.Button("Execute Task", variant="primary")
            
            gr.HTML("""
            <div class="skills-container">
                <div style="margin-bottom: 5px;"><b style="font-size: 0.9rem; color: #374151;">Agent Capabilities</b></div>
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

            gr.HTML("<div style='padding: 15px; margin-top: 15px; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;'><p style='font-size: 0.88em; color: #6b7280; margin: 0; line-height: 1.5;'><i>Note: These are sample queries for the demo project. Feel free to replace them with your own tasks!</i></p></div>")

        with gr.Column(scale=3):
            # THE PAKKOKEINO: Custom HTML instead of Gr.Chatbot
            log_window = gr.HTML(label="Logs & Output", elem_id="log-window", value="")

    ui.load(setup, [], [sidekick], api_name=False)
    
    message.submit(
        process_message, [sidekick, message, success_criteria, log_window], [log_window, sidekick], api_name=False
    )
    success_criteria.submit(
        process_message, [sidekick, message, success_criteria, log_window], [log_window, sidekick], api_name=False
    )
    go_button.click(
        process_message, [sidekick, message, success_criteria, log_window], [log_window, sidekick], api_name=False
    )
    reset_button.click(reset, [], [message, success_criteria, log_window, sidekick], api_name=False)


if __name__ == "__main__":
    ui.queue(default_concurrency_limit=2, max_size=10).launch(
        show_error=True,
        share=False,
        ssr_mode=False
    )
