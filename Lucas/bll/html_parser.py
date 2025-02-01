from bs4 import BeautifulSoup
import json
import re

def extract_form_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    form = soup.find('form', {'id': 'jsonForm1'})
    
    data = {
        'form_info': {
            'action': form.get('action'),
            'id': form.get('id'),
            'method': form.get('method')
        },
        'hidden_inputs': [],
        'header_info': {},
        'items': []
    }
    
    # Extract hidden inputs
    for hidden_input in form.find_all('input', {'type': 'hidden'}):
        data['hidden_inputs'].append({
            'name': hidden_input.get('name'),
            'id': hidden_input.get('id'),
            'value': hidden_input.get('value')
        })
    
    # Extract header information
    header_table = form.find('table', {'class': 'table-data'})
    if header_table:
        for row in header_table.find_all('tr'):
            for cell in row.find_all('td'):
                label = cell.find('label')
                if label:
                    key = label.text.strip().replace(':', '')
                    value = cell.find('b').text.strip() if cell.find('b') else ''
                    data['header_info'][key] = value
    
    # Extract items table
    items_table = form.find('table', {'class': 'table-striped'})
    if items_table:
        headers = [th.text.strip() for th in items_table.find_all('th')]
        
        for row in items_table.find_all('tr', {'id': re.compile(r'batchItemProp\d+')}):
            item = {}
            cells = row.find_all('td')
            
            # Extract basic information
            if len(cells) >= 5:
                item['lote'] = cells[0].text.strip()
                item['item'] = cells[1].text.strip()
                item['descricao'] = cells[2].text.strip()
                item['unidade'] = cells[3].text.strip()
                item['quantidade'] = cells[4].text.strip()
                item['valor_ref'] = cells[5].text.strip() if len(cells) > 5 else ''
            
            # Extract hidden input value
            hidden_input = row.find('input', {'type': 'hidden'})
            if hidden_input:
                item['id_item'] = hidden_input.get('value')
            
            data['items'].append(item)
    
    return data

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def parse_html_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    data = extract_form_data(html_content)
    save_to_json(data, output_file)
    return data

if __name__ == '__main__':
    # Exemplo de uso
    input_file = 'form.html'  # Arquivo HTML com o formulário
    output_file = 'form_data.json'  # Arquivo JSON de saída
    data = parse_html_file(input_file, output_file)
    print("Dados extraídos e salvos em", output_file)
