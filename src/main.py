def parse_osu_file(osu_file_path):
    notes = []
    try:
        with open(osu_file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file {osu_file_path} was not found.")
        return []
    
    hit_objects_section = False
    for line in lines:
        line = line.strip()
        if line.startswith('[HitObjects]'):
            hit_objects_section = True
            continue
        if hit_objects_section:
            if not line:
                break
            try:
                # osu! hit object format: x,y,time,type,hitSound,endTime:hitSample
                parts = line.split(',')
                x = int(parts[0])
                y = int(parts[1])
                time = int(parts[2])
                note_type = int(parts[3])
                
                # Determine Roblox lane from osu! x coordinate
                position = int(x // 128) + 1
                note_type_str = "hold" if note_type & 2 else "normal"
                
                # Optional: Handle duration for hold notes if specified
                duration = 0.5 if note_type & 2 else 0  # Default duration if not found
                if note_type & 2 and len(parts) > 5:
                    end_time = int(parts[5])
                    duration = (end_time - time) / 1000.0  # Convert to seconds
                
                notes.append({
                    'time': time / 1000.0,  # Convert to seconds
                    'position': position,
                    'type': note_type_str,
                    'duration': duration
                })
            except (ValueError, IndexError) as e:
                print(f"Error parsing line: {line}\n{e}")
    
    return notes

def generate_roblox_chart(notes, output_file_path):
    try:
        with open(output_file_path, 'w') as file:
            file.write("local Chart = {}\n\n")
            file.write("Chart.Notes = {\n")
            for i, note in enumerate(notes):
                trailing_comma = ',' if i < len(notes) - 1 else ''
                file.write(f"    {{time = {note['time']}, position = {note['position']}, type = '{note['type']}', duration = {note['duration']}}}{trailing_comma}\n")
            file.write("}\n\n")
            file.write("return Chart\n")
    except IOError:
        print(f"Error: Unable to write to file {output_file_path}.")

if __name__ == "__main__":
    osu_file_path = 'chart.osu'
    output_file_path = 'chart.lua'
    notes = parse_osu_file(osu_file_path)
    if notes:
        generate_roblox_chart(notes, output_file_path)
        print(f"Converted osu! chart to Roblox format: {output_file_path}")
