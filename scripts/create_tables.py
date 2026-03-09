import os
import csv
import re
from pylatex import Tabularx, MultiColumn
from pylatex.utils import NoEscape

def to_snake_case(name):
    s1 = re.sub(r'[\s\-]+', '_', name)
    return s1.lower()

def process_csv(csv_file, output_dir):
    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    snake_name = to_snake_case(base_name)[8:]  # Remove 'Sheet n' prefix
    tex_file = os.path.join(output_dir, f"{snake_name}.tex")
    
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)
        
    table = Tabularx('l Y Y Y Y', width_argument=NoEscape(r'\textwidth'), width=5)
    
    table.append(NoEscape(r'\toprule' + '\n'))
    
    table.add_row([
        'Component', 
        MultiColumn(2, align='c', data='Values'),
        'Delta', 
        NoEscape(r'\% Error')
    ])

    table.add_row([
        '', 
        'Expected',
        'Measured',
        '', 
        ''
    ])
    
    table.append(NoEscape(r'\midrule' + '\n'))
    
    for row in rows:
        formatted_row = []
        for i, cell in enumerate(row):
            if i == 0:
                if '_' in cell:
                    formatted_row.append(NoEscape(f"${cell}$"))
                else:
                    formatted_row.append(cell)
            else:
                formatted_row.append(cell)
        table.add_row(formatted_row)
        
    table.append(NoEscape(r'\bottomrule' + '\n'))
    
    with open(tex_file, 'w') as f:
        f.write(table.dumps())
    print(f"Created {tex_file}")

def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory (workspace root)
    workspace_dir = os.path.dirname(script_dir)
    
    data_dir = os.path.join(workspace_dir, 'data')
    tables_dir = os.path.join(workspace_dir, 'tables')
    
    if not os.path.exists(tables_dir):
        os.makedirs(tables_dir)
        
    for filename in os.listdir(data_dir):
        if filename.endswith('.csv'):
            process_csv(os.path.join(data_dir, filename), tables_dir)

if __name__ == '__main__':
    main()
