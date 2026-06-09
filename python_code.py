import pandas as pd
import re
from datetime import datetime

# ==========================================
# 1. FUNÇÕES AUXILIARES DE HIGIENIZAÇÃO
# ==========================================

def sanitize_date(val):
    """
    Normaliza a data para ISO YYYY-MM-DD. Retorna 'INVALID' se falhar.
    """
    if pd.isna(val):
        return 'INVALID'
    
    val_str = str(val).strip()
    
    # Lista de formatos comuns para tentar converter
    date_formats = [
        "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d",
        "%m/%d/%Y", "%m/%d/%y", "%m-%d-%y"
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(val_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
            
    # Tratamento para formatos textuais (Ex: "April 31st, 2024", "Jun 18th 2027")
    try:
        # Remove sufixos ordinais (st, nd, rd, th) de forma robusta
        clean_text = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', val_str, flags=re.IGNORECASE)
        # Tenta formatos com nomes de meses
        for text_fmt in ["%B %d, %Y", "%b %d %Y", "%d-%m-%Y"]: 
            try:
                return datetime.strptime(clean_text, text_fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
    except Exception:
        pass

    return 'INVALID'

def sanitize_porsche_model(val):
    """
    Normaliza os modelos para Canonical Title Case.
    """
    if pd.isna(val):
        return 'INVALID'
    return str(val).strip().title()

def sanitize_model_year(val):
    """
    Converte anos em texto ou formatos errados para inteiros de 4 dígitos.
    Valores fora de 1990 a 2035 retornam 'INVALID'.
    """
    if pd.isna(val):
        return 'INVALID'
    
    val_str = str(val).strip().lower()
    
    # Dicionário simples para conversão textual comum
    text_years = {
        "twenty twenty two": 2022,
        "twenty twenty three": 2023,
        "twenty twenty four": 2024,
        "twenty twenty five": 2025,
        "twenty twenty six": 2026
    }
    
    if val_str in text_years:
        year = text_years[val_str]
    else:
        # Remove hífens ou espaços (ex: 20-24 -> 2024, 20 24 -> 2024)
        cleaned = re.sub(r'[- ]', '', val_str)
        try:
            year = int(cleaned)
        except ValueError:
            return 'INVALID'
            
    if 1990 <= year <= 2035:
        return str(year)
    return 'INVALID'

def sanitize_sale_price(val):
    """
    Normaliza para string decimal com duas casas (ex: 985000.00).
    """
    if pd.isna(val):
        return 'INVALID'
    
    val_str = str(val).strip().lower()
    
    # Tratamento de abreviações como 'k'
    multiplier = 1.0
    if 'k' in val_str:
        multiplier = 1000.0
        val_str = val_str.replace('k', '')
        
    # Remove símbolos de moedas, espaços e texto comum
    val_str = re.sub(r'[$\s,a-z_]', '', val_str)
    
    try:
        price = float(val_str) * multiplier
        return f"{price:.2f}"
    except ValueError:
        return 'INVALID'

def sanitize_vehicle_mileage(val):
    """
    Normaliza para milhas inteiras. Se contiver 'km', converte usando 1 km = 0.621371 milhas.
    """
    if pd.isna(val):
        return 'INVALID'
    
    val_str = str(val).strip().lower()
    
    # Casos de veículo novo
    if val_str in ['zero miles', 'new', '0 mi', 'new car', '0 miles']:
        return '0'
        
    is_km = 'km' in val_str
    
    # Extrai apenas os números e pontos decimais/vírgulas
    cleaned = re.sub(r'[^\d.]', '', val_str.replace(',', ''))
    
    try:
        value = float(cleaned)
        if is_km:
            value = value * 0.621371
        return str(round(value))
    except ValueError:
        return 'INVALID'

def sanitize_payment_method(val):
    """
    Mapeia para os rótulos controlados do Schema.
    """
    if pd.isna(val):
        return 'INVALID'
    
    val_str = str(val).strip().lower().replace('-', '').replace(' ', '')
    
    mapping = {
        'creditcard': 'Credit Card',
        'debitcard': 'Debit Card',
        'banktransfer': 'Bank Transfer',
        'wiretransfer': 'Wire Transfer',
        'financing': 'Financing',
        'financingplan': 'Financing',
        'lease': 'Lease',
        'cash': 'Cash',
        'achpayment': 'ACH Payment',
        'cryptopayment': 'Crypto Payment'
    }
    
    return mapping.get(val_str, str(val).strip().title())

def sanitize_city(val):
    """
    Converte o nome da cidade para Title Case, preservando pontuações conhecidas.
    """
    if pd.isna(val):
        return 'INVALID'
    return str(val).strip().title()

def sanitize_state(val):
    """
    Normaliza estados americanos para a sigla de duas letras USPS.
    """
    if pd.isna(val):
        return 'INVALID'
    
    state_str = str(val).strip().upper()
    
    us_states = {
        'CALIFORNIA': 'CA', 'NEW YORK': 'NY', 'TEXAS': 'TX', 'FLORIDA': 'FL',
        'COLORADO': 'CO', 'MASSACHUSETTS': 'MA', 'WASHINGTON': 'WA', 'NV': 'NV',
        'TX': 'TX', 'CA': 'CA', 'NY': 'NY', 'FL': 'FL', 'CO': 'CO', 'MA': 'MA', 
        'WA': 'WA', 'AZ': 'AZ', 'ARIZONA': 'AZ', 'ILLINOIS': 'IL', 'NC': 'NC'
    }
    
    return us_states.get(state_str, 'INVALID')

def sanitize_delivery_status(val):
    """
    Normaliza os status de entrega de acordo com a lista controlada.
    """
    if pd.isna(val):
        return 'INVALID'
    
    val_str = str(val).strip().lower().replace('!', '').replace('-', '').replace('.', '')
    
    mapping = {
        'delivered': 'Delivered',
        'deliverd': 'Delivered', # Correção do erro de digitação comum
        'pending': 'Pending',
        'intransit': 'In Transit',
        'cancelled': 'Cancelled',
        'awaitingdelivery': 'Awaiting Delivery',
        'awaitingpickup': 'Awaiting Pickup',
        'pendingapproval': 'Pending Approval',
        'pendingreview': 'Pending Review',
        'shipped': 'Shipped',
        'awaitingreview': 'Awaiting Review'
    }
    
    return mapping.get(val_str, 'INVALID')


# ==========================================
# 2. EXECUÇÃO DO PROCESSO DE HIGIENIZAÇÃO
# ==========================================

def run_sanitization_agent(input_file_path, output_file_path):
    # Carrega a amostragem de dados original
    df = pd.read_csv(input_file_path)
    
    # Dicionário mapeando as funções para cada nova coluna alvo
    sanitizers = {
        'sale_date': ('SaleDateSanitized', sanitize_date),
        'porsche_model': ('PorscheModelSanitized', sanitize_porsche_model),
        'model_year': ('ModelYearSanitized', sanitize_model_year),
        'sale_price': ('SalesPriceSanitized', sanitize_sale_price),
        'vehicle_mileage': ('VehicleMileageSanitized', sanitize_vehicle_mileage),
        'payment_method': ('PayMethodSanitized', sanitize_payment_method),
        'city': ('CitySanitized', sanitize_city),
        'state': ('StateSanitized', sanitize_state),
        'delivery_status': ('DeliveryStatusSanitized', sanitize_delivery_status)
    }
    
    # Processa e posiciona as colunas sanitizadas imediatamente após as originais
    for col_origem, (col_nova, func_higienizar) in sanitizers.items():
        if col_origem in df.columns:
            loc = df.columns.get_loc(col_origem) + 1
            df.insert(loc, col_nova, df[col_origem].apply(func_higienizar))
            
    # Salva o arquivo final tratado em um novo arquivo CSV
    df.to_csv(output_file_path, index=False)
    print(f"Higienização concluída com sucesso! Arquivo salvo em: {output_file_path}")

# Substitua pelos caminhos corretos do seu ambiente de execução
run_sanitization_agent('porchet_amostragem.csv', 'porchet_amostragem_tratado.csv')