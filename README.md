# Web Scraping Python

## Instalação

Clonar o repositório e executar o comando:

```bash
pipenv install
```

## Usando

No arquivo main.py é chamada a classe Scraping e lá tem a chamada das funções para a realização do teste. Há duas maneiras de chama-las, você pode declarar uma UF e irá executar somente a extração dos dados daquela UF ou chamar com uma string vazia, onde vai trazer as informações de todas as UFs.
```python
scrap.main('SP', scrap) # retorna somente os dados de SP 
scrap.main('', scrap) # retorna os dados de todas as UFs
```

## Exemplo de retorno
```
Exemplo dos dados no arquivo SP.jsonl
```
