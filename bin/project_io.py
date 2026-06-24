import os
import glob
import zipfile
import base64
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from github import Github



class ProjectIO:
    def __init__(self, studio):
        self.studio = studio
        self.github_pat = None

    def export_project(self):
        """Zip config/, custom_modules/, and root project files to a user-chosen .zip."""
        self.studio.save_cb()

        # zip_path, _ = QFileDialog.getSaveFileName(
        #     self.studio, "Export project", "project.zip", "Zip files (*.zip)"
        # )
        if not zip_path:
            return
        if not zip_path.endswith(".zip"):
            zip_path += ".zip"

        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for fname in ["main.cpp", "Makefile", "VERSION.txt"]:
                    fpath = os.path.join(self.studio.current_dir, fname)
                    if os.path.isfile(fpath):
                        zf.write(fpath, fname)

                for subdir in ["config", "custom_modules"]:
                    for fpath in glob.glob(os.path.join(self.studio.current_dir, subdir, "*")):
                        if os.path.isfile(fpath):
                            zf.write(fpath, os.path.join(subdir, os.path.basename(fpath)))

            print(f"project_io: exported project to {zip_path}")

        except Exception as e:
            self._show_error(f"Export failed: {e}")

    def import_project(self):
        """Extract a previously exported .zip into the current project directory and reload."""
        zip_path, _ = QFileDialog.getOpenFileName(
            self.studio, "Import project", "", "Zip files (*.zip)"
        )
        if not zip_path:
            return

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                for member in zf.namelist():
                    dest = Path(self.studio.current_dir) / member
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if not member.endswith("/"):
                        dest.write_bytes(zf.read(member))

            print(f"project_io: imported project from {zip_path}")

            try:
                self.studio.load_model("PhysiCell_settings")
            except Exception as e:
                self._show_error(
                    f"Project files extracted but could not reload config: {e}\n"
                    "Use File > Open to load your .xml manually."
                )

        except Exception as e:
            self._show_error(f"Import failed: {e}")

    def upload_binary_file(self, repo_name, local_path, github_path, commit_message, branch_name):
        """Upload a binary file to a GitHub repository using self.github_pat."""
        g = Github(self.github_pat)
        repo = g.get_repo(repo_name)

        with open(local_path, 'rb') as f:
            encoded_content = base64.b64encode(f.read()).decode("utf-8")

        try:
            contents = repo.get_contents(github_path, ref=branch_name)
            repo.update_file(
                contents.path,
                commit_message,
                encoded_content,
                contents.sha,
                branch=branch_name
            )
            print(f"File '{github_path}' updated successfully.")
        except Exception:
            repo.create_file(
                github_path,
                commit_message,
                encoded_content,
                branch=branch_name
            )
            print(f"File '{github_path}' created successfully.")

    def _show_error(self, msg):
        box = QMessageBox(self.studio)
        box.setIcon(QMessageBox.Warning)
        box.setText(msg)
        box.exec()


