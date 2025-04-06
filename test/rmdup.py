import json


def remove_duplicates_from_json(input_file, output_file):
    try:
        # Load JSON data from the input file
        with open(input_file, "r") as infile:
            data = json.load(infile)

        if not isinstance(data, list):
            raise ValueError("The JSON file must contain a list of dictionaries.")

        # Remove duplicates by using frozenset to make dictionaries hashable
        unique_dicts = list({frozenset(item.items()): item for item in data}.values())

        # Save the cleaned data back to the output file
        with open(output_file, "w") as outfile:
            json.dump(unique_dicts, outfile, indent=4)

        print(f"Duplicates removed. Cleaned data saved to {output_file}.")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
input_file = "wyr_questions.json"
output_file = "output.json"
remove_duplicates_from_json(input_file, output_file)
