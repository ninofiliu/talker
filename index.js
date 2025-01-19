let idle = true;
const button = document.querySelector("button");
const audio = document.querySelector("audio");
const stream = await navigator.mediaDevices.getUserMedia({ audio: "true" });
const recorder = new MediaRecorder(stream);

let chunks = [];
recorder.addEventListener("stop", async () => {
  const blob = new Blob(chunks, { type: "audio/wav" });
  const resp = await fetch("/upload", {
    method: "POST",
    body: blob,
  });
  const text = await resp.text();
  console.log(text);
  const utterance = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utterance);
});

button.addEventListener("click", async () => {
  if (idle) {
    button.innerHTML = "stop";
    idle = false;
    chunks = [];
    recorder.start();
    recorder.addEventListener("dataavailable", (evt) => {
      chunks.push(evt.data);
    });
  } else {
    button.innerHTML = "record";
    idle = true;
    recorder.stop();
  }
});
