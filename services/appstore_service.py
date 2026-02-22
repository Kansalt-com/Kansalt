"""
App Store service for Business tab.

Responsibilities:
- create and manage SQLite schema for app store data
- manage app package ZIP storage/extraction
- admin credential initialization and verification
- metadata CRUD and download counters
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sqlite3
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import bcrypt


DEFAULT_CATEGORIES = ["Healthcare", "Finance", "HR", "Other"]
EXCLUDED_DIR_NAMES = {
    "venv",
    "node_modules",
    ".git",
    "__pycache__",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".pytest_cache",
}


class AppStoreService:
    """Service layer for Business App Store features."""

    def __init__(self, project_root: Optional[Path] = None) -> None:
        self.project_root = project_root or Path(__file__).resolve().parents[1]
        self.data_dir = self.project_root / "data"
        self.app_store_dir = self.project_root / "apps_store"
        self.zips_dir = self.app_store_dir / "zips"
        self.packages_dir = self.app_store_dir / "packages"
        self.assets_dir = self.app_store_dir / "assets"
        self.db_path = self.data_dir / "appstore.db"

        self._ensure_storage_dirs()
        self._init_db()
        self.seed_default_apps()

    def _ensure_storage_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.app_store_dir.mkdir(parents=True, exist_ok=True)
        self.zips_dir.mkdir(parents=True, exist_ok=True)
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        # Some environments (including restricted sandboxes) disallow deleting
        # rollback journal files. Use in-memory journaling for compatibility.
        conn.execute("PRAGMA journal_mode=MEMORY;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS apps (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    slug TEXT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    short_desc TEXT NOT NULL,
                    full_desc TEXT NOT NULL,
                    version TEXT NOT NULL,
                    tags_json TEXT NOT NULL,
                    os_support_json TEXT NOT NULL,
                    setup_instructions TEXT NOT NULL,
                    changelog TEXT NOT NULL,
                    zip_path TEXT NOT NULL,
                    package_path TEXT NOT NULL,
                    logo_path TEXT NULL,
                    screenshots_json TEXT NULL,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    downloads INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS admin_users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def seed_default_apps(self) -> None:
        """
        Seed metadata-only records for requested sample apps.
        Safe to call multiple times.
        """
        self._seed_if_missing(
            name="SIMS Hospital",
            slug="sims-hospital",
            category="Healthcare",
            short_desc="Hospital operations and patient workflow management toolkit.",
            full_desc=(
                "SIMS Hospital provides operational modules for appointments, patient flow, "
                "billing checkpoints, and clinical communication dashboards."
            ),
            version="1.0.0",
            tags=["Healthcare", "Operations", "Hospital"],
            os_support=["Windows", "Linux", "Web"],
            setup_instructions="Package not uploaded yet. Admin can upload ZIP from Admin panel.",
            changelog="Initial metadata seed.",
        )
        self._seed_if_missing(
            name="Stock Master",
            slug="stock-master",
            category="Finance",
            short_desc="Portfolio tracking and market watch assistant for business users.",
            full_desc=(
                "Stock Master includes modules for watchlists, portfolio snapshots, "
                "price alerts, and business-oriented market tracking workflows."
            ),
            version="1.0.0",
            tags=["Finance", "Trading", "Analytics"],
            os_support=["Windows", "Linux", "Web"],
            setup_instructions="Package not uploaded yet. Admin can upload ZIP from Admin panel.",
            changelog="Initial metadata seed.",
        )

    def _seed_if_missing(
        self,
        *,
        name: str,
        slug: str,
        category: str,
        short_desc: str,
        full_desc: str,
        version: str,
        tags: List[str],
        os_support: List[str],
        setup_instructions: str,
        changelog: str,
    ) -> None:
        with self._connect() as conn:
            exists = conn.execute("SELECT id FROM apps WHERE slug = ?", (slug,)).fetchone()
            if exists:
                return
            now = self._now_iso()
            conn.execute(
                """
                INSERT INTO apps (
                    name, slug, category, short_desc, full_desc, version,
                    tags_json, os_support_json, setup_instructions, changelog,
                    zip_path, package_path, logo_path, screenshots_json,
                    is_active, downloads, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    slug,
                    category,
                    short_desc,
                    full_desc,
                    version,
                    json.dumps(tags),
                    json.dumps(os_support),
                    setup_instructions,
                    changelog,
                    "",
                    "",
                    None,
                    json.dumps([]),
                    1,
                    0,
                    now,
                    now,
                ),
            )
            conn.commit()

    @staticmethod
    def _slugify(name: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        return slug or "app"

    @staticmethod
    def _sanitize_version(version: str) -> str:
        clean = re.sub(r"[^a-zA-Z0-9._-]+", "-", version.strip())
        return clean or "1.0.0"

    def _relative_path(self, path: Path) -> str:
        try:
            rel = path.resolve().relative_to(self.project_root.resolve())
            return rel.as_posix()
        except Exception:
            return path.as_posix()

    def _absolute_path(self, stored_path: str) -> Optional[Path]:
        if not stored_path:
            return None
        path = Path(stored_path)
        if path.is_absolute():
            return path
        return self.project_root / path

    @staticmethod
    def _parse_json_list(raw: Optional[str]) -> List[str]:
        if not raw:
            return []
        try:
            val = json.loads(raw)
            if isinstance(val, list):
                return [str(item).strip() for item in val if str(item).strip()]
        except Exception:
            return []
        return []

    def _row_to_app(self, row: sqlite3.Row) -> Dict[str, Any]:
        app = dict(row)
        app["tags"] = self._parse_json_list(app.get("tags_json"))
        app["os_support"] = self._parse_json_list(app.get("os_support_json"))
        app["screenshots"] = self._parse_json_list(app.get("screenshots_json"))
        app["is_active"] = bool(int(app.get("is_active", 0)))
        app["downloads"] = int(app.get("downloads", 0) or 0)
        return app

    @staticmethod
    def _clean_csv_values(raw: str) -> List[str]:
        return [part.strip() for part in raw.split(",") if part.strip()]

    def _normalize_metadata(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        name = str(payload.get("name", "")).strip()
        if not name:
            raise ValueError("App name is required.")

        category = str(payload.get("category", "Other")).strip() or "Other"
        if category not in DEFAULT_CATEGORIES:
            category = "Other"

        short_desc = str(payload.get("short_desc", "")).strip()
        full_desc = str(payload.get("full_desc", "")).strip()
        version = self._sanitize_version(str(payload.get("version", "1.0.0")))

        tags = payload.get("tags", [])
        if isinstance(tags, str):
            tags = self._clean_csv_values(tags)
        tags = [str(item).strip() for item in tags if str(item).strip()]

        os_support = payload.get("os_support", [])
        if isinstance(os_support, str):
            os_support = self._clean_csv_values(os_support)
        os_support = [str(item).strip() for item in os_support if str(item).strip()]

        setup_instructions = str(payload.get("setup_instructions", "")).strip()
        changelog = str(payload.get("changelog", "")).strip()
        is_active = 1 if bool(payload.get("is_active", True)) else 0

        return {
            "name": name,
            "slug": self._slugify(name),
            "category": category,
            "short_desc": short_desc,
            "full_desc": full_desc or short_desc,
            "version": version,
            "tags_json": json.dumps(tags),
            "os_support_json": json.dumps(os_support),
            "setup_instructions": setup_instructions,
            "changelog": changelog,
            "is_active": is_active,
        }

    def has_admin_users(self) -> bool:
        with self._connect() as conn:
            row = conn.execute("SELECT COUNT(1) AS cnt FROM admin_users").fetchone()
            return bool(row and int(row["cnt"]) > 0)

    def create_initial_admin(self, username: str, password: str) -> Tuple[bool, str]:
        if self.has_admin_users():
            return False, "Admin already initialized."

        username = username.strip()
        if not username:
            return False, "Username is required."
        if len(password) < 8:
            return False, "Password must be at least 8 characters."

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        now = self._now_iso()

        try:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO admin_users (username, password_hash, created_at) VALUES (?, ?, ?)",
                    (username, password_hash, now),
                )
                conn.commit()
            return True, "Admin account initialized successfully."
        except sqlite3.IntegrityError:
            return False, "Username already exists."

    def verify_admin(self, username: str, password: str) -> bool:
        username = username.strip()
        if not username or not password:
            return False
        with self._connect() as conn:
            row = conn.execute(
                "SELECT password_hash FROM admin_users WHERE username = ?",
                (username,),
            ).fetchone()
        if not row:
            return False
        try:
            return bcrypt.checkpw(password.encode("utf-8"), row["password_hash"].encode("utf-8"))
        except Exception:
            return False

    def get_categories(self, active_only: bool = True) -> List[str]:
        apps = self.list_admin_apps()
        categories = {app["category"] for app in apps if app.get("category")}
        if active_only:
            categories = {app["category"] for app in apps if app.get("is_active")}
        return sorted(set(DEFAULT_CATEGORIES) | categories)

    def get_all_tags(self, active_only: bool = True) -> List[str]:
        tags: set[str] = set()
        for app in self.list_admin_apps():
            if active_only and not app.get("is_active"):
                continue
            for tag in app.get("tags", []):
                clean = str(tag).strip()
                if clean:
                    tags.add(clean)
        return sorted(tags)

    def list_apps(
        self,
        *,
        search: str = "",
        category: str = "All",
        tags: Optional[List[str]] = None,
        page: int = 1,
        per_page: int = 12,
        active_only: bool = True,
    ) -> Dict[str, Any]:
        where = "WHERE is_active = 1" if active_only else ""
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM apps {where} ORDER BY datetime(updated_at) DESC, name ASC"
            ).fetchall()

        apps = [self._row_to_app(row) for row in rows]
        query = search.strip().lower()
        selected_tags = {tag.strip().lower() for tag in (tags or []) if tag.strip()}

        filtered: List[Dict[str, Any]] = []
        for app in apps:
            if category and category != "All" and app.get("category") != category:
                continue

            if query:
                haystack_parts = [
                    app.get("name", ""),
                    app.get("short_desc", ""),
                    app.get("full_desc", ""),
                    " ".join(app.get("tags", [])),
                ]
                haystack = " ".join(str(part) for part in haystack_parts).lower()
                if query not in haystack:
                    continue

            if selected_tags:
                app_tags = {str(tag).lower() for tag in app.get("tags", [])}
                if not app_tags.intersection(selected_tags):
                    continue

            filtered.append(app)

        total = len(filtered)
        per_page = max(1, int(per_page))
        total_pages = max(1, (total + per_page - 1) // per_page)
        page = max(1, min(int(page), total_pages))
        start = (page - 1) * per_page
        end = start + per_page

        return {
            "items": filtered[start:end],
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
        }

    def list_admin_apps(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM apps ORDER BY datetime(updated_at) DESC, name ASC"
            ).fetchall()
        return [self._row_to_app(row) for row in rows]

    def get_app_by_slug(self, slug: str, include_inactive: bool = False) -> Optional[Dict[str, Any]]:
        condition = "slug = ?" if include_inactive else "slug = ? AND is_active = 1"
        with self._connect() as conn:
            row = conn.execute(f"SELECT * FROM apps WHERE {condition}", (slug,)).fetchone()
        return self._row_to_app(row) if row else None

    def get_app_by_id(self, app_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM apps WHERE id = ?", (int(app_id),)).fetchone()
        return self._row_to_app(row) if row else None

    def _safe_extract_zip(self, zip_path: Path, dest_dir: Path) -> None:
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zf:
            for member in zf.infolist():
                member_path = (dest_dir / member.filename).resolve()
                if not str(member_path).startswith(str(dest_dir.resolve())):
                    raise ValueError("ZIP contains invalid paths.")
            zf.extractall(dest_dir)

    def _iter_included_files(self, folder: Path) -> Iterable[Path]:
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIR_NAMES]
            root_path = Path(root)
            for filename in files:
                full_path = root_path / filename
                rel_parts = full_path.relative_to(folder).parts
                if any(part in EXCLUDED_DIR_NAMES for part in rel_parts):
                    continue
                yield full_path

    def _write_zip_from_folder(self, folder: Path, slug: str, version: str) -> Path:
        zip_filename = f"{slug}-{self._sanitize_version(version)}.zip"
        zip_path = self.zips_dir / zip_filename
        files = list(self._iter_included_files(folder))
        if not files:
            raise ValueError("Folder has no eligible files after exclusions.")

        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file_path in files:
                arcname = file_path.relative_to(folder).as_posix()
                zf.write(file_path, arcname)
        return zip_path

    def _upsert_app_record(
        self,
        *,
        metadata: Dict[str, Any],
        zip_path: Optional[Path],
        package_path: Optional[Path],
    ) -> Tuple[int, str]:
        slug = metadata["slug"]
        now = self._now_iso()
        zip_rel = self._relative_path(zip_path) if zip_path else ""
        package_rel = self._relative_path(package_path) if package_path else ""

        with self._connect() as conn:
            existing = conn.execute("SELECT * FROM apps WHERE slug = ?", (slug,)).fetchone()
            if existing:
                existing_data = self._row_to_app(existing)
                conn.execute(
                    """
                    UPDATE apps
                    SET name = ?, category = ?, short_desc = ?, full_desc = ?, version = ?,
                        tags_json = ?, os_support_json = ?, setup_instructions = ?, changelog = ?,
                        zip_path = ?, package_path = ?, logo_path = ?, screenshots_json = ?,
                        is_active = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        metadata["name"],
                        metadata["category"],
                        metadata["short_desc"],
                        metadata["full_desc"],
                        metadata["version"],
                        metadata["tags_json"],
                        metadata["os_support_json"],
                        metadata["setup_instructions"],
                        metadata["changelog"],
                        zip_rel or existing_data.get("zip_path", ""),
                        package_rel or existing_data.get("package_path", ""),
                        existing_data.get("logo_path"),
                        json.dumps(existing_data.get("screenshots", [])),
                        metadata["is_active"],
                        now,
                        int(existing_data["id"]),
                    ),
                )
                conn.commit()
                return int(existing_data["id"]), "updated"

            cur = conn.execute(
                """
                INSERT INTO apps (
                    name, slug, category, short_desc, full_desc, version,
                    tags_json, os_support_json, setup_instructions, changelog,
                    zip_path, package_path, logo_path, screenshots_json,
                    is_active, downloads, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    metadata["name"],
                    slug,
                    metadata["category"],
                    metadata["short_desc"],
                    metadata["full_desc"],
                    metadata["version"],
                    metadata["tags_json"],
                    metadata["os_support_json"],
                    metadata["setup_instructions"],
                    metadata["changelog"],
                    zip_rel,
                    package_rel,
                    None,
                    json.dumps([]),
                    metadata["is_active"],
                    0,
                    now,
                    now,
                ),
            )
            conn.commit()
            return int(cur.lastrowid), "created"

    def add_or_update_app_from_uploaded_zip(
        self,
        *,
        metadata: Dict[str, Any],
        zip_bytes: bytes,
    ) -> Tuple[bool, str, Optional[int]]:
        if not zip_bytes:
            return False, "ZIP file is empty.", None

        try:
            normalized = self._normalize_metadata(metadata)
        except ValueError as exc:
            return False, str(exc), None

        slug = normalized["slug"]
        version = normalized["version"]
        zip_filename = f"{slug}-{self._sanitize_version(version)}.zip"
        zip_path = self.zips_dir / zip_filename
        package_path = self.packages_dir / slug

        try:
            zip_path.write_bytes(zip_bytes)
            self._safe_extract_zip(zip_path, package_path)
            app_id, mode = self._upsert_app_record(
                metadata=normalized,
                zip_path=zip_path,
                package_path=package_path,
            )
            return True, f"App {mode} successfully from ZIP upload.", app_id
        except zipfile.BadZipFile:
            if zip_path.exists():
                zip_path.unlink()
            return False, "Invalid ZIP file. Please upload a valid .zip package.", None
        except Exception as exc:
            return False, f"Could not process ZIP upload: {exc}", None

    def add_or_update_app_from_folder(
        self,
        *,
        metadata: Dict[str, Any],
        folder_path: str,
    ) -> Tuple[bool, str, Optional[int]]:
        raw = folder_path.strip().strip('"').strip("'")
        if not raw:
            return False, "Folder path is required.", None

        folder = Path(raw).expanduser()
        if not folder.exists():
            return False, "The provided folder path does not exist.", None
        if not folder.is_dir():
            return False, "The provided path is not a directory.", None

        has_files = any(path.is_file() for path in folder.rglob("*"))
        if not has_files:
            return False, "The provided folder is empty.", None

        try:
            normalized = self._normalize_metadata(metadata)
        except ValueError as exc:
            return False, str(exc), None

        slug = normalized["slug"]
        version = normalized["version"]
        package_path = self.packages_dir / slug

        try:
            zip_path = self._write_zip_from_folder(folder, slug, version)
            self._safe_extract_zip(zip_path, package_path)
            app_id, mode = self._upsert_app_record(
                metadata=normalized,
                zip_path=zip_path,
                package_path=package_path,
            )
            return True, f"App {mode} successfully from local folder.", app_id
        except Exception as exc:
            return False, f"Could not package local folder: {exc}", None

    def update_app_metadata(self, app_id: int, payload: Dict[str, Any]) -> Tuple[bool, str]:
        existing = self.get_app_by_id(app_id)
        if not existing:
            return False, "App not found."

        merged = {
            "name": payload.get("name", existing.get("name", "")),
            "category": payload.get("category", existing.get("category", "Other")),
            "short_desc": payload.get("short_desc", existing.get("short_desc", "")),
            "full_desc": payload.get("full_desc", existing.get("full_desc", "")),
            "version": payload.get("version", existing.get("version", "1.0.0")),
            "tags": payload.get("tags", existing.get("tags", [])),
            "os_support": payload.get("os_support", existing.get("os_support", [])),
            "setup_instructions": payload.get(
                "setup_instructions",
                existing.get("setup_instructions", ""),
            ),
            "changelog": payload.get("changelog", existing.get("changelog", "")),
            "is_active": payload.get("is_active", existing.get("is_active", True)),
        }

        try:
            normalized = self._normalize_metadata(merged)
        except ValueError as exc:
            return False, str(exc)

        now = self._now_iso()
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE apps
                SET name = ?, category = ?, short_desc = ?, full_desc = ?, version = ?,
                    tags_json = ?, os_support_json = ?, setup_instructions = ?, changelog = ?,
                    is_active = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    normalized["name"],
                    normalized["category"],
                    normalized["short_desc"],
                    normalized["full_desc"],
                    normalized["version"],
                    normalized["tags_json"],
                    normalized["os_support_json"],
                    normalized["setup_instructions"],
                    normalized["changelog"],
                    normalized["is_active"],
                    now,
                    int(app_id),
                ),
            )
            conn.commit()
        return True, "App metadata updated."

    def set_app_active(self, app_id: int, is_active: bool) -> Tuple[bool, str]:
        existing = self.get_app_by_id(app_id)
        if not existing:
            return False, "App not found."
        with self._connect() as conn:
            conn.execute(
                "UPDATE apps SET is_active = ?, updated_at = ? WHERE id = ?",
                (1 if is_active else 0, self._now_iso(), int(app_id)),
            )
            conn.commit()
        return True, "App visibility updated."

    def delete_app(self, app_id: int) -> Tuple[bool, str]:
        app = self.get_app_by_id(app_id)
        if not app:
            return False, "App not found."

        for key, is_dir in (("zip_path", False), ("package_path", True)):
            abs_path = self._absolute_path(str(app.get(key, "")))
            if not abs_path:
                continue
            try:
                resolved = abs_path.resolve()
                root_resolved = self.project_root.resolve()
                if not str(resolved).startswith(str(root_resolved)):
                    continue
                if resolved.exists():
                    if is_dir and resolved.is_dir():
                        shutil.rmtree(resolved)
                    elif not is_dir and resolved.is_file():
                        resolved.unlink()
            except Exception:
                # Keep DB deletion independent from filesystem cleanup edge cases.
                pass

        with self._connect() as conn:
            conn.execute("DELETE FROM apps WHERE id = ?", (int(app_id),))
            conn.commit()
        return True, "App deleted."

    def increment_downloads(self, app_id: int) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE apps SET downloads = downloads + 1 WHERE id = ?", (int(app_id),))
            conn.commit()

    def get_zip_bytes(self, app_id: int) -> Optional[bytes]:
        app = self.get_app_by_id(app_id)
        if not app:
            return None
        zip_path = self._absolute_path(str(app.get("zip_path", "")))
        if not zip_path or not zip_path.exists() or not zip_path.is_file():
            return None
        return zip_path.read_bytes()

    def get_download_filename(self, app: Dict[str, Any]) -> str:
        zip_path = self._absolute_path(str(app.get("zip_path", "")))
        if zip_path and zip_path.exists():
            return zip_path.name
        slug = str(app.get("slug", "app")).strip() or "app"
        version = self._sanitize_version(str(app.get("version", "1.0.0")))
        return f"{slug}-{version}.zip"

    def list_download_stats(self) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, name, category, version, downloads, is_active, updated_at
                FROM apps
                ORDER BY downloads DESC, name ASC
                """
            ).fetchall()
        return [dict(row) for row in rows]
