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


# Custom CSS for the "Electric Blue" Premium Theme
custom_css = """
body, .gradio-container {
    background-color: #0A0A0B !important;
    color: #E0E0E0 !important;
}
.gradio-container {
    border: none !important;
}
button.primary {
    background: linear-gradient(90deg, #007BFF 0%, #00C2FF 100%) !important;
    border: none !important;
    box-shadow: 0 0 15px rgba(0, 123, 255, 0.4) !important;
}
button.primary:hover {
    box-shadow: 0 0 25px rgba(0, 194, 255, 0.6) !important;
    transform: translateY(-1px);
}
.chatbot .message {
    border-radius: 12px !important;
}
.chatbot .user-message {
    background-color: #1A1A1C !important;
}
.chatbot .bot-message {
    background-color: #121214 !important;
    border-left: 3px solid #00C2FF !important;
}
input, textarea {
    background-color: #1A1A1C !important;
    border: 1px solid #333 !important;
    color: white !important;
}
h2, .markdown-text {
    color: #00C2FF !important;
    text-shadow: 0 0 10px rgba(0, 194, 255, 0.3) !important;
}
"""

# Startup check for Hugging Face
if os.environ.get("SPACE_ID"):
    print("Detected Hugging Face environment. Ensuring Playwright is installed...")
    os.system("playwright install chromium")

with gr.Blocks(title="Sidekick AI", theme=gr.themes.Default(primary_hue="blue", neutral_hue="slate"), css=custom_css) as ui:
    gr.Markdown("## Sidekick AI Agent (Gemini 2026 Edition)")
    sidekick = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick conversation", height=450, type="messages")
    with gr.Group():
        with gr.Row():
            message = gr.Textbox(show_label=False, placeholder="What should I do for you?")
        with gr.Row():
            success_criteria = gr.Textbox(
                show_label=False, placeholder="Define your success criteria (e.g. 'Give me a 5-sentence summary')"
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
