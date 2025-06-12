from litellm import completion
import os
import json 
import re

os.environ["GEMINI_API_KEY"] = "AIzaSyA55HTNRf7S6FlabLZ2hAA5rCrkWBRYVdo"
# os.environ["GEMINI_API_KEY"] = "AIzaSyAKHidiUFFw0Qp5OsKYNuc01atZQUmm_5c"
# os.environ["GEMINI_API_KEY"] = "AIzaSyAUXdWiEMUUv6X_3uC2e4PvMCUF81VFt2s"

def translate_conversation(conversation_data):
    """
    Translate a conversation data sample from English to Vietnamese.
    
    Args:
        conversation_data (str): The conversation data to translate (should be a string representation of the data)
    
    Returns:
        str: The translated conversation content
    """
    response = completion(
        model="gemini/gemini-2.5-flash-preview-05-20", 
        messages=[{"role": "user", "content": f"""
You are an expert English to Vietnamese translator specializing in conversational AI and navigation systems.

**Task**: Translate the following structured conversation data from English to Vietnamese while preserving the JSON structure and maintaining natural Vietnamese expressions.

**Guidelines**:
1. Keep all keys, IDs, and technical identifiers unchanged. ("kg", "task", "ref_ents", "kg_tripe".)
2. Translate only human-readable text content ("responses", "history".)
3. Use natural Vietnamese conversational style
4. Preserve the meaning and tone of the original text
5. For location names and addresses, keep them as-is if they are proper nouns or specific locations, but translate any descriptive text around them.
6. Maintain the same JSON structure and formatting

**Input Data**:
```json
{conversation_data}
```

**Output**: Return only the translated JSON data without any additional text or explanations.
        """}]
    )
    
    # Extract JSON from the response
    content = response.choices[0].message.content
    
    # Remove markdown code blocks if present
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'```\s*$', '', content)
    content = content.strip()
    
    try:
        # Parse the JSON string to return a proper dict
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw content: {content}")
        return content  # Return raw string if JSON parsing fails

# Example usage:
if __name__ == "__main__":
    sample_conversation = "{'id': '1', 'kg': [['dish_parking', 'distance', '2_miles'], ['dish_parking', 'traffic_info', 'road_block_nearby'], ['dish_parking', 'poi_type', 'parking_garage'], ['dish_parking', 'address', '550_alester_ave'], ['stanford_oval_parking', 'distance', '6_miles'], ['stanford_oval_parking', 'traffic_info', 'no_traffic'], ['stanford_oval_parking', 'poi_type', 'parking_garage'], ['stanford_oval_parking', 'address', '610_amarillo_ave'], ['willows_market', 'distance', '4_miles'], ['willows_market', 'traffic_info', 'car_collision_nearby'], ['willows_market', 'poi_type', 'grocery_store'], ['willows_market', 'address', '409_bollard_st'], ['the_westin', 'distance', '2_miles'], ['the_westin', 'traffic_info', 'moderate_traffic'], ['the_westin', 'poi_type', 'rest_stop'], ['the_westin', 'address', '329_el_camino_real'], ['toms_house', 'distance', '1_miles'], ['toms_house', 'traffic_info', 'heavy_traffic'], ['toms_house', 'poi_type', 'friends_house'], ['toms_house', 'address', '580_van_ness_ave'], ['pizza_chicago', 'distance', '4_miles'], ['pizza_chicago', 'traffic_info', 'heavy_traffic'], ['pizza_chicago', 'poi_type', 'pizza_restaurant'], ['pizza_chicago', 'address', '915_arbol_dr'], ['valero', 'distance', '6_miles'], ['valero', 'traffic_info', 'car_collision_nearby'], ['valero', 'poi_type', 'gas_station'], ['valero', 'address', '200_alester_ave'], ['mandarin_roots', 'distance', '2_miles'], ['mandarin_roots', 'traffic_info', 'no_traffic'], ['mandarin_roots', 'poi_type', 'chinese_restaurant'], ['mandarin_roots', 'address', '271_springer_street']], 'task': 'navigate', 'response': 'the nearest parking_garage is dish_parking at 550_alester_ave would you like directions there ?', 'history': ['where s the nearest parking_garage'], 'ref_ents': ['parking_garage', '550_alester_ave', 'dish_parking'], 'kg_tripe': [['dish_parking', 'distance', '2_miles'], ['dish_parking', 'traffic_info', 'road_block_nearby'], ['dish_parking', 'poi_type', 'parking_garage'], ['dish_parking', 'address', '550_alester_ave']]}"
    
    translated_result = translate_conversation(sample_conversation)
    print(translated_result)