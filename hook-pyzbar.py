from PyInstaller.utils.hooks import collect_data_files

hiddenimports = ['pyzbar']
datas = collect_data_files('pyzbar')
