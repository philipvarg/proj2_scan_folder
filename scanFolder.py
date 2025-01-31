
# setup
import os, sys
import matplotlib.pyplot as plt
import datetime as dt

save_folder = "SCAN"
if not os.path.exists(save_folder):
    os.mkdir(save_folder)

# Input and validate folder
folder = input("Enter folder to scan: ")
print(f"FOLDER, {folder}")
if not os.path.exists(folder):
    print(f"Folder {folder} does not exist!")
    sys.exit(0)
print("Continuing script!")

files = os.listdir(folder) # get the list of files

# Split filename into 2 parts, name and extension
files = [f.split(".") for f in files]
# FILTER OUT folders and hidden files. Criteria, must have name and ext and name is not empty str.
files = [f for f in files if len(f) == 2 and f[0] != '']

# FILTER 1: we will use the filtered file list to make 2 dictonarys - files and unique extensions
files_dict = {".".join(f):0 for f in files} # dict of the filtered files, all values zero

ext_dict ={f[1] for f in files}     # we extraxt the ext part and use set to filter out duplicate ext.
ext_dict = {e:0 for e in ext_dict}  # dict using ext as key, all values zero

# at this point we have a dict of unique extensions, each value set to zero lines of code.
# we now read each file in file-dict for the number of code lines and assign the values into the file-dict.
# try-except is used to filter out non-line files
others = [] # list to store non-readlines files
for k in files_dict:
    try:
        with open(folder + os.sep + k, "r") as r:
            read = r.readlines()
            if len(read) == 0:
                others.append(k)
    except UnicodeDecodeError as e:
        others.append(k)
        continue
    
    files_dict[k] = len(read)
print(f"These files have no code {others}")

# FILTER 2: Delete all non-readlines files
for o in others:
    files_dict = {k:v for k,v in files_dict.items() if k != o}
    ext_dict = {e:v for e,v in ext_dict.items() if e != o.split(".")[1]}

# interate thru file-dict, get the ext, use the ext to accumulate values for each file type in ext-dict.
for k in files_dict:
    ext_key = k.split(".")[1]
    ext_dict[ext_key] += files_dict[k]

# total of all the unique ext.
total = sum(ext_dict.values())

# calculate percentages
for k in ext_dict:
    value = (ext_dict[k] / total) * 100
    r_value = round(value, 1)
    ext_dict[k] = str(r_value)+"%"

for k in ext_dict:
    print(f"Language: {k}")

# PLOT BAR GRAPH
plt.figure(figsize = (10, 5))
plt.title(f"% of Languages in {folder} directory", fontsize = 20)

data = list(ext_dict.values())
labels = list(ext_dict.keys())

for k in ext_dict:
    number = float(ext_dict[k].split("%")[0])
    plt.bar(k, height = number)

timestamp = dt.datetime.now().strftime("%Y-%m-%d")
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlabel("languages", fontsize = 15)
plt.ylabel("%", fontsize = 15)
plt.legend(labels = data, fontsize = 15)
plt.savefig(save_folder + os.sep + folder + f"__{timestamp}__.png", bbox_inches = "tight")
plt.show()
