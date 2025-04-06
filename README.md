# 🧠 Sahaayak – Empowering Elderly Care with Multi-Agent AI System

Sahaayak is a modular, on-device multi-agent AI system built to assist elderly individuals living independently. By integrating health monitoring, safety alerts, routine reminders, and AI-driven social engagement, Sahaayak ensures real-time support while keeping caregivers, healthcare providers, and family members in the loop.

---

## 🧩 Problem Statement

As the global population ages, ensuring the well-being of elderly individuals living alone becomes a growing challenge. Our aim is to develop a multi-agent AI system that:

- Continuously monitors health vitals
- Detects falls and unusual behavior
- Sends timely reminders (e.g., medications, appointments)
- Enables real-time emergency alerts
- Provides social companionship through natural language conversations

---

## 💡 Proposed Solution

Sahaayak leverages a decentralized architecture using multiple intelligent agents. Each agent specializes in one core task—health tracking, safety, reminders, social interaction, or emergency response. Agents communicate via a central SQLite database and are orchestrated via a lightweight Python framework. On-device LLMs via **Ollama** ensure fast, private, and reliable performance without needing internet connectivity.

---

## 🛠️ Technologies Used

| Component              | Tools/Frameworks                                |
|------------------------|--------------------------------------------------|
| LLMs & Embeddings      | [Ollama](https://ollama.com/) (Mistral, LLaMA)  |
| Frontend Dashboard     | [Streamlit](https://streamlit.io/)              |
| Backend Storage        | SQLite                                           |
| ML Models              | Custom Python models for anomaly & fall detection |
| Voice Reminders        | `pyttsx3` (Text-to-Speech)                      |
| Scheduling             | `APScheduler` for reminder timing               |
| Notifications          | Twilio/Email API (for emergency alerts)         |
| Multi-Agent Architecture | Custom Python classes                          |

---

## 🤖 Agents Architecture

```
             +-----------------------+
             |   Coordination Agent  |
             +-----------------------+
                  ↑    ↑      ↑     ↑
                  ↓    ↓      ↓     ↓
   +----------------+ +----------------+ +----------------+ +----------------+
   | Health Agent   | | Safety Agent   | | Reminder Agent | | Social Agent   |
   |  → Vitals      | |  → Fall detect | |  → Schedule     | |  → Chat, mood  |
   +----------------+ +----------------+ +----------------+ +----------------+
                        ↓                       ↓
                   +------------------------------+
                   |  Emergency/Notification Agent|
                   +------------------------------+
```

---

## 🧾 Code Structure

```
sahaayak/
│
├── agents/
│   ├── health_agent.py
│   ├── safety_agent.py
│   ├── reminder_agent.py
│   ├── social_agent.py
│   └── notification_agent.py
│
├── streamlit_app/
│   └── main_dashboard.py
│
├── tools/
│   ├── ml_models.py
│   ├── db_utils.py
│   └── ollama_interface.py
│
├── data/
│   └── elderly.db
│
├── demo/
│   └── sahaayak_demo.mp4
└── README.md
```

---

## 🧪 Features

- 📊 **Health Monitoring** — Track vitals with alerts for anomalies
- 🛡️ **Safety Detection** — Detect inactivity/falls and notify contacts
- 🔔 **Daily Reminders** — Voice and visual reminders for meds/tasks
- 💬 **LLM-Powered Chat** — Local chat companion for emotional support
- 🚨 **Emergency Alerts** — Triggers notification to caregivers instantly
- 👨‍👩‍👧‍👦 **Caregiver Dashboard** — View and manage elderly health remotely

---

## 🚀 How to Run

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourname/sahaayak.git
   cd sahaayak
   ```

2. **Set up the virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Streamlit App**
   ```bash
   streamlit run streamlit_app/main_dashboard.py
   ```

5. **Run agents in background**
   ```bash
   python agents/health_agent.py
   python agents/safety_agent.py
   ...
   ```

---

## 📽️ Demo Video

> [🎥 Watch the Demo](./demo/sahaayak_demo.mp4) — See real-time detection, reminders, and chat interaction in action.

---

## 📌 Future Enhancements

- Multilingual support (Hindi, Bengali, etc.)
- Edge deployment with Raspberry Pi
- Real wearable integration (e.g., Apple Watch, Fitbit)
- Caregiver mobile app (Flutter)

---

## 🙌 Authors

- Your Name (@yourgithub)
- [Other Team Members]

---

## 📚 References

- Ollama: https://ollama.com/
- Streamlit: https://streamlit.io/
- SQLite: https://sqlite.org/
- APScheduler: https://apscheduler.readthedocs.io/
- pyttsx3: https://pyttsx3.readthedocs.io/

---

> 💙 *Sahaayak* means "Helper" – an AI friend for elderly care, built with empathy and innovation.
```
