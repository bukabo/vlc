import os


def FileList(c_dir):
    files = []
    med_ext = ['.avi', '.mkv']
    # pathh = []
    for r, d, f in os.walk(c_dir):
        for file in f:
            if any(ext in file for ext in med_ext):
                files.append(os.path.join(r, file))
                # files.append(os.path.join(r, file))
    return sorted(files)


def GetMaxID(sql, c):
    c.execute(sql)
    results = c.fetchall()
    maxPlId = results[0][0]
    return maxPlId
