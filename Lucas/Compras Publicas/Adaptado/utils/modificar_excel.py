import os

def create_modified_excel(original_file):
    try:
        print("\nCriando novo arquivo Excel com modificações...")
        print("Lendo arquivo original...")
        
        # Extrai o número do processo do nome do arquivo
        filename = os.path.basename(original_file)
        process_number = filename.replace("ModeloPropostas", "").split("-")[0]
        
        # Lê o arquivo CSV com ponto e vírgula como separador
        with open(original_file, 'r', encoding='latin1') as f:
            lines = f.readlines()
            
        # Processa cada linha
        new_lines = []
        header = lines[0].strip()  # Mantém o cabeçalho original
        new_lines.append(header + '\n')
        
        # Processa cada linha de dados
        for line in lines[1:]:
            if not line.strip():  # Pula linhas vazias
                continue
                
            # Divide a linha em colunas
            columns = line.strip().split(';')
            
            # Encontra os índices das colunas
            header_cols = header.split(';')
            produto_idx = next(i for i, col in enumerate(header_cols) if "Produto (Não edite)" in col)
            descricao_idx = next(i for i, col in enumerate(header_cols) if "Descrição" in col)
            modelo_idx = next(i for i, col in enumerate(header_cols) if "Modelo" in col)
            marca_idx = next(i for i, col in enumerate(header_cols) if "Marca" in col)
            anvisa_idx = next(i for i, col in enumerate(header_cols) if "ANVISA" in col)
            quantidade_idx = next(i for i, col in enumerate(header_cols) if "Quantidade (Não edite)" in col)
            valor_unit_idx = next(i for i, col in enumerate(header_cols) if "Valor unitário" in col)
            valor_total_idx = next(i for i, col in enumerate(header_cols) if "Valor total" in col)
            
            # Preenche os valores vazios
            if len(columns) < len(header_cols):
                columns.extend([''] * (len(header_cols) - len(columns)))
                
            # Modelo
            if not columns[modelo_idx].strip():
                columns[modelo_idx] = 'modelo proprio'
                
            # Marca
            if not columns[marca_idx].strip():
                columns[marca_idx] = 'marca propria'
                
            # ANVISA
            if not columns[anvisa_idx].strip():
                columns[anvisa_idx] = '0'
                
            # Descrição
            if not columns[descricao_idx].strip():
                columns[descricao_idx] = columns[produto_idx]
                
            # Valor unitário
            if not columns[valor_unit_idx].strip():
                columns[valor_unit_idx] = '10000'
                
            # Valor total
            if not columns[valor_total_idx].strip():
                try:
                    quantidade = float(columns[quantidade_idx].replace(',', '.'))
                    valor_total = int(quantidade * 10000)
                    columns[valor_total_idx] = str(valor_total)
                except:
                    columns[valor_total_idx] = ''
            
            # Junta as colunas de volta
            new_line = ';'.join(columns) + '\n'
            new_lines.append(new_line)
        
        # Salva o novo arquivo
        output_dir = os.path.dirname(original_file)
        new_filename = os.path.join(output_dir, f"ModeloPropostas{process_number}-1.csv")
        
        try:
            with open(new_filename, 'w', encoding='latin1', newline='') as f:
                f.writelines(new_lines)
            print(f"✓ Novo arquivo salvo como: {new_filename}")
            return True, new_filename
        except PermissionError as e:
            print(f"Erro ao salvar arquivo: {str(e)}")
            # Tenta salvar no diretório atual
            new_filename = f"ModeloPropostas{process_number}-1.csv"
            with open(new_filename, 'w', encoding='latin1', newline='') as f:
                f.writelines(new_lines)
            print(f"✓ Novo arquivo salvo como: {new_filename}")
            return True, new_filename
            
    except Exception as e:
        print(f"Erro ao modificar arquivo Excel:\n{str(e)}")
        return False, None

if __name__ == "__main__":
    file_path = r"D:\trabalho\AlcantaraMendes\PROJETO OPERACIONAL\portal-compras-publicas\portal-compras-publicas\downloads\ModeloPropostas357629-1.csv"
    create_modified_excel(file_path)