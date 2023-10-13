import os
import json
import csv
#librarys used :
# os lirary and json library to open folders and write on a json file
#csv library to map between the ids and the path on csv file

# Here, create a list of the most common words that can be dismissed (according to chatGPT)
stop_words = [
    "a", "an", "and", "the", "in", "on", " of ", "with", "he", "she", "it", "is", "at",
    "to", "for", "that", "as", "by", "from", "or"
]

def text_tokenizer(text):
    words = text.lower().split()
    words = [word.strip('.,?!:;()[]{}"\'') for word in words if word not in stop_words and len(word) >= 3]
    return words

def inverted_index_creator(file, document_id):
    inverted_index = {}
    input_file = open(file, 'r')
    position = 0

    for line in input_file:
        words = text_tokenizer(line)
        for word in words:
            if word not in inverted_index:
                inverted_index[word] = {document_id: [position]}
            else:
                if document_id not in inverted_index[word]:
                    inverted_index[word][document_id] = [position]
                else:
                    inverted_index[word][document_id].append(position)
            position += 1

    input_file.close()
    return inverted_index

def save_inverted_index_to_file(inverted_index, output_file):
    json_data = {}
    for word, data in inverted_index.items():
        json_data[word] = data

    json_file = open(output_file, 'w')
    json.dump(json_data, json_file, separators=(',', ': '))
    json_file.close()

def enter_data_from_files(input_folder, output_file):
    inverted_index = {}
    document_id_mapping = {}  
    document_id = 1

    for file in os.listdir(input_folder):
        input_file = os.path.join(input_folder, file)
        document_id_mapping[document_id] = input_file  
        index = inverted_index_creator(input_file, document_id)

        for word, positions in index.items():
            if word not in inverted_index:
                inverted_index[word] = positions
            else:
                for doc_id, doc_positions in positions.items():
                    if doc_id not in inverted_index[word]:
                        inverted_index[word][doc_id] = doc_positions
                    else:
                        inverted_index[word][doc_id] += doc_positions

        document_id += 1

    csv_file = open('docId_filePath_mapping.csv', 'w', newline='')
    fieldnames = ['Document id', 'File path']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for doc_id, file_path in document_id_mapping.items():
        writer.writerow({'Document id': doc_id, 'File path': file_path})

    csv_file.close()

    json_file = open(output_file, 'w')
    json_data = {}
    for word, data in inverted_index.items():
        json_data[word] = data
    json.dump(json_data, json_file, indent=2, separators=(',', ': '))
    json_file.close()

def search_query_in_files(query, input_folder):
    result_files = []

    for file in os.listdir(input_folder):
            input_file = open(os.path.join(input_folder, file), 'r')
            content = input_file.read()
            input_file.close()

            if query in content:
                result_files.append(file)

    return result_files

input_folder = "C://Users//USER//Desktop//folder_input"
output_file = "pos_inverted_index.json"
enter_data_from_files(input_folder, output_file)

user_query = input("please enter the required query: ")
found_files = search_query_in_files(user_query, input_folder)

if found_files:
    print(f"Query '{user_query}' is found in these files:")
    for file_name in found_files:
        print(file_name)
else:
    print(f"Query '{user_query}' not found.")
