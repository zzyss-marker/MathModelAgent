import os
import datetime
import hashlib
import tomllib
from core.LLM import BaseModel


def create_task_id() -> str:
    """生成任务ID"""
    # 生成时间戳和随机hash
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    random_hash = hashlib.md5(str(datetime.datetime.now()).encode()).hexdigest()[:8]
    return f"{timestamp}-{random_hash}"


def create_work_directories(task_id: str):
    """
    summary

    Args:
        task_id : description

    Returns:
        base_dir : './project/wirk_dir'
        dirs : './project/work_dir/*'
    """
    work_dir_name = task_id

    # 设置主工作目录和子目录
    base_dir = os.path.join("project", "work_dir", work_dir_name)
    dirs = {
        "jupyter": os.path.join(base_dir, "jupyter"),
        "log": os.path.join(base_dir, "log"),
        "res": os.path.join(base_dir, "res"),
    }

    # 创建所需目录
    for dir_path in dirs.values():
        os.makedirs(dir_path, exist_ok=True)

    return base_dir, dirs


def load_toml(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_markdown(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_current_files(folder_path: str, type: str = "all") -> list[str]:
    files = os.listdir(folder_path)
    if type == "all":
        return files

    elif type == "md":
        return [file for file in files if file.endswith(".md")]
    elif type == "ipynb":
        return [file for file in files if file.endswith(".ipynb")]
    elif type == "xlsx":
        return [file for file in files if file.endswith(".xlsx")]
    elif type == "image":
        return [
            file for file in files if file.endswith(".png") or file.endswith(".jpg")
        ]


def simple_chat(model: BaseModel, history: list) -> str:
    """
    Description of the function.

    Args:
        model (BaseModel): 模型
        history (list): 构造好的历史记录（包含system_prompt,user_prompt）

    Returns:
        return_type: Description of the return value.
    """
    kwargs = {
        "model": model.model,
        "messages": history,
        "stream": False,
    }

    completion = model.client.chat.completions.create(**kwargs)

    return completion.choices[0].message.content
