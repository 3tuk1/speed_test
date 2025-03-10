from pathlib import Path
CURDIR = Path.cwd()

def get_fqdn(server):
    return server["host"].split(':')[0]

def gen_filename(name:str, ext:str, dir:str) -> Path:
    # ディレクトリが存在しない場合に作成
    dir_path = CURDIR / dir
    if not dir_path.exists():
        dir_path.mkdir()
        
    file_name = f"{name}.{ext}"
    file_path = dir_path / file_name
    counter = 1
    while file_path.exists():
        file_path = dir_path / f"{name}_{counter}.{ext}"
        counter += 1
    return file_path.absolute()