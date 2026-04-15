import gradio as gr
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


with gr.Blocks(title="Sidekick", theme=gr.themes.Default(primary_hue="emerald")) as ui:
    gr.Markdown("## Sidekick AI Agent (Gemini 2026 Edition)")
    sidekick = gr.State(delete_callback=free_resources)

    with gr.Row():
        chatbot = gr.Chatbot(label="Sidekick conversation", height=450)
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

    ui.load(setup, [], [sidekick])
    
    message.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    success_criteria.submit(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    go_button.click(
        process_message, [sidekick, message, success_criteria, chatbot], [chatbot, sidekick]
    )
    reset_button.click(reset, [], [message, success_criteria, chatbot, sidekick])


if __name__ == "__main__":
    ui.launch(inbrowser=True)
