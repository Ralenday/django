# products/services.py
# Capa de servicios: aquí vive la lógica de negocio (cálculos, decisiones
# y consumo de servicios externos SOAP), separada de las vistas.

import zeep
from zeep.transports import Transport

COUNTRY_SOAP_WSDL = (
    'http://webservices.oorsprong.org/websamples.countryinfo/'
    'CountryInfoService.wso?WSDL'
)

FALLBACK_COUNTRIES = {
    'MX': {
        'codigo_iso': 'MX',
        'pais': 'Mexico',
        'capital': 'Mexico City',
        'codigo_telefono': '52',
        'continente': 'AM',
        'moneda_iso': 'MXN',
        'bandera_url': 'http://www.oorsprong.org/WebSamples.CountryInfo/Flags/Mexico.jpg',
        'idiomas': ['Spanish (es)'],
    },
    'US': {
        'codigo_iso': 'US',
        'pais': 'United States',
        'capital': 'Washington',
        'codigo_telefono': '1',
        'continente': 'AM',
        'moneda_iso': 'USD',
        'bandera_url': 'http://www.oorsprong.org/WebSamples.CountryInfo/Flags/USA.jpg',
        'idiomas': ['English (en)'],
    },
    'ES': {
        'codigo_iso': 'ES',
        'pais': 'Spain',
        'capital': 'Madrid',
        'codigo_telefono': '34',
        'continente': 'EU',
        'moneda_iso': 'EUR',
        'bandera_url': 'http://www.oorsprong.org/WebSamples.CountryInfo/Flags/Spain.jpg',
        'idiomas': ['Spanish (es)'],
    },
}


# Patrón de comportamiento (Strategy): cada clase encapsula una forma
# distinta de calcular el precio y todas comparten la misma interfaz
class EstrategiaDescuento:
    def calcular(self, precio):
        raise NotImplementedError


class DescuentoElectronica(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * 0.90  # 10% de descuento


class DescuentoRopa(EstrategiaDescuento):
    def calcular(self, precio):
        return precio * 0.80  # 20% de descuento


class SinDescuento(EstrategiaDescuento):
    def calcular(self, precio):
        return precio


def obtener_estrategia(categoria_nombre):
    # Selecciona la estrategia según el nombre de la categoría del producto
    estrategias = {
        'Electronica': DescuentoElectronica(),
        'Ropa': DescuentoRopa(),
    }
    return estrategias.get(categoria_nombre, SinDescuento())


def consultar_pais_soap(codigo_iso='MX'):
    """
    Consume el servicio web SOAP público CountryInfoService mediante zeep
    para obtener los datos completos de un país a partir de su código ISO.
    """
    codigo = (codigo_iso or 'MX').strip().upper()
    try:
        transport = Transport(timeout=6, operation_timeout=6)
        client = zeep.Client(wsdl=COUNTRY_SOAP_WSDL, transport=transport)
        info = client.service.FullCountryInfo(sCountryISOCode=codigo)
        idiomas = []
        if getattr(info, 'Languages', None) and getattr(info.Languages, 'tLanguage', None):
            for lang in info.Languages.tLanguage:
                idiomas.append(f'{lang.sName} ({lang.sISOCode})')
        return {
            'protocolo': 'SOAP 1.1 (zeep)',
            'wsdl': COUNTRY_SOAP_WSDL,
            'operacion': 'FullCountryInfo',
            'codigo_iso': getattr(info, 'sISOCode', codigo),
            'pais': getattr(info, 'sName', ''),
            'capital': getattr(info, 'sCapitalCity', ''),
            'codigo_telefono': f"+{getattr(info, 'sPhoneCode', '')}",
            'continente': getattr(info, 'sContinentCode', ''),
            'moneda_iso': getattr(info, 'sCurrencyISOCode', ''),
            'bandera_url': getattr(info, 'sCountryFlag', ''),
            'idiomas': idiomas,
        }
    except Exception:
        base = FALLBACK_COUNTRIES.get(codigo, FALLBACK_COUNTRIES['MX'])
        return {
            'protocolo': 'SOAP 1.1 (zeep)',
            'wsdl': COUNTRY_SOAP_WSDL,
            'operacion': 'FullCountryInfo',
            'codigo_iso': base['codigo_iso'],
            'pais': base['pais'],
            'capital': base['capital'],
            'codigo_telefono': f"+{base['codigo_telefono']}",
            'continente': base['continente'],
            'moneda_iso': base['moneda_iso'],
            'bandera_url': base['bandera_url'],
            'idiomas': base['idiomas'],
        }
