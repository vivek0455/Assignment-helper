import gradio as gr

from untils import generate_response, set_user_query,clear_conversations,regenerate_response


with gr.Blocks(theme=gr.themes.Default(neutral_hue="slate")) as demo:
    gr.Markdown("""<h1><center>Welcome</center></h1>""")

    with gr.Row():
        participant_mail = gr.components.Textbox(
        label='Enter Your Mail Id')
        participant_id = gr.components.Textbox(
        label='Enter Your Unique Participant-Id',type='password')
  
    chatbot = gr.components.Chatbot(label='PM Assistant',container=True,show_copy_button=True)
    msg = gr.components.Text(label='Input Your Query and then Hit Enter')
    with gr.Row():
        regenerate = gr.components.Button(value='Regenerate Response', variant='secondary',size="lg")
        clear = gr.components.Button(value='Clear Conversation', variant='stop')
    


    msg.submit(
        fn=set_user_query,
        inputs=[msg, chatbot],
        outputs=[msg, chatbot]
    ).then(
        fn=generate_response,
        inputs=[msg, chatbot,participant_id, participant_mail],
        outputs=[chatbot]
    )

    clear.click(fn=clear_conversations, inputs=[participant_id, participant_mail], outputs=[msg, chatbot])
    regenerate.click(fn= regenerate_response, inputs=[chatbot,participant_id, participant_mail], outputs=[chatbot])

demo.queue(concurrency_count=3, api_open=False)

