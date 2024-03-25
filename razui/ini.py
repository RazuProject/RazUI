def read_ini(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as ini_file: ini = ini_file.read(); ini_file.close()
    
    result = {}
    current_header = None
    
    ini = [line.split(";",1)[0].strip() for line in ini.split("\n") if not(line.strip().startswith(";") or line.strip()=="")]
    for line in ini:
        if line.startswith("["): current_header = line.strip()[1:-1].strip(); result[current_header] = {}; continue
        if line.split("=",1)[1].strip().isdigit():
            result[current_header][line.split("=",1)[0].strip()] = int(line.split("=",1)[1].strip())
            continue
        elif line.split("=",1)[1].strip().startswith("\"") and line.split("=",1)[1].strip().endswith("\""):
            result[current_header][line.split("=",1)[0].strip()] = line.split("=",1)[1].strip()[1:-1]
            continue
        result[current_header][line.split("=",1)[0].strip()] = line.split("=",1)[1].strip()
    
    print(result)
    return result