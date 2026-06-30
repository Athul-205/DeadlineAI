import os
from datetime import datetime
from zoneinfo import ZoneInfo

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_schedule(data):

    now = datetime.now(ZoneInfo("Asia/Kolkata"))

    current_date = now.strftime("%d-%m-%Y")
    current_time = now.strftime("%I:%M %p")

    prompt = f"""

You are DeadlineAI, an intelligent AI productivity planner.

Below is today's information.

{data}

Current Date: {current_date}
Current Time: {current_time} (Asia/Kolkata)

YOUR JOB

Create a complete schedule for today.

STRICT RULES

1. Never schedule anything before the Current Time provided above.
Use the Current Date and Current Time (Asia/Kolkata) exactly as provided.
Never assume a different date or timezone.

2. Never schedule study sessions during commitment times.

3. Include ALL commitments in the final timeline at their original times.

4. Add a 5–10 minute break after every 60–90 minutes of continuous work.

5. Prioritize tasks with the nearest deadlines.

6. A task MAY be split into multiple study sessions.

7. If a task does not fit into one free time slot, continue it in the next available free time slot.

8. Always prefer splitting a task across multiple available slots instead of postponing it.

9. Only postpone a task if the TOTAL remaining free time today is less than the total duration required.

10. Never postpone a task simply because one free slot is too small.

11. Use real clock times.

12. Keep the output short and professional.

OUTPUT FORMAT

🧠 AI Summary

🟢 Schedule Status: Feasible / Busy / Overloaded

⏱ Total Study Time: ___

🕒 Estimated Free Time: ___

☕ Breaks: ___

📅 Commitments: ___

-----------------------------------------

📅 Today's Timeline

2:00 PM - 3:00 PM
📘 DBMS Assignment

3:00 PM - 3:10 PM
☕ Break

3:10 PM - 4:00 PM
📘 Continue DBMS Assignment

4:00 PM - 5:00 PM
🏫 College (Commitment)

5:00 PM - 6:00 PM
📘 ML Revision

6:00 PM - 6:10 PM
☕ Break

6:30 PM - 7:30 PM
🏋 Gym (Commitment)

7:30 PM - 8:00 PM
📘 Complete Remaining Work

Only return the AI Summary and Today's Timeline.

Do NOT write paragraphs.

Do NOT explain every task.

Do NOT greet the user.

Keep the output clean and easy to read.
"""

    response = model.generate_content(prompt)

    return response.text