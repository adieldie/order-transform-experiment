import re
import unicodedata
from datetime import datetime

def formatar_info_edicao(p):
    history = p.get('productChangesHistory', [])
    if not history: return ""
    items = p.get('items', [])
    items_dict = {str(item.get('variantId')): item.get('name', 'Produto') for item in items if item}
    mudancas = []
    for h in history:
        orig_id = str(h.get('originalVariantId'))
        orig_qtd = h.get('originalQuantity')
        final_qtd = h.get('finalQuantity')
        nome = items_dict.get(orig_id, f"ID {orig_id}")
        mudancas.append(f"{nome}: {orig_qtd} -> {final_qtd}")
    return "Edição: " + " | ".join(mudancas)


def normalizar_texto(texto):
    if not texto: return ""
    try:
        nfkd = unicodedata.normalize('NFKD', texto)
        # Converte para minúsculas e remove acentos
        t = "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()
        # Remove APENAS palavras completas (com word boundaries), não letras isoladas
        palavras_remover = ["bairro", "loteamento", "residencial", "condominio", "pq"]
        for p in palavras_remover:
            # Remove a palavra apenas se for uma palavra completa, não parte de outra
            t = re.sub(r'\b' + p + r'\b', '', t)
        # Remove números e caracteres especiais para padronizar
        t = re.sub(r'\d+', '', t)  # Remove números
        t = re.sub(r'[^\w\s]', '', t)  # Remove caracteres especiais
        return t.strip()
    except: return texto.lower().strip()

def parse_data_pedido(data_str):
    if not data_str:
        return None
    if isinstance(data_str, datetime):
        return data_str
    try:
        s = str(data_str).strip()
        if s.endswith("Z"):
            s = s.replace("Z", "+00:00")
        
        # Parse com timezone info se tiver
        dt = datetime.fromisoformat(s)
        
        # Se tem timezone info (aware), converter de UTC para São Paulo (UTC-3)
        if dt.tzinfo is not None:
            # Subtrair 3 horas para converter de UTC para São Paulo
            from datetime import timezone, timedelta
            utc_tz = timezone.utc
            sp_tz = timezone(timedelta(hours=-3))
            
            # Converter para UTC primeiro, depois para São Paulo
            dt_utc = dt.astimezone(utc_tz)
            dt_sp = dt_utc.astimezone(sp_tz)
            
            # Retorna naive datetime (sem tz info) para ser salvo no Excel
            return dt_sp.replace(tzinfo=None)
        else:
            # Se não tem timezone, assumir que é UTC e converter para São Paulo
            from datetime import timezone, timedelta
            utc_tz = timezone.utc
            dt_with_tz = dt.replace(tzinfo=utc_tz)
            sp_tz = timezone(timedelta(hours=-3))
            dt_sp = dt_with_tz.astimezone(sp_tz)
            return dt_sp.replace(tzinfo=None)
    except Exception as e:
        try:
            return datetime.strptime(str(data_str).strip(), "%Y-%m-%dT%H:%M:%S.%f")
        except Exception:
            return None

def normalizar_bairro(texto):
    t = normalizar_texto(texto)
    t = re.sub(r'[^a-z0-9\s]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

