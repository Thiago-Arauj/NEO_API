import requests
import pandas as pd
import os
from dotenv import load_dotenv

def initial_filter(response):
    searchIgnore = ('links', 'nasa_jpl_url', 'sentry_data')
    secondSearch = ('estimated_diameter', 'close_approach_data')

    if response.status_code == 200:
        dictionaries = {}

        data = response.json()

        for date in data['near_earth_objects']:

            if '-' not in date:
                pass
            else:
                dictionaries[date] = []
                
                for item in data['near_earth_objects'][date]:
                    auxDict = {}
                    for key, value in item.items():
                        if key in searchIgnore:
                            pass
                        else:
                            if key in secondSearch:
                                match key:
                                    case 'estimated_diameter':
                                        auxDict[key] = value['kilometers']
                                    case 'close_approach_data':
                                        
                                        auxDict[key] = value[0]['close_approach_date_full']
                            else:
                                auxDict[key] = value
                
                    dictionaries[date].append(auxDict)
        
        sorted_dict = dict(sorted(dictionaries.items()))

        return sorted_dict

    else:
        return 'API error'

def toDataFrame(dictionaries, path):
    if type(dictionaries) == dict:
        with pd.ExcelWriter(path) as writer:
            for date, dic in dictionaries.items():

                if date in writer.sheets:
                    lastRow = writer.sheets[date].max_row
                else:
                    lastRow = 0
                helper = pd.DataFrame(dic)
                helper.to_excel(writer, sheet_name=date, index=False, startrow=lastRow, header=lastRow==0)
    
    else:
        print(dictionaries)

def pathCorrecting(init_path, name):
    path = init_path.replace("\ ", "/")
    path += f"/{name}.xlsx"
    return path

def main():
    load_dotenv(".env")
    api_key = os.getenv("API-KEY")
    start_date = input("Selecione a data no modelo aaaa-mm-dd: ")
    end_date = input("Digite a data de fim no mesmo modelo: ") 
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}"

    response = requests.get(url)
    init_path = input("Cole aqui o caminho onde deseja que apareça o arquivo: ")
    name = input("Digite agora o nome do arquivo que deseja: ")
    path = pathCorrecting(init_path, name)

    toDataFrame(initial_filter(response), path)

main()
    