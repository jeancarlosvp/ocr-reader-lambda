import regex as re

def get_row(worksheet):
    '''
    Get last row from worksheet
    input: worksheet - worksheet object
    output: row - int
    '''
    row = len(worksheet.get('B1:B')) + 1
    return row

def get_data_bcp(result_list):
    '''
    Get data from BCP
    '''
    patterns = {
        "Total": re.compile(r"(?:[\/I])\s?(\d{1,3}(?:,?\d{3})*)(?:\.\d{2})"),
        "Numero tarjeta": re.compile(r"\*{3,}\d{3,4}$"),
        "Numero tarjeta": re.compile(r"DESDE"),
        "DNI": re.compile(r"MR CASH"),
        "Codigo de operacion": re.compile(r"DE OPERACION")
    }

    matches_dict = {
        "Banco": 1,
        "Total": None,    
    }

    for index in range(len(result_list)):
        for key, pattern in patterns.items():
            text = result_list[index]
            match = pattern.search(text)
            if match:
                if key == "Total" and matches_dict["Total"] is None:
                    total_str = match.group(0).replace("/", "").replace("I", "").replace(",", "")
                    matches_dict[key] = float(total_str)
                elif key == "Numero tarjeta":
                    four_last = result_list[index + 1][-4:]
                    matches_dict[key] = re.sub("\D", "", four_last)
                elif key == "DNI":
                    for item in result_list[index:index+3]:
                        eight_last = item[-8:]
                        if eight_last.isdigit():
                            matches_dict[key] = eight_last
                            break
                elif key == "Codigo de operacion":
                    operation_code = re.sub("\D", "", result_list[index + 1])
                    matches_dict[key] = operation_code
                break

    return matches_dict

def get_data_ibk(result_list):
    '''
    Get data from interbank
    input: result_list - list of values from easyocr
    output: matches_dict - dict with values
    '''
    patterns = {
        "Total": re.compile(r"(?:[\/I])\s?(\d{1,3}(?:,\d{3})*)(?:\.\d{2})"),  # Patrón para moneda S/
        "Numero tarjeta": re.compile(r"CUENTA CARGO.*\d{3,4}$"),
        "DNI": re.compile(r"DATOS"),
        "Codigo de operacion": re.compile(r"CODIGO DE\s+\d*\s*OPERACION.*")
    }

    matches_dict = {"Banco": 2}
    for text in result_list:
        for key, pattern in patterns.items():
            match = pattern.search(text)
            if match:
                if key == "Total":
                    total_str = match.group(0).replace("/", "").replace("I", "").replace(",", "")
                    matches_dict[key] = float(total_str)
                elif key == "Numero tarjeta":
                    matches_dict[key] = re.sub("\D", "", text[-4:])
                elif key == "DNI":
                    matches_dict[key] = text[-8:]
                elif key == "Codigo de operacion":
                    matches_dict[key] = re.findall(r'\d+', text[-28:])[0]
                break

    return matches_dict

def get_data_scotiabank(result_list):
    '''
    Get data from scotiabank
    '''
    patterns = {
        "Codigo de operacion": re.compile(r"NUMERO DE OPERACION"),
        "Numero tarjeta": re.compile(r'[*+]+ ?\d+$'),
        "Total": re.compile(r"(?:[\/I])\s?(\d{1,3}(?:,\d{3})*)(?:\.\d{2})"),  # Patrón para moneda S/
        "DNI": re.compile(r"DNI")
    }

    matches_dict = {"Banco": 4}
    for text in result_list:
        for key, pattern in patterns.items():
            match = pattern.search(text)
            if match:
                print(match)
                print(text)
                if key == "Codigo de operacion":
                    matches_dict[key] = re.sub("\D", "", text)
                elif key == "Numero tarjeta":
                    matches_dict[key] = re.sub("\D", "", text[-4:])
                elif key == "Total":
                    total_str = match.group(0).replace("/", "").replace("I", "").replace(",", "")
                    matches_dict[key] = float(total_str)
                elif key == "DNI":
                    matches_dict[key] = re.sub("\D", "", text)
                break

    return matches_dict

def get_data_banbif(result_list):
    '''
    Get data from banbif
    '''
    patterns = {
        "Total": re.compile(r"(?:[\/I])\s?(\d{1,3}(?:,\d{3})*)(?:\.\d{2})"),  # Patrón para moneda S/
        "DNI": re.compile(r"DOCUMENT")
    }

    matches_dict = {"Banco": 5}
    for text in result_list:
        for key, pattern in patterns.items():
            match = pattern.search(text)
            if match:
                if key == "Total":
                    total_str = match.group(0).replace("/", "").replace("I", "").replace(",", "")
                    matches_dict[key] = float(total_str)
                elif key == "DNI":
                    matches_dict[key] = re.sub("\D", "", text)
                break

    return matches_dict 

def get_data_bbva(result_list):
    '''
    Get data from bbva
    '''
    patterns = {
        "Total": re.compile(r"(?:[\/I])\s?(\d{1,3}(?:,\d{3})*)(?:\.\d{2})"),  # Patrón para moneda S/
        "Numero tarjeta": re.compile(r"TARJETA DE ORIGEN")
    }

    matches_dict = {"Banco": 3}
    for text in result_list:
        for key, pattern in patterns.items():
            match = pattern.search(text)
            if match:
                if key == "Total":
                    total_str = match.group(0).replace("/", "").replace("I", "").replace(",", "")
                    matches_dict[key] = float(total_str)
                elif key == "Numero tarjeta":
                    matches_dict[key] = re.sub("\D", "", text)
                break

    return matches_dict 