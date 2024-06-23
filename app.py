from flask import Flask, request, render_template_string
import os
import re

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Definir las palabras reservadas y símbolos
keywords = {'int', 'for', 'if', 'else', 'while', 'return', 'System', 'out', 'println', 'public', 'class', 'static', 'void', 'String','("HolaMundo");','String[]','args)','System.out.println'}
symbols = {';', '{', '}', '(', ')'}


# Función de análisis léxico
def lexical_analysis(code):
    result = []
    lines = code.split('\n')
    for line_number, line in enumerate(lines, start=1):
        index = 0
        while index < len(line):
            token_detected = False
            for keyword in keywords:
                if line[index:].startswith(keyword) and (index + len(keyword) == len(line) or not line[index + len(keyword)].isalnum()):
                    result.append((line_number, index, 'Palabra reservada', keyword))
                    index += len(keyword)
                    token_detected = True
                    break
            if token_detected:
                continue

            char = line[index]
            if char in symbols:
                tipo = 'Símbolo'
                result.append((line_number, index, tipo, char))
                index += 1
            elif char.isdigit():
                start_index = index
                while index < len(line) and line[index].isdigit():
                    index += 1
                result.append((line_number, start_index, 'Número', line[start_index:index]))
            elif char.isalpha() or char == '_':
                start_index = index
                while index < len(line) and (line[index].isalnum() or line[index] == '_'):
                    index += 1
                token = line[start_index:index]
                if token not in keywords:
                    if re.search(r'\d', token):
                        result.append((line_number, start_index, 'Error', f'Identificador inválido: {token}'))
                    else:
                        result.append((line_number, start_index, 'Identificador', token))
            else:
                index += 1
    return result

# Función de análisis sintáctico
def syntactic_analysis(code):
    result = []
    correct_keyword = 'System.out.println'
    lines = code.split('\n')
    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        if stripped_line.startswith('System.out.'):
            if stripped_line.startswith(correct_keyword):
                result.append((line_number, correct_keyword, True))
            else:
                result.append((line_number, stripped_line.split('(')[0], False))
        elif 'System' in stripped_line or '.out' in stripped_line:
            result.append((line_number, stripped_line.split('(')[0], False))
        elif 'public static void main' in stripped_line:
            main_pattern = r'public static void main\s*\(\s*String\s*\[\s*\]\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)'
            match = re.match(main_pattern, stripped_line)
            if match:
                parameter_name = match.group(1)
                if parameter_name != "args":
                    result.append((line_number, f'Parámetro del main incorrecto: {parameter_name}', False))
                else:
                    result.append((line_number, 'Método main', True))
            else:
                result.append((line_number, 'Método main', False))
        else:
            tokens = stripped_line.split()
            for token in tokens:
                if token in keywords:
                    result.append((line_number, token, True))
                elif any(keyword in token for keyword in keywords):
                    result.append((line_number, token, False))
                    break
    return result

# Función de análisis semántico
def semantic_analysis(code):
    result = []
    declared_classes = set()
    declared_methods = set()
    declared_variables = set()
    lines = code.split('\n')
    for line_number, line in enumerate(lines, start=1):
        stripped_line = line.strip()
        tokens = stripped_line.split()

        # Identificar clases declaradas
        if 'class' in tokens:
            class_name_index = tokens.index('class') + 1
            if class_name_index < len(tokens):
                declared_classes.add(tokens[class_name_index])
            else:
                result.append((line_number, 'Error: Falta la definición de la clase', False))

        # Identificar el método main y sus parámetros
        if 'public static void main' in stripped_line:
            main_pattern = r'public static void main\s*\(\s*String\s*\[\s*\]\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)'
            match = re.match(main_pattern, stripped_line)
            if match:
                declared_methods.add('main')
                declared_variables.add(match.group(1))
            else:
                result.append((line_number, 'Error: Método main mal definido', False))

        # Identificar variables declaradas
        if 'int' in tokens or 'String' in tokens:
            type_index = tokens.index('int') if 'int' in tokens else tokens.index('String')
            var_name_index = type_index + 1
            if var_name_index < len(tokens):
                declared_variables.add(tokens[var_name_index])
            else:
                result.append((line_number, 'Error: Falta el nombre de la variable', False))

        # Verificar uso de variables no declaradas
        for token in tokens:
            if token not in keywords and token not in symbols and token not in declared_classes and token not in declared_methods and token not in declared_variables:
                result.append((line_number, f'Error: Variable no declarada {token}', False))
            else:
                if token in symbols:
                    continue
                if 'System.out.println' in stripped_line:
                    declared_methods.add('System.out.println')
                if 'println' in stripped_line:
                    declared_methods.add('println')

    if not declared_classes:
        result.append((1, 'Error: Falta la definición de clase', False))
    if 'main' not in declared_methods:
        result.append((1, 'Error: Falta el método main', False))

    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    code = ""
    lexical_result = []
    syntactic_result = []
    semantic_result = []
    if request.method == 'POST':
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            with open(file_path, 'r') as f:
                code = f.read()
        elif 'code' in request.form and request.form['code'].strip() != '':
            code = request.form['code']
        else:
            return "No file selected or code provided"

        lexical_result = lexical_analysis(code)
        syntactic_result = syntactic_analysis(code)
        semantic_result = semantic_analysis(code)

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 20px;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            form {
                margin-bottom: 20px;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            label {
                display: block;
                margin-bottom: 10px;
                font-weight: bold;
                color: #333;
            }
            textarea, input[type="file"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            .table-container {
                overflow-x: auto;
            }
        </style>
        <title>Analizador Léxico, Sintáctico y Semántico</title>
    </head>
    <body>
        <h1>Analizador Léxico, Sintáctico y Semántico</h1>
        <form method="POST" enctype="multipart/form-data">
            <label for="file">Subir Archivo:</label>
            <input type="file" name="file"><br><br>
            <label for="code">O introducir código:</label>
            <textarea name="code" rows="10" cols="50">{{code}}</textarea><br>
            <input type="submit" value="Analizar">
        </form>
        
        {% if lexical_result %}
            <h2>Análisis Léxico</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Línea</th>
                            <th>Índice</th>
                            <th>Tipo</th>
                            <th>Token</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for line_number, index, tipo, token in lexical_result %}
                            <tr>
                                <td>{{ line_number }}</td>
                                <td>{{ index }}</td>
                                <td>{{ tipo }}</td>
                                <td>{{ token }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% endif %}
        
        {% if syntactic_result %}
            <h2>Análisis Sintáctico</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Línea</th>
                            <th>Token</th>
                            <th>Correcto</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for line_number, token, correct in syntactic_result %}
                            <tr>
                                <td>{{ line_number }}</td>
                                <td>{{ token }}</td>
                                <td>{{ 'Sí' if correct else 'No' }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% endif %}
        
        {% if semantic_result %}
            <h2>Análisis Semántico</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Línea</th>
                            <th>Error</th>
                            <th>Correcto</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for line_number, error, correct in semantic_result %}
                            <tr>
                                <td>{{ line_number }}</td>
                                <td>{{ error }}</td>
                                <td>{{ 'Sí' if correct else 'No' }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% endif %}
    </body>
    </html>
    """, code=code, lexical_result=lexical_result, syntactic_result=syntactic_result, semantic_result=semantic_result)

if __name__ == '__main__':
    app.run(debug=True)
