# 🤖 Automated Robobo with LLM (GPT-4)

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?logo=openai&logoColor=white)](https://platform.openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Thesis](https://img.shields.io/badge/Thesis-MSc%20UDC-blue)](https://www.udc.es)

> **Master's thesis (Universidade da Coruña)** — vision-language control of a
> *Robobo* robot using **GPT-4**: the model interprets the robot's camera feed
> and decides the next action (move, turn, speak) in real time.

---

## 📚 Description

This project couples a **Robobo** mobile robot (real hardware or simulator)
with a **GPT-4** vision-language model. The robot captures its camera frame
and sensor data, the frame is base64-encoded and sent to the OpenAI API
together with a behavioural prompt, and the model's structured response is
dispatched to the robot's action API.

It supports two operating modes, selectable from `config.py`:

- `real` — connects to a physical Robobo over its TCP/IP interface.
- `simulation` — connects to the Robobo Simulator.

The repository includes:

- `main.py` — orchestration loop (capture → prompt → act).
- `api_openai.py` — OpenAI client + structured prompt assembly.
- `roboboactions.py` — typed action dispatcher for the robot.
- `template.py` / `template_old.py` — alternative prompt templates.
- `behaviour_mod/` — behavioural modules (prompt + post-processing) per task.
- `utils.py` — image I/O, base64 helpers, and simulator glue.
- `images/` — sample frames.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| LLM | OpenAI GPT-4 (vision) |
| Hardware | Robobo robot (real or simulated) |
| Robot control | [`robobo-python-video-stream`](https://github.com/mintforpeople/robobo-python-video-stream) |
| Config | `python-dotenv` (`.env` file) |
| Output | Structured JSON actions consumed by `roboboactions.py` |

---

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/fhvaldes/TFMproject.git
   cd TFMproject
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. For **real mode**, install the Robobo video-stream library following
   [mintforpeople/robobo-python-video-stream](https://github.com/mintforpeople/robobo-python-video-stream).

4. For **simulation mode**, start the Robobo Simulator and make sure its
   camera is open (see `img.png` for the expected layout).

5. Create a `.env` file in the project root:

   ```dotenv
   OPENAI_API_KEY=sk-...
   ROBOT_IP=192.168.1.135       # replace with the real robot's IP
   ```

---

## 🚀 Usage

Edit `config.py` to choose the operating mode:

```python
config = Config(mode="real")        # or "simulation"
```

Then run the main loop (make sure the simulator is open or the physical
robot is reachable):

```bash
python main.py
```

The script will:

1. Capture a frame from the robot's camera.
2. Send it to GPT-4 with the active behaviour prompt.
3. Apply the resulting JSON action via `roboboactions.py`.
4. Repeat.

---

## 🧪 Status

This repository is the **research artefact** of a completed MSc thesis and
is kept for reproducibility. Behaviour modules may be experimental; the
orchestration layer is stable.

---

## 🙏 Acknowledgements

- **Universidade da Coruña** — MSc programme.
- [`mintforpeople/robobo-python-video-stream`](https://github.com/mintforpeople/robobo-python-video-stream)
  for the Robobo Python interface.
- **OpenAI** for the GPT-4 multimodal API.

---

## 📄 License

Released under the [MIT License](LICENSE).
