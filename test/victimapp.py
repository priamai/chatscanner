import gradio as gr
from threading import Thread
from typing import Optional
from transformers import TextIteratorStreamer
from langchain import PromptTemplate
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain import LLMChain
from langchain.llms.base import LLM

def initialize_model_and_tokenizer(model_name="bigscience/bloom-1b7"):
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

template = """Question: {question}
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])

class CustomLLM(LLM):
    streamer: Optional[TextIteratorStreamer] = None

    def _call(self, prompt, stop=None, run_manager=None) -> str:
        self.streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, Timeout=5)
        inputs = tokenizer(prompt, return_tensors="pt")
        kwargs = dict(input_ids=inputs["input_ids"], streamer=self.streamer, max_new_tokens=20)
        thread = Thread(target=model.generate, kwargs=kwargs)
        thread.start()
        return ""

    @property
    def _llm_type(self) -> str:
        return "custom"

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")
    llm = CustomLLM()
    model, tokenizer = initialize_model_and_tokenizer()

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        print("Question: ", history[-1][0])
        llm_chain.run(question=history[-1][0])
        history[-1][1] = ""
        for character in llm.streamer:
            print(character)
            history[-1][1] += character
            yield history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch()