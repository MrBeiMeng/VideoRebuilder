import os
import re


def list_files(directory):
    return sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))], reverse=True)


def match_files(dir1, dir2):
    files1 = list_files(dir1)
    files2 = list_files(dir2)

    matched_pairs = []

    for file1 in files1:
        # match = re.search(r'S\d+E(\d+)', file1)
        # match = re.search(r'S01E(\d+)', file1)
        match = re.search(r'(\d+)', file1)
        if match:
            episode_number = int(match.group(1))  # Convert to integer to remove leading zeros
            breaked = False
            for file2 in files2:
                if re.match(fr'^{episode_number}\b', file2):
                    matched_pairs.append((os.path.join(dir1, file1), os.path.join(dir2, file2)))
                    breaked = True
                    break  # Assuming only one match per directory, remove this line if there could be multiple matches

            if not breaked:
                matched_pairs.append((os.path.join(dir1, file1), ''))

    return matched_pairs


# Directories to match files between
dir1 = 'E:/data/Penguins/'
dir2 = 'E:/360MoveData/Users/MrB/Desktop/penguins_finally/'

# Get matched file pairs
matched_file_pairs = match_files(dir1, dir2)

print(matched_file_pairs)

# Print matched pairs
for pair in matched_file_pairs:
    print(pair)
