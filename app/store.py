import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class RunStore:
    def __init__(self, root: Path = Path(".runs")):
        self.root = root
        self.root.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = self.root / timestamp
        self.latest_dir = self.root / "latest"

    def start(self) -> Path:
        self.run_dir.mkdir(parents=True, exist_ok=True)

        if self.latest_dir.exists() or self.latest_dir.is_symlink():
            if self.latest_dir.is_symlink():
                self.latest_dir.unlink()
            else:
                shutil.rmtree(self.latest_dir)

        shutil.copytree(self.run_dir, self.latest_dir)
        self.run_dir = self.latest_dir
        return self.run_dir

    def write_text(self, filename: str, content: str) -> None:
        path = self.run_dir / filename
        path.write_text(content, encoding="utf-8")

    def write_json(self, filename: str, data: Dict[str, Any]) -> None:
        path = self.run_dir / filename
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def append_trace(self, event: Dict[str, Any]) -> None:
        path = self.run_dir / "trace.jsonl"
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")