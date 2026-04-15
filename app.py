import gradio as gr
import os
from sidekick import Sidekick


async def setup():
    sk = Sidekick()
    await sk.setup()
    return sk


async def process_message(sidekick, message, success_criteria, history):
    # Pass the instance to running superstep
    results = await sidekick.run_superstep(message, success_criteria, history)
    return results, sidekick


async def reset():
    new_sidekick = Sidekick()
    await new_sidekick.setup()
    return "", "", None, new_sidekick


def free_resources(sidekick):
    print("Cleaning up browser resources...")
    try:
        if sidekick:
            sidekick.cleanup()
    except Exception as e:
        print(f"Exception during cleanup: {e}")


# Custom CSS for the Professional Minimalist Theme
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

body, .gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #fdfdfd !important;
    color: #1f2937 !important;
}

.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* Typography */
h1 {
    font-weight: 700 !important;
    color: #111827 !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 0.2rem !important;
    font-size: 2.2rem !important;
}

h1 + p {
    color: #6b7280 !important;
    font-style: italic;
    font-size: 0.95rem !important;
    margin-bottom: 1.5rem !important;
}

h3 {
    font-weight: 600 !important;
    color: #374151 !important;
    font-size: 1.1rem !important;
    margin-bottom: 0.5rem !important;
}

/* Inputs */
input, textarea {
    background-color: #ffffff !important;
    border: 1px solid #d1d5db !important;
    border-radius: 6px !important;
    color: #1f2937 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    padding: 10px 12px !important;
}

input:focus, textarea:focus {
    border-color: #9ca3af !important;
    box-shadow: 0 0 0 1px #9ca3af !important;
    outline: none !important;
}

/* Chatbot Area */
.chatbot {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    font-size: 0.95rem !important;
}

.chatbot .message {
    border-radius: 6px !important;
    padding: 14px 18px !important;
    line-height: 1.6 !important;
    margin-bottom: 12px !important;
}

.chatbot .user-message {
    background-color: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    color: #1f2937 !important;
}

.chatbot .bot-message {
    background-color: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-left: 3px solid #111827 !important;
    color: #374151 !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
}

/* Buttons */
button.primary {
    background: #111827 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.2s ease !important;
    padding: 10px 20px !important;
}

button.primary:hover {
    background: #374151 !important;
    transform: translateY(-1px) !important;
}

button.stop {
    background: #ffffff !important;
    color: #374151 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    padding: 8px 16px !important;
}

button.stop:hover {
    background: #f3f4f6 !important;
    color: #111827 !important;
    border-color: #9ca3af !important;
}

/* General Layout Tweaks */
.gr-group {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 8px !important;
    padding: 18px !important;
}

.left-panel {
    margin-right: 15px !important;
}

/* Chatbot inner fixes for thread line and empty avatars */
.chatbot [class*="avatar"] { 
    display: none !important; 
    width: 0 !important;
}

/* Aggressively remove thread lines by making them transparent */
.chatbot * {
    border-left-color: transparent !important;
}

/* Restore the bubble borders properly */
.chatbot .user-message {
    background-color: #f9fafb !important;
    border: 1px solid #e5e7eb !important;
    color: #1f2937 !important;
}

.chatbot .bot-message {
    background-color: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-left-color: #111827 !important;
    border-left-width: 3px !important;
    color: #374151 !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
}

.chatbot [class*="message-wrap"] {
    margin-left: 0 !important;
    padding-left: 0 !important;
}

.reset-btn {
    min-width: 0 !important;
    padding: 6px 14px !important;
    margin-top: 15px !important;
}
"""

# Startup check for Hugging Face
if os.environ.get("SPACE_ID"):
    print("Detected Hugging Face environment. Ensuring Playwright is installed...")
    os.system("playwright install chromium")

with gr.Blocks(title="Sidekick AI", theme=gr.themes.Base(primary_hue="slate", neutral_hue="slate"), css=custom_css) as ui:
    with gr.Row(elem_id="header", equal_height=False):
        with gr.Column(scale=1):
            gr.Markdown("# ⚡ Sidekick AI Agent (Enterprise Edition)\n*Full Automation Agent for the Modern Enterprise.*")
        with gr.Column(scale=0):
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
            
            gr.HTML("<div style='padding: 15px; margin-top: 15px; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;'><p style='font-size: 0.88em; color: #6b7280; margin: 0; line-height: 1.5;'><i>Note: These are sample queries for the demo project. Feel free to replace them with your own tasks!</i></p></div>")

        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Logs & Output", height=650, type="messages", show_label=False)

    ui.load(setup, [], [sidekick], api_name=False)
    
    message.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick], api_name=False
    )
    success_criteria.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick], api_name=False
    )
    go_button.click(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick], api_name=False
    )
    reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick], api_name=False)


if __name__ == "__main__":
    ui.queue(default_concurrency_limit=2, max_size=10).launch(
        server_name="0.0.0.0",
        server_port=7860
    )
