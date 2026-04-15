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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

body, .gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #fdfdfd !important;
    color: #1a1a1a !important;
}

.gradio-container {
    max-width: 1000px !important;
    margin: 0 auto !important;
}

/* Typography */
h2 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    color: #111111 !important;
    letter-spacing: -0.02em !important;
    border-bottom: 1px solid #eaeaea;
    padding-bottom: 0.5rem;
    margin-bottom: 1.5rem !important;
    text-shadow: none !important;
}

/* Inputs */
input, textarea {
    background-color: #ffffff !important;
    border: 1px solid #d4d4d4 !important;
    border-radius: 6px !important;
    color: #111111 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
    padding: 10px 12px !important;
}

input:focus, textarea:focus {
    border-color: #4a4a4a !important;
    box-shadow: 0 0 0 1px #4a4a4a !important;
    outline: none !important;
}

/* Chatbot Area */
.chatbot {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
}

.chatbot .message {
    border-radius: 6px !important;
    padding: 14px 18px !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    margin-bottom: 12px !important;
}

.chatbot .user-message {
    background-color: #f7f7f7 !important;
    border: 1px solid #e0e0e0 !important;
    color: #111111 !important;
}

.chatbot .bot-message {
    background-color: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-left: 3px solid #111111 !important;
    color: #222222 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02) !important;
}

/* Buttons */
button.primary {
    background: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #111111 !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08) !important;
    transition: all 0.2s ease !important;
    padding: 12px 24px !important;
}

button.primary:hover {
    background: #2a2a2a !important;
    border-color: #2a2a2a !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.12) !important;
    transform: translateY(-1px) !important;
}

button.stop {
    background: #ffffff !important;
    color: #444444 !important;
    border: 1px solid #cccccc !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

button.stop:hover {
    background: #f0f0f0 !important;
    color: #111111 !important;
    border-color: #aaaaaa !important;
}
"""

# Startup check for Hugging Face
if os.environ.get("SPACE_ID"):
    print("Detected Hugging Face environment. Ensuring Playwright is installed...")
    os.system("playwright install chromium")

with gr.Blocks(title="Sidekick AI", theme=gr.themes.Base(primary_hue="zinc", neutral_hue="zinc"), css=custom_css) as ui:
    gr.Markdown("## Sidekick AI Agent (Enterprise Edition)")
    sidekick = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick conversation", height=450, type="messages")
    with gr.Group():
        gr.Markdown("<p style='font-size: 0.9em; color: #666; margin-bottom: 5px; padding-left: 5px;'><i>These are sample queries for the demo project. Feel free to replace them with your own tasks!</i></p>")
        with gr.Row():
            message = gr.Textbox(
                show_label=False, 
                placeholder="What should I do for you?",
                value="Find me the top 3 best-rated gyms in Vantaa, Finland."
            )
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, 
                placeholder="Define your success criteria (e.g. 'Give me a 5-sentence summary')",
                value="Provide a list of 3 gyms with their address and average rating."
            )
    with gr.Row():
        reset_button = gr.Button("Reset Session", variant="stop")
        go_button = gr.Button("Execute Task", variant="primary")

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
