from json import load, dump
from argparse import ArgumentParser

#temporarily the default loccation for this is pwd;
#should change but meh
METADATA = "metadata.json"
STRING="string.json"

with open(METADATA) as f:
    metadata = load(f)

with open(STRING) as f:
    string = load(f)

#not a whole lot in this script, just a main
def main(target_id, new_entry):
    
    #all three of these directly reference metadata
    storage = metadata["stringStorage"]
    info = metadata["stringTableEntries"]
    header = metadata["header"]

    original_storage_len = len(storage)

    print("Modifying the header...\n")
    #increment by length of new entry
    header["stringStorageSize"] += len(new_entry)

    print("Adding the string to the end of the storage...\n")
    #append the byte-version of the entry to the end
    #of the storage
    storage += [ ord(letter) for letter in new_entry ] 

    print(f"Modifying the table entry:\n\t{info[target_id]}\n")
    #modify the table entry so it now points to the end
    #of the string storage instead of it's original
    info[target_id] = {
        'isUTF16': 0,
        'offset': original_storage_len-1,
        'length': len(new_entry)
        }

    print(f"Modifying string.json at {target_id}\n")

    #modify the string that's in string.json so it all lines up
    string[target_id]["value"] = new_entry

    with open("new_metadata.json", "w") as f:
        dump(metadata, f)

    with open("new_string.json", "w") as f:
        dump(string, f)

    print("Success!")

if __name__ == "__main__":
    
    parser = ArgumentParser()

    parser.add_argument(
        "id",
        help="ID of the string inside of the string.json file to target",
        type=int
    )

    parser.add_argument(
        "entry",
        help="string to have the table entry point to"
    )

    args = parser.parse_args()

    main(args.id, args.entry)

