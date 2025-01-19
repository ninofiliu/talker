# Talker

A super simple tool for a chatbot with voice control

## How it works

The whole code contains close to no logic in itself, rather it is mostly glue code between:

- [getUserMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia) and [MediaRecorder](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder) to record the user's audio
- [OpenAI's Whisper](https://openai.com/index/whisper/) to convert the user audio into a question text
- [Google's Gemma](https://ai.google.dev/gemma) as an LLM to compute a answer text
- [Huggingface's Transformers](https://pypi.org/project/huggingface/) python lib to wrap around the LLM, or any model you want to use (just replace the `checkpoint` string)
- [SpeechSynthesis](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis) to convert the answer text into audio

As of now it's way too basic to be practically used on a daily basis, but it serves as a POC for future applications (eg: LLM-powered local vocal chat in video games). It's also a surprisingly small repository: 85 lines for the python server, 58 lines for the web app

## Installation

Install torch with GPU support

```sh
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Install dependencies

```sh
pip install -r requirements.txt
```

Run the server

```sh
python server.py
```

Navigate to [localhost:8080](http://localhost:8080) when ready
