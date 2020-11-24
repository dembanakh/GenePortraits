import requests
import xml.etree.ElementTree as ET


class NCBIAPI:

    @staticmethod
    def search(term: str) -> str:
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
        result = requests.get(url=url, params={'db': 'nuccore', 'term': term})
        if result.status_code == 200:
            root = ET.fromstring(result.text)
            count_node = root.find('Count')
            if count_node.text == '1':
                return root.find('IdList').find('Id').text
            raise Exception("esearch didn't responded with a single ID")
        else:
            raise Exception('esearch request error')

    @staticmethod
    def fetch(gene_id: str, parameters: str):
        url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
        params = {'db': 'nuccore', 'id': gene_id, 'rettype': 'fasta', 'retmode': 'text'}
        if parameters is not None:
            if parameters[0] == 'c':
                parameters = parameters[1:]
                params['strand'] = '2'
            else:
                params['strand'] = '1'
            if '-' in parameters:
                p_from, p_to = parameters.split('-')
                if p_from > p_to:
                    p_from, p_to = p_to, p_from
                params['from'] = str(p_from)
                params['to'] = str(p_to)
        result = requests.get(url=url, params=params)
        if result.status_code == 200:
            return result.text
        else:
            raise Exception('efetch request error')
