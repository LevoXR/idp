"""Load COVID case data from statw.txt file"""
from pathlib import Path


def load_covid_data():
    """Load COVID case data from statw.txt file"""
    covid_data = {}
    try:
        # Try to find statw.txt in the same directory as the app or parent directory
        current_dir = Path(__file__).parent.parent.parent
        file_path = current_dir / 'statw.txt'
        
        # If not found, try in desktop_app directory
        if not file_path.exists():
            file_path = Path(__file__).parent.parent / 'statw.txt'
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Skip header lines (first 2 lines)
                for line in lines[2:]:
                    line = line.strip()
                    # Skip empty lines and separator lines
                    if not line or '---' in line:
                        continue
                    # Parse the markdown table format
                    # Format: | State/UT | Cases |
                    parts = [p.strip() for p in line.split('|')]
                    # Filter out empty parts (markdown tables have empty first/last parts)
                    parts = [p for p in parts if p]
                    if len(parts) >= 2:
                        state = parts[0].strip()
                        # Remove commas from numbers and convert to int
                        cases_str = parts[1].strip().replace(',', '').replace(' ', '')
                        try:
                            cases = int(cases_str)
                            covid_data[state] = cases
                        except ValueError:
                            continue
    except Exception as e:
        print(f"Error loading COVID data: {e}")
    return covid_data


