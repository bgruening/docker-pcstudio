import os
import glob
import zipfile
import base64
import time
import traceback
from datetime import datetime
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from github import Github

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox,
)
# from PyQt5.QtGui import QIntValidator

from studio_classes import QCheckBox_custom

class ExportProjectWindow(QWidget):
    def __init__(self):
        super().__init__()

        stylesheet = """
            QPushButton{ border: 1px solid; border-color: rgb(145, 200, 145); border-radius: 1px;  background-color: lightgreen; color: black; width: 64px; padding-right: 8px; padding-left: 8px; padding-top: 3px; padding-bottom: 3px; }
            """

        self.xml_creator = None    # set by caller

        self.setStyleSheet(stylesheet)

        self.scroll = QScrollArea()
        self.vbox = QVBoxLayout()
        glayout = QGridLayout()
        self.vbox.addLayout(glayout)

        idx_row = 0
        self.export_file_button = QPushButton("Export .zip")
        self.export_file_button.setFixedWidth(90)
        self.export_file_button.setEnabled(True)
        self.export_file_button.setStyleSheet("background-color: lightgreen;")
        self.export_file_button.clicked.connect(self.export_project_cb)
        glayout.addWidget(self.export_file_button, idx_row, 0, 1, 1) # w, row, column, rowspan, colspan

        self.project_name_w = QLineEdit("my_model")
        # self.project_name_w.setFixedWidth(200)
        self.project_name_w.setEnabled(True)
        glayout.addWidget(self.project_name_w, idx_row, 1, 1, 1)


        self.timestamp_w = QCheckBox_custom("time-stamp")
        glayout.addWidget(self.timestamp_w, idx_row, 2, 1, 1)

        idx_row += 1
        glayout.addWidget(QLabel("GitHub info:"), idx_row, 0, 1, 1)
        # upload_binary_file(..., repo_name, local_path, github_path, commit_message, branch_name):
        glayout.addWidget(QLabel("username"), idx_row, 1, 1, 1)
        glayout.addWidget(QLabel("repo"), idx_row, 2, 1, 1)

        idx_row += 1
        self.github_user_name = "user"
        self.github_user_w = QLineEdit(self.github_user_name)
        # self.github_user_w.setFixedWidth(200)
        self.github_user_w.setEnabled(True)
        glayout.addWidget(self.github_user_w, idx_row, 1, 1, 1)

        self.github_repo_name = "repo"
        self.github_repo_w = QLineEdit(self.github_repo_name)
        # self.github_user_w.setFixedWidth(200)
        self.github_repo_w.setEnabled(True)
        glayout.addWidget(self.github_repo_w, idx_row, 2, 1, 1)

        idx_row += 1
        msg = ("Click Export to have your project zipped and copied to your GitHub repo.\n"
               "Rename the base filename if you wish.\n"
               "It may take a few seconds to appear in your repo.")
        glayout.addWidget(QLabel(msg), idx_row, 0, 1, 3)

        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("background-color: lightgreen;")
        self.close_button.clicked.connect(self.close)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.vbox.addWidget(self.close_button)
        self.setLayout(self.vbox)

    def show_info_message(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()

    def export_project_cb(self):
        self.github_user_name = self.github_user_w.text()
        self.github_repo_name = self.github_repo_w.text()

        fname = self.project_name_w.text()
        if self.timestamp_w.isChecked():
            ts = datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S")
            fname = f"{fname}_{ts}.zip"
        else:
            fname = f"{fname}.zip"

        msgBox = QMessageBox()
        msgBox.setText(f"This will bundle your current model's config file, its cells/substrates ICs, and rules, "
                   f"then copy '{fname}' to the specified GitHub repo.")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if msgBox.exec() == QMessageBox.Cancel:
            return

        # self.show_info_message(f"export_project_cb(): zipping proj into {fname}")
        self.show_info_message(f"zipping project into {fname}")
        file_str = os.path.join(os.getcwd(), "config/*.csv")
        # print('-------- export_project_cb(): zip up all', file_str)
        try:
            with zipfile.ZipFile(fname, 'w') as myzip:
                myzip.write(self.xml_creator.current_xml_file,
                            os.path.basename(self.xml_creator.current_xml_file))
                for f in glob.glob(file_str):
                    myzip.write(f, os.path.basename(f))

            # put(fname)
            # self.upload_binary_file(repo_name, local_path, github_path, commit_message, branch_name)
            # repo_name = self.github_user_w.text() + "/" + self.github_repo_w.text()
            repo_name = os.path.join(self.github_user_name, self.github_repo_name)
            # self.show_info_message(f"repo_name is {repo_name}")

            # print("repo_name= ",repo_name)
            github_pat_str = self.xml_creator.project_io.github_pat # token (PAT)
            if github_pat_str is None:
                # pass
                self.show_error_message("github_pat_str is None")
            else:
                github_pat_str = github_pat_str.rstrip("\r\n")
            # self.show_info_message(f"github_pat_str is {github_pat_str}. Calling upload_binary_file: repo={repo_name}, fname={fname}")
            self.upload_binary_file(github_pat_str, repo_name, fname, fname, "update project", "main")
        except KeyError:
            msg = traceback.format_exc()
            self.show_error_message(msg)


    def upload_binary_file(self, pa_token, repo_name, local_path, github_path, commit_message, branch_name):
        """Upload a binary file to a GitHub repository using a GitHub personal access token"""
        try:
            g = Github(pa_token)
            repo = g.get_repo(repo_name)
        except Exception:
            self.show_error_message(f"Error connecting to {repo_name}")
            return

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

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setFixedWidth(500)
        msg.exec_()

#--------------------------------------
class ProjectIO:
    def __init__(self, studio):
        self.studio = studio
        self.zip_basename = "my_project"
        self.export_project_UI = None

    @property
    def github_pat(self):
        settings = getattr(self.studio, 'studio_settings', None)
        return settings.github_pat if settings is not None else None

    @github_pat.setter
    def github_pat(self, value):
        settings = getattr(self.studio, 'studio_settings', None)
        if settings is not None:
            settings.github_pat = value

    def export_project(self):
        """Zip config/, custom_modules/, and root project files to a user-chosen .zip."""
        self.studio.save_cb()

        self.export_project_github_ui()

        # zip_path, _ = QFileDialog.getSaveFileName(
        #     self.studio, "Export project", "project.zip", "Zip files (*.zip)"
        # )
        # if not zip_path:
            # return
        # if not zip_path.endswith(".zip"):
            # zip_path += ".zip"

        try:
            zip_path = self.zip_basename + ".zip"
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
        # zip_path, _ = QFileDialog.getOpenFileName(
        #     self.studio, "Import project", "", "Zip files (*.zip)"
        # )
        # if not zip_path:
        #     return

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

    # def upload_binary_file(self, token, repo_name, local_path, github_path, commit_message, branch_name):
    #     """Upload a binary file to a GitHub repository using self.github_pa_token."""
    #     g = Github(self.github_pa_token)
    #     repo = g.get_repo(repo_name)

    #     with open(local_path, 'rb') as f:
    #         encoded_content = base64.b64encode(f.read()).decode("utf-8")

    #     try:
    #         contents = repo.get_contents(github_path, ref=branch_name)
    #         repo.update_file(
    #             contents.path,
    #             commit_message,
    #             encoded_content,
    #             contents.sha,
    #             branch=branch_name
    #         )
    #         print(f"File '{github_path}' updated successfully.")
    #     except Exception:
    #         repo.create_file(
    #             github_path,
    #             commit_message,
    #             encoded_content,
    #             branch=branch_name
    #         )
    #         print(f"File '{github_path}' created successfully.")

    def _show_error(self, msg):
        box = QMessageBox(self.studio)
        box.setIcon(QMessageBox.Warning)
        box.setText(msg)
        box.exec()



    def export_project_github_ui(self):
        if self.export_project_UI is None:
            self.export_project_UI = ExportProjectWindow()
            self.export_project_UI.xml_creator = self.studio
        self.export_project_UI.show()
        self.export_project_UI.raise_()


    # def import_project_github_history(self):
    #     self.project_historyUI = ImportProjectWindow()
    #     self.project_historyUI.xml_creator = self
    #     self.project_historyUI.hide()
    #     self.project_historyUI.show()
