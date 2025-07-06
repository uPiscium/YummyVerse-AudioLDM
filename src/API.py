from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
import uuid
import os
import time
import asyncio
from typing import Dict
from audioLDM import AudioLDM2Controller

app = FastAPI()
OUTPUT_DIR = "./outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

model = AudioLDM2Controller()
tasks: Dict[str, Dict] = {}
EXPIRE_SECONDS = 3600


def generate(prompt: str, length_s: float, output_path: str):
    audio_data = model.generate_audio(
        prompt=prompt,
        length_s=length_s,
    )
    model.save_audio(audio_data, output_path)


def background_generate(task_id: str, prompt: str, length_s: float):
    try:
        tasks[task_id]["status"] = "processing"
        out_path = os.path.join(OUTPUT_DIR, f"{task_id}.wav")
        generate(prompt, length_s, out_path)
        tasks[task_id]["status"] = "done"
        tasks[task_id]["result"] = out_path
        tasks[task_id]["timestamp"] = time.time()
    except Exception as e:
        tasks[task_id]["status"] = "error"
        tasks[task_id]["error"] = str(e)


async def cleanup_expired_files():
    while True:
        now = time.time()
        expired = [
            tid
            for tid, t in tasks.items()
            if "timestamp" in t and now - t["timestamp"] > EXPIRE_SECONDS
        ]
        for tid in expired:
            result_path = tasks[tid].get("result")
            if result_path and os.path.exists(result_path):
                try:
                    os.remove(result_path)
                except Exception:
                    pass
            del tasks[tid]
        await asyncio.sleep(300)  # 5分ごとに確認


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_expired_files())


@app.post("/generate/")
async def generate_audio(
    prompt: str = Form(...),
    length_s: float = Form(10.0),
    background_tasks: BackgroundTasks = None,
):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "pending", "timestamp": time.time()}
    background_tasks.add_task(background_generate, task_id, prompt, length_s)
    return {"task_id": task_id}


@app.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in tasks:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return tasks[task_id]


@app.get("/download/{task_id}")
async def download_result(task_id: str):
    task = tasks.get(task_id)
    if not task or task.get("status") != "done":
        return JSONResponse(status_code=404, content={"error": "Result not ready"})
    return FileResponse(
        task["result"],
        media_type="audio/wav",
        filename=os.path.basename(task["result"]),
    )


@app.get("/queue")
async def queue_status():
    return {
        "total": len(tasks),
        "pending": [tid for tid, t in tasks.items() if t["status"] == "pending"],
        "processing": [tid for tid, t in tasks.items() if t["status"] == "processing"],
        "done": [tid for tid, t in tasks.items() if t["status"] == "done"],
        "error": [tid for tid, t in tasks.items() if t["status"] == "error"],
    }
