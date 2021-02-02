from scraping import Scraping

scrap = Scraping()

# Chamar a função definindo a UF
scrap.main('SP', scrap)

# Chamar a função para todas as UFs
scrap.main('', scrap)
