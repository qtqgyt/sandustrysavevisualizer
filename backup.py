import platformdirs
import os
import shutil

data_dir = platformdirs.user_config_dir("sandustrysaveviewer")
backups_dir = os.path.join(data_dir, "Backups")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    os.makedirs(backups_dir)
if not os.path.exists(backups_dir):
    os.makedirs(backups_dir)

def createbackup(savepath):
    shutil.copy(savepath, os.path.join(backups_dir, os.path.basename(savepath) + ".bak"))
