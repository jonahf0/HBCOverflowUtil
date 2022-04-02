from json import load,dump
from argparse import ArgumentParser

#just for testing; change to fit actual locations
METADATA = "metadata.json"
STRINGS = "string.json"

#read from the data files
with open(METADATA) as f:
    metadata = load(f)
with open(STRINGS) as f:
    strings = load(f)


#get info about the string
def get_string_info(id):
    target_symptom = strings[id]

    target_info = metadata["stringTableEntries"][id]
        
    target = metadata["stringStorage"][target_info["offset"]:target_info["offset"]+target_info["length"]]

    return target, target_info

#replace the info at the target location
def replace_info(byte_modified, target_info):
    
    offset = target_info["offset"]

    copy_storage = metadata["stringStorage"].copy()

    #this replaces the string at the offset with the new string
    copy_storage[offset:offset+len(byte_modified)] = byte_modified

    return copy_storage

#id is the ID of the string to replace, found in the string.json file
#modified is the string that you want to place at that ID location
def main(id, modified):

    #get info for the target and next entry
    target, target_info = get_string_info(id)
    
    print("Target string's info: \n\t{}".format(target_info))

    byte_modified = [ ord(letter) for letter in modified ]

    if len(byte_modified) <= len(target):
        print("Padding the string...")

        byte_modified = [ 32 for byte in range(0, len(target)-len(byte_modified) )] + byte_modified

        new_storage = replace_info(
                [ 32 for byte in range(0, len(target)-len(byte_modified) )] + byte_modified,
                target_info
        )

    else:
        #new_length_for_next_entry = total_length - len(byte_modified)
        new_storage = replace_info(byte_modified, target_info)
    
    copy_metadata = metadata.copy()

    copy_metadata["stringStorage"] = new_storage

    print("Modifying the length entry...")
    #make sure to modify the length of the table entry
    copy_metadata["stringTableEntries"][id]["length"] = len(byte_modified)

    print("New 'stringTableEntries' entry:\n\t{}".format(copy_metadata["stringTableEntries"][id]))

    print("Dumping the data to 'new_metadata.json'...")
    #dump the file, making sure not to overwrite the original
    with open("new_metadata.json", "w") as new:
        dump(copy_metadata, new)

    print("Success!")

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "id",
        help="ID of the string inside of the string.json file to target",
        type=int
    )

    parser.add_argument(
        "modified",
        help="string to replace the target with (including overflowing)"
    )

    args = parser.parse_args()

    main(args.id, args.modified)