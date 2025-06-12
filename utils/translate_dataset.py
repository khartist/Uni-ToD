import json
import os
import time
from tqdm import tqdm
from translate import translate_conversation
import argparse

def translate_json_dataset(input_file, output_file, resume_from=None, batch_size=10):
    """
    Translate all conversation data points in a JSON file from English to Vietnamese.
    
    Args:
        input_file (str): Path to the input JSON file
        output_file (str): Path to save the translated JSON file
        resume_from (str): Key to resume translation from (useful for large datasets)
        batch_size (int): Number of conversations to process before saving checkpoint
    """
    
    # Load the input JSON file
    print(f"Loading data from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Load existing translated data if resuming
    translated_data = {}
    if resume_from and os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            translated_data = json.load(f)
        print(f"Resuming from existing file with {len(translated_data)} conversations...")
    
    # Get list of keys to process
    keys_to_process = list(data.keys())
    if resume_from:
        try:
            start_index = keys_to_process.index(resume_from)
            keys_to_process = keys_to_process[start_index:]
            print(f"Resuming from conversation {resume_from}")
        except ValueError:
            print(f"Resume key {resume_from} not found, starting from beginning")
    
    total_items = len(keys_to_process)
    print(f"Starting translation of {total_items} conversation samples...")
    
    # Process each conversation sample
    for i, key in enumerate(tqdm(keys_to_process, desc="Translating conversations")):
        try:
            # Skip if already translated
            if key in translated_data:
                continue
                
            conversation = data[key]
            
            # Convert the conversation to string format for translation
            conversation_str = json.dumps(conversation, ensure_ascii=False)
            
            # Translate the conversation
            translated_conversation = translate_conversation(conversation_str)
            
            # Add to translated data
            translated_data[key] = translated_conversation
            
            # Save checkpoint every batch_size conversations
            if (i + 1) % batch_size == 0:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(translated_data, f, ensure_ascii=False, indent=2)
                print(f"\nCheckpoint saved at conversation {key}")
            
            # Small delay to avoid hitting API rate limits
            time.sleep(0.5)
            
        except Exception as e:
            print(f"\nError translating conversation {key}: {e}")
            # Keep the original conversation if translation fails
            # translated_data[key] = conversation
            continue
    
    # Save the final translated data
    print(f"\nSaving final translated data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)
    
    print(f"Translation completed! {len(translated_data)} conversations saved.")

def main():
    parser = argparse.ArgumentParser(description='Translate conversation dataset from English to Vietnamese')
    parser.add_argument('--input', '-i', required=True, help='Input JSON file path')
    parser.add_argument('--output', '-o', required=True, help='Output JSON file path')
    parser.add_argument('--resume', '-r', help='Resume from specific conversation key')
    parser.add_argument('--batch-size', '-b', type=int, default=10, help='Batch size for checkpoints')
    
    args = parser.parse_args()
    
    # Translate the dataset
    translate_json_dataset(args.input, args.output, args.resume, args.batch_size)

if __name__ == "__main__":
    main()