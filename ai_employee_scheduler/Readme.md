# AI-Powered Employee Scheduling System

This project implements an AI-powered employee scheduling system featuring:
- **User Management:** Workers and supervisors register and are assigned to groups/jobs.
- **Constraint Collection:** Workers submit free-text constraints via a Telegram bot (or other channels), processed by the ChatGPT API.
- **Scheduling Algorithm:** Once all constraints are in, a scheduling algorithm generates an optimized schedule.
- **Supervisor Approval:** Supervisors review and approve schedules before final notification.
- **Notifications:** Email/SMS notifications are sent at various stages.
- **Deployment:** Fully containerized using Docker and Docker Compose, with PostgreSQL as the database.

## Setup

1. **Fill in the Missing Parts:**
   - Set your ChatGPT API key in `app/ai_processing.py` or as an environment variable (`OPENAI_API_KEY`).
   - Update SMTP credentials and Telegram Bot Token in `docker-compose.yml`.
   - If needed, modify any additional environment-specific configurations.

2. **Build and Run:**
   ```bash
   docker-compose up --build
