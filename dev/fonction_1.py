import Gaffer
import GafferUI
import os
import sys
from PySide2.QtWidgets import QApplication, QMessageBox

root = plug.node().scriptNode()
pathroot = root["variables"]["stim:path"]["value"].getValue()
entity = root["variables"]["stim:entity"]["value"].getValue()

def to_lowercase(word):
    if any(c.isupper() for c in word):
        return word.lower()
    else:
        return word

department = to_lowercase(entity.split("_")[-1])
SHOW = os.environ.get("STIM_SHOW")

def create_render_folder(directory):
    images_folder = os.path.join(directory, "images")
    render_folder = os.path.join(images_folder, "renders")
    return render_folder

def create_entity_folder(renders_folder):
    # Générer le chemin cible sans vérifier l'existence
    entity_folder = os.path.join(renders_folder, department)
    return entity_folder

def create_new_version(entity_folder):
    folder_format = "{}{:03d}"
    base_name = "v"
    version_number = 1
    folder_name = folder_format.format(base_name, version_number)

    while os.path.exists(os.path.join(entity_folder, folder_name)):
        version_number += 1
        folder_name = folder_format.format(base_name, version_number)

    version_folder = os.path.join(entity_folder, folder_name)
    return version_folder


def check_previous_version(entity_folder):
    version_folder = os.path.join(entity_folder, find_latest_version(entity_folder))


    if os.path.exists(version_folder) and empty_folder(version_folder):
        app = QApplication.instance() or QApplication(sys.argv)
        warning_pop = QMessageBox()
        warning_pop.setWindowTitle("WARNING")
        t = "The current render directory is empty, are you sure to increment ?"
        warning_pop.setText(t)

        button_continue = warning_pop.addButton("Continue", QMessageBox.AcceptRole)
        button_cancel = warning_pop.addButton("Cancel", QMessageBox.RejectRole)

        warning_pop.exec_()

        if warning_pop.clickedButton() == button_continue:
            version_folder = create_new_version(entity_folder)
        else:
            print("Action annulée.")
    else:
        version_folder = create_new_version(entity_folder)

    return version_folder

def find_latest_version(entity_folder):
    version_prefix = 'v'
    latest_version = 0

    # Vérifier les versions existantes uniquement si le dossier existe
    if os.path.exists(entity_folder):
        for folder_name in os.listdir(entity_folder):
            if folder_name.startswith(version_prefix) and folder_name[1:].isdigit():
                version_number = int(folder_name[1:])
                latest_version = max(latest_version, version_number)

    return f'{version_prefix}{latest_version:03d}'



def empty_folder(version_folder):
    return not os.listdir(version_folder)


render_folder = create_render_folder(pathroot)
entity_folder = create_entity_folder(render_folder)
version_folder = check_previous_version(entity_folder).replace("\\", "/")
current_version = find_latest_version(entity_folder)
BATCHNAME = f'{SHOW + "_" + entity + "_" + current_version}'


plug = plug.node()
plug["asset"].setValue(entity)
plug["version"].setValue(version_folder.split("/")[-1])
plug["tweaks_tweak0_value"].setValue(version_folder)
plug["user_get_batch_name"].setValue(BATCHNAME)




root["variables"][""]["value"].getValue()