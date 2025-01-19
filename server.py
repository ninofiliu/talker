from http.server import BaseHTTPRequestHandler, HTTPServer
import whisper  # type: ignore
from transformers import pipeline


print("loading speech to text...")
stt = whisper.load_model("turbo")

print("loading llm...")
checkpoint = "google/gemma-2b-it"
pipe = pipeline("text-generation", checkpoint)
messages = []


def serve_file(handler, filename, content_type):
    """Serve a file with the given content type."""
    try:
        with open(filename, "rb") as file:
            handler.send_response(200)
            handler.send_header("Content-type", content_type)
            handler.end_headers()
            handler.wfile.write(file.read())
    except FileNotFoundError:
        handler.send_error(404, "File Not Found")


def s2s(handler):
    """Save an uploaded file from a raw POST request."""
    global is_first_msg
    content_length = int(handler.headers["Content-Length"])
    file_data = handler.rfile.read(content_length)

    print("uploading file...")
    filename = "recording.opus"
    with open(filename, "wb") as f:
        f.write(file_data)

    print("speech to text...")
    user_text = stt.transcribe("recording.opus")["text"]
    print(f"speech to text done: ${user_text}")

    print("llm...")
    messages.append({"role": "user", "content": user_text})
    answer_text = pipe(messages, max_new_tokens=128)[0]["generated_text"][-1]["content"]
    messages.append({"role": "assistant", "content": answer_text})
    print(messages)

    handler.send_response(200)
    handler.end_headers()
    handler.wfile.write(f"{answer_text}".encode("utf-8"))


def handle_request(handler):
    """Handle incoming HTTP requests."""
    if handler.path == "/":
        serve_file(handler, "index.html", "text/html")
    elif handler.path == "/index.js":
        serve_file(handler, "index.js", "application/javascript")
    elif handler.path.startswith("/answer.wav"):
        serve_file(handler, "answer.wav", "audio/wav")
    elif handler.path == "/upload" and handler.command == "POST":
        s2s(handler)
    else:
        handler.send_error(404, "Not Found")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        handle_request(self)

    def do_POST(self):
        handle_request(self)


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    """Start the HTTP server."""
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
