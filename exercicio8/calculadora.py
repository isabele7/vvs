import re

def add(numbers: str) -> int:
    if numbers == "":
        return 0

    delimiters = [",", "\n"]
    
    ## verificar se há delimitador no início da string
    if numbers.startswith("//"):
        header, numbers = numbers.split("\n", 1)
        header = header[2:]  

        if header.startswith("["):
            delimiters += re.findall(r"\[([^\]]+)\]", header)
        else:
            delimiters.append(header)
            
    ## criar regex para dividir os números usando os delimitadores
    pattern = "|".join(re.escape(d) for d in delimiters)
    parts = re.split(pattern, numbers)

    nums = [int(x) for x in parts]
    
    ## verificar se há números negativos
    negatives = [n for n in nums if n < 0]
    if negatives:
        raise ValueError(f"negativos não permitidos: {', '.join(str(n) for n in negatives)}")
    
    ## ignorar números maiores que 1000 na soma
    return sum(n for n in nums if n <= 1000)
