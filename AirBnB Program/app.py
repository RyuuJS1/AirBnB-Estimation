import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
from PIL import Image
from fpdf import FPDF
from src.cleaning import LimpiezaProfunda

def create_pdf(df, title, lang_selected):
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Diccionario para elegir la fuente según el idioma seleccionado
    font_map = {
        "Español": "NotoSans-Regular.ttf",
        "English": "NotoSans-Regular.ttf",
        "Português": "NotoSans-Regular.ttf",
        "Русский": "NotoSans-Regular.ttf",
        "日本語": "NotoSansJP-Regular.ttf", 
        "中文": "NotoSansTC-Regular.ttf"
    }

    # Obtenemos el nombre del archivo. Si no está en el mapa, usamos la estándar por defecto.
    font_file = font_map.get(lang_selected, "NotoSans-Regular.ttf")
    font_path = os.path.join(ruta_base, 'assets', font_file)
    font_name = "DynamicFont" # Nombre interno para FPDF

    unicode_ready = False
    if os.path.exists(font_path):
        try:
            # Registramos la fuente específica
            pdf.add_font(font_name, '', font_path)
            pdf.set_font(font_name, '', 14)
            unicode_ready = True
        except Exception as e:
            st.error(f"Error al cargar la fuente {font_file}: {e}")
            pdf.set_font("Arial", "B", 14)
            font_name = "Arial"
    else:
        st.warning(f"No se encontró el archivo: {font_file} en la carpeta assets")
        pdf.set_font("Arial", "B", 14)
        font_name = "Arial"

    # --- CONSTRUCCIÓN DEL CONTENIDO DEL PDF ---
    # Título
    pdf.cell(190, 10, title, ln=True, align="C")
    pdf.ln(10)
    
    # Encabezados de tabla
    pdf.set_font(font_name, '', 10)
    cols = df.columns.tolist()
    ancho_celda = 190 / len(cols)
    
    for col in cols:
        pdf.cell(ancho_celda, 10, col, border=1)
    pdf.ln()
    
    # Filas de datos
    pdf.set_font(font_name, '', 9)
    for i in range(len(df)):
        for col in cols:
            val = str(df.iloc[i][col])
            # Si falló la carga de la fuente, limpiamos caracteres especiales para evitar errores
            if not unicode_ready:
                val = val.encode('ascii', 'ignore').decode('ascii')
            pdf.cell(ancho_celda, 10, val, border=1)
        pdf.ln()
        
    # Retornamos como bytes para el st.download_button
    return bytes(pdf.output())

# --- CONFIGURACIÓN PREVIA ---
ruta_base = os.path.dirname(__file__)
ruta_icono = os.path.join(ruta_base, 'assets', 'LogoAirBnB.jpg')

try:
    imagen_icono = Image.open(ruta_icono)
except FileNotFoundError:
    imagen_icono = "🏠"

st.set_page_config(page_title="Airbnb | Precios y Recomendaciones", page_icon=imagen_icono, layout="wide")

# --- DICCIONARIO DE IDIOMAS ---
texts = {
    "Español": {
        "mode_label": "Selecciona tu perfil",
        "host": "Anfitrión",
        "traveler": "Viajero",
        "title": "Estimación de Precios para Alojamientos",
        "info": "Las siguientes estimaciones son hechas con IA con datos proporcionados de AirBnB.",
        "host_header": "Características de la Propiedad",
        "btn_calc": "Calcular Precio Sugerido",
        "city": "Ciudad",
        "room_type": "Tipo de Habitación",
        "property_type": "Tipo de Propiedad",
        "district": "Distrito/Barrio",
        "people": "Cantidad de Personas",
        "bedrooms": "Número de habitaciones",
        "bathrooms": "Número de baños",
        "fee": "¿Cobras tarifa de limpieza?",
        "travel_header": "Planea tu viaje",
        "destination": "¿Cuáles ciudades te interesan?",
        "budget": "Presupuesto máximo por noche (USD)",
        "btn_search": "Buscar recomendaciones",
        "col_city": "Destino",
        "col_name": "Alojamiento",
        "col_price": "Precio por noche",
        "stay_dates": "Fechas de tu estancia",
        "min_rating": "Calificación mínima",
        "export": "Descargar recomendaciones (PDF)",
        "total_price": "Costo total",
        "market_comparison": "Comparativa de Mercado",
        "price_dist": "Distribución de precios en la zona"
    },
    "English": {
        "mode_label": "Select your profile",
        "host": "Host",
        "traveler": "Traveler",
        "title": "Price Estimation for Accommodations",
        "info": "The following estimates are made with AI using data provided by AirBnB.",
        "host_header": "Property Characteristics",
        "btn_calc": "Calculate Suggested Price",
        "city": "City",
        "room_type": "Room Type",
        "property_type": "Property Type",
        "district": "District/Neighborhood",
        "people": "Number of People",
        "bedrooms": "Number of bedrooms",
        "bathrooms": "Number of bathrooms",
        "fee": "Do you charge a cleaning fee?",
        "travel_header": "Plan your trip",
        "destination": "Which cities are you interested in?",
        "budget": "Maximum budget per night (USD)",
        "btn_search": "Search recommendations",
        "col_city": "Destination",
        "col_name": "Accommodation",
        "col_price": "Price per night",
        "stay_dates": "Stay dates",
        "min_rating": "Minimum rating",
        "export": "Download recommendations (PDF)",
        "total_price": "Total cost",
        "market_comparison": "Market Comparison",
        "price_dist": "Price distribution in the area"
    },
    "日本語": {
        "mode_label": "プロフィールを選択してください",
        "host": "ホスト",
        "traveler": "旅行者",
        "title": "宿泊施設の価格推定",
        "info": "以下の推定は、AirBnB提供のデータを使用してAIによって作成されています。",
        "host_header": "物件の特徴",
        "btn_calc": "推奨価格を計算する",
        "city": "都市",
        "room_type": "部屋タイプ",
        "property_type": "物件タイプ",
        "district": "地区/近隣",
        "people": "人数",
        "bedrooms": "寝室数",
        "bathrooms": "バスルーム数",
        "fee": "清掃料金を請求しますか？",
        "travel_header": "旅行を計画する",
        "destination": "どの都市に興味がありますか？",
        "budget": "1泊あたりの最大予算 (USD)",
        "btn_search": "おすすめを検索する",
        "col_city": "目的地",
        "col_name": "宿泊施設",
        "col_price": "1泊あたりの価格",
        "stay_dates": "滞在日",
        "min_rating": "最低評価",
        "export": "おすすめをダウンロード (PDF)",
        "total_price": "合計金額",
        "market_comparison": "市場比較",
        "price_dist": "このエリアの価格分布"
    },
    "中文": {
        "mode_label": "选择您的个人资料",
        "host": "房东",
        "traveler": "旅行者",
        "title": "住宿价格预测",
        "info": "以下预测是利用 AirBnB 提供的数据通过人工智能生成的。",
        "host_header": "房源特征",
        "btn_calc": "计算建议价格",
        "city": "城市",
        "room_type": "房间类型",
        "property_type": "房源类型",
        "district": "地区/街区",
        "people": "入住人数",
        "bedrooms": "卧室数量",
        "bathrooms": "浴室数量",
        "fee": "您是否收取清洁费？",
        "travel_header": "计划您的旅行",
        "destination": "您对哪些城市感兴趣？",
        "budget": "每晚最高预算 (USD)",
        "btn_search": "搜索推荐",
        "col_city": "目的地",
        "col_name": "房源名称",
        "col_price": "每晚价格",
        "stay_dates": "入住日期",
        "min_rating": "最低评分",
        "export": "下载推荐列表 (PDF)",
        "total_price": "总费用",
        "market_comparison": "市场比较",
        "price_dist": "该区域的价格分布"
    },
    "Русский": {
        "mode_label": "Выберите профиль",
        "host": "Хозяин",
        "traveler": "Путешественник",
        "title": "Оценка стоимости жилья",
        "info": "Следующие оценки сделаны с помощью ИИ на основе данных, предоставленных AirBnB.",
        "host_header": "Характеристики недвижимости",
        "btn_calc": "Рассчитать рекомендованную цену",
        "city": "Город",
        "room_type": "Тип жилья",
        "property_type": "Тип недвижимости",
        "district": "Район",
        "people": "Количество человек",
        "bedrooms": "Количество спален",
        "bathrooms": "Количество ванных комнат",
        "fee": "Взимаете ли вы плату за уборку?",
        "travel_header": "Планируйте свою поездку",
        "destination": "Какие города вас интересуют?",
        "budget": "Максимальный бюджет за ночь (USD)",
        "btn_search": "Найти рекомендации",
        "col_city": "Место назначения",
        "col_name": "Жилье",
        "col_price": "Цена за ночь",
        "stay_dates": "Даты поездки",
        "min_rating": "Минимальный рейтинг",
        "export": "Скачать рекомендации (CSV)",
        "total_price": "Общая стоимость",
        "market_comparison": "Сравнение с рынком",
        "price_dist": "Распределение цен в этом районе"
    },
    "Português": {
        "mode_label": "Selecione seu perfil",
        "host": "Anfitrião",
        "traveler": "Viajante",
        "title": "Estimativa de Preços para Acomodações",
        "info": "As seguintes estimativas são feitas com IA usando dados fornecidos pelo AirBnB.",
        "host_header": "Características da Propriedade",
        "btn_calc": "Calcular Preço Sugerido",
        "city": "Cidade",
        "room_type": "Tipo de Quarto",
        "property_type": "Tipo de Propriedade",
        "district": "Distrito/Bairro",
        "people": "Quantidade de Pessoas",
        "bedrooms": "Número de quartos",
        "bathrooms": "Número de banheiros",
        "fee": "Você cobra taxa de limpeza?",
        "travel_header": "Planeje sua viagem",
        "destination": "Quais cidades te interessam?",
        "budget": "Orçamento máximo por noite (USD)",
        "btn_search": "Buscar recomendações",
        "col_city": "Destino",
        "col_name": "Acomodação",
        "col_price": "Preço por noite",
        "stay_dates": "Datas da estadia",
        "min_rating": "Classificação mínima",
        "export": "Baixar recomendações (PDF)",
        "total_price": "Custo total",
        "market_comparison": "Comparação de Mercado",
        "price_dist": "Distribuição de preços na área"
    }
}

# --- BARRA LATERAL (CONFIGURACIÓN GLOBAL) ---
st.sidebar.title("Configuración / Settings")
lang = st.sidebar.selectbox("Idioma / Language", ["Español", "Português", "English", "Русский", "日本語", "中文"])
t = texts[lang]

perfil = st.sidebar.radio(t["mode_label"], [t["host"], t["traveler"]])

# --- CARGA DE MODELO ---
@st.cache_resource
def cargar_modelo():
    ruta_modelo = os.path.join(ruta_base, 'models', 'modelo_airbnb.joblib')
    if os.path.exists(ruta_modelo):
        return joblib.load(ruta_modelo)
    return None

recursos = cargar_modelo()

# --- INTERFAZ DINÁMICA ---

# Diccionario de ciudades y sus distritos principales
ubicaciones = {
    "New York": [
        "Alphabet City", "Astoria", "Arrochar", "Allerton", "Annadale", "Bath Beach", "Battery Park City", "Bay Ridge", 
        "Baychester", "Bayside", "Bedford Park", "Bedford-Stuyvesant", "Bensonhurst", "Bergen Beach", "Boerum Hill", 
        "Borough Park", "Brighton Beach", "Bronxdale", "Brooklyn", "Brooklyn Heights", "Brooklyn Navy Yard", "Brownsville", 
        "Bushwick", "Canarsie", "Carroll Gardens", "Castle Hill ", "Castleton Corners", "Chelsea", "Chinatown", "City Island", 
        "Clifton", "Clinton Hill", "Co-op City", "Cobble Hill", "College Point", "Columbia Street Waterfront", "Concourse", 
        "Concourse Village", "Coney Island", "Corona", "Country Club", "Crotona", "Crown Heights", "DUMBO", "Ditmars / Steinway", 
        "Dongan Hills", "Downtown Brooklyn", "Dyker Heights", "East Elmhurst", "East Flatbush", "East Harlem", "East New York", 
        "East Village", "Eastchester", "Edenwald", "Elm Park", "Elmhurst", "Eltingville", "Emerson Hill", "Financial District", 
        "Flatbush", "Flatiron District", "Flatlands", "Flushing", "Fordham", "Forest Hills", "Fort Greene", "Fort Wadsworth", 
        "Fresh Meadows", "Gerritsen Beach", "Gowanus", "Gramercy Park", "Graniteville", "Grant City", "Grasmere", "Gravesend", 
        "Great Kills", "Greenpoint", "Greenwich Village", "Greenwood Heights", "Grymes Hill", "Hamilton Heights", "Harlem", 
        "Hell's Kitchen", "Highbridge", "Howard Beach", "Hudson Square", "Huguenot", "Hunts Point", "Inwood", "Jackson Heights", 
        "Jamaica", "Kensington", "Kew Garden Hills", "Kingsbridge", "Kingsbridge Heights", "Kips Bay", "Lefferts Garden", 
        "Lighthouse HIll", "Lindenwood", "Little Italy", "Long Island City", "Lower East Side", "Manhattan", "Manhattan Beach", 
        "Marble Hill", "Marine Park", "Mariners Harbor", "Maspeth", "Meiers Corners", "Melrose", "Middle Village", 
        "Midland Beach", "Midtown", "Midtown East", "Midwood", "Mill Basin", "Morningside Heights", "Morris Heights", 
        "Morris Park", "Morrisania", "Mott Haven", "Mount Eden", "Murray Hill", "Navy Yard", "New Brighton", "New Dorp Beach", 
        "New Springville", "Noho", "Nolita", "Norwood", "Ozone Park", "Park Slope", "Park Versailles", "Parkchester", 
        "Pelham Bay", "Port Morris", "Port Richmond", "Prospect Heights", "Queens", "Randall Manor", "Red Hook", "Rego Park", 
        "Richmond Hill", "Ridgewood", "Riverdale", "Roosevelt Island", "Rosebank", "Rossville", "Sea Gate", "Sheepshead Bay", 
        "Soho", "Soundview", "South Beach", "South Ozone Park", "South Street Seaport", "Spuyten Duyvil", "St. George", 
        "Stapleton", "Sunnyside", "Sunset Park", "The Bronx", "The Rockaways", "Theater District", "Throgs Neck", 
        "Times Square/Theatre District", "Todt Hill", "Tompkinsville", "Tottenville", "Tremont", "Tribeca", "Upper East Side", 
        "Upper West Side", "Utopia", "Van Nest", "Vinegar Hill", "Wakefield", "Washington Heights", "West Brighton", 
        "West Farms", "West Village", "Westchester Village", "Westerleigh", "Whitestone", "Williamsbridge", "Williamsburg", 
        "Windsor Terrace", "Woodhaven", "Woodside"
    ],
    "Los Angeles": [
        "Alhambra", "Alondra Park", "Altadena", "Arcadia", "Arleta", "Artesia", "Arts District", "Atwater Village", "Azusa", 
        "Baldwin Hills", "Baldwin Park", "Bel Air/Beverly Crest", "Bell", "Bellflower", "Beverly Hills", "Boyle Heights", 
        "Bradbury", "Brentwood", "Burbank", "Cahuenga Pass", "Canoga Park", "Carson", "Cerritos", "Chatsworth", "Claremont", 
        "Commerce", "Compton", "Covina", "Culver City", "Cypress Park", "Del Rey", "Downey", "Downtown", "Duarte", "Eagle Rock", 
        "East Hollywood", "East Los Angeles", "East San Gabriel", "Echo Park", "El Monte", "El Segundo", "El Sereno", "Encino", 
        "Elysian Valley", "Florence-Graham", "Gardena", "Glassell Park", "Glendale", "Glendora", "Granada Hills North", 
        "Harbor City", "Harbor Gateway", "Hawaiian Gardens", "Hawthorne", "Hermon", "Hermosa Beach", "Highland Park", 
        "Hollywood", "Hollywood Hills", "Huntington Park", "Inglewood", "Irwindale", "La Canada Flintridge", 
        "La Crescenta-Montrose", "La Habra", "La Mirada", "La Puente", "Lake Balboa", "Lakewood", "Langdon", "Laurel Canyon", 
        "Lawndale", "Lincoln Heights", "Lomita", "Long Beach", "Los Feliz", "Lynwood", "Malibu", "Manhattan Beach", "Mar Vista", 
        "Marina Del Rey", "Mid-City", "Mid-Wilshire", "Mission Hills", "Monrovia", "Montebello", "Montecito Heights", 
        "Monterey Hills", "Monterey Park", "Mount Washington", "North Hills East", "North Hills West", "North Hollywood", 
        "Northridge", "Norwalk", "Pacific Palisades", "Pacoima", "Palms", "Palos Verdes", "Panorama City", "Paramount", 
        "Pasadena", "Pico Rivera", "Porter Ranch", "Rancho Palos Verdes", "Redondo Beach", "Reseda", "Rolling Hills", 
        "Rolling Hills Estates", "San Gabriel", "San Marino", "San Pedro", "Santa Fe Springs", "Santa Monica", "Sherman Oaks", 
        "Sierra Madre", "Signal Hill", "Silver Lake", "Skid Row", "South El Monte", "South Gate", "South LA", "South Pasadena", 
        "South Robertson", "South San Gabriel", "South Whittier", "Studio City", "Sun Valley", "Sunland/Tujunga", "Sylmar", 
        "Tarzana", "Temple City", "Toluca Lake", "Topanga", "Torrance", "University Heights", "Valley Glen", "Valley Village", 
        "Van Nuys", "Venice", "Vernon", "Watts", "West Adams", "West Athens", "West Covina", "West Hills", "West Hollywood", 
        "West Los Angeles", "West Puente Valley", "Westchester/Playa Del Rey", "Westlake", "Westmont", "Westside", "Westwood", 
        "Whittier", "Willowbrook", "Wilmington", "Winnetka", "Woodland Hills/Warner Center"
    ],
    "San Francisco": [
        "Alamo Square", "Balboa Terrace", "Bayview", "Bernal Heights", "Civic Center", "Cole Valley", "Cow Hollow", 
        "Crocker Amazon", "Diamond Heights", "Dogpatch", "Duboce Triangle", "Excelsior", "Fisherman's Wharf", "Forest Hill", 
        "Glen Park", "Haight-Ashbury", "Hayes Valley", "Ingleside", "Inner Sunset", "Japantown", "Lakeshore", "Lower Haight", 
        "Marina", "Mission Bay", "Mission District", "Mission Terrace", "Nob Hill", "Noe Valley", "North Beach", "Oceanview", 
        "Outer Sunset", "Pacific Heights", "Potrero Hill", "Presidio", "Presidio Heights", "Richmond District", "Russian Hill", 
        "Sea Cliff", "SoMa", "South Beach", "The Castro", "Twin Peaks", "Visitacion Valley", "Western Addition/NOPA", "West Portal"
    ],
    "Chicago": [
        "Albany Park", "Andersonville", "Archer Heights", "Armour Square", "Ashburn", "Auburn Gresham", "Austin", "Avondale", 
        "Back of the Yards", "Belmont Cragin", "Beverly", "Boystown", "Bridgeport", "Brighton Park", "Bronzeville", "Bucktown", 
        "Chatham", "Chinatown", "Clearing", "Dunning", "East Side", "Edgewater", "Edison Park", "Englewood", "Galewood", 
        "Garfield Park", "Garfield Ridge", "Gold Coast", "Grand Crossing", "Humboldt Park", "Hyde Park", "Irving Park", 
        "Jefferson Park", "Kenwood", "Lakeview", "Lincoln Park", "Lincoln Square", "Little Italy/UIC", "Little Village", 
        "Logan Square", "Loop", "Magnificent Mile", "McKinley Park", "Montclare", "Morgan Park", "Mount Greenwood", 
        "Near North Side", "Near West Side", "North Center", "North Park", "Norwood Park", "O'Hare", "Oakland", "Old Town", 
        "Pilsen", "Portage Park", "Printers Row", "Pullman", "River North", "River West", "Rogers Park", "Roseland", 
        "South Chicago", "South Loop/Printers Row", "South Shore", "Streeterville", "Ukrainian Village", "Uptown", 
        "Washington Park", "West Elsdon", "West Lawn", "West Loop/Greektown", "West Ridge", "West Town", "Wicker Park", 
        "Woodlawn", "Wrigleyville"
    ],
    "Washington D.C.": [
        "16th Street Heights", "Adams Morgan", "American University Park", "Anacostia", "Arboretum", "Barney Circle", 
        "Barry Farm", "Bellevue", "Benning", "Benning Heights", "Benning Ridge", "Berkley", "Bloomingdale", "Brightwood", 
        "Brookland", "Burleith", "Capitol Hill", "Carver Langston", "Cathedral Heights", 
        "Central Northeast/Mahaning Heights", "Chevy Chase", "Cleveland Park", "Colonial Village", "Columbia Heights", 
        "Congress Heights", "Crestwood", "Deanwood", "Douglass", "Downtown/Penn Quarter", "Dupont Circle", "Dupont Park", 
        "Eastland Gardens", "Eckington", "Edgewood", "Fairlawn", "Foggy Bottom", "Fort Davis", "Fort Dupont", "Fort Lincoln", 
        "Fort Totten", "Foxhall", "Friendship Heights", "Gallaudet", "Garfield Heights", "Gateway", "Georgetown", "Glover Park", 
        "Good Hope", "Greenway", "Hillbrook", "Hillcrest", "Ivy City", "Judiciary Square", "Kalorama", "Kent", "Kingman Park", 
        "Lamond Riggs", "LeDroit Park", "Logan Circle", "Manor Park", "Marshall Heights", "Massachusetts Heights", 
        "Michigan Park", "Mount Pleasant", "Mount Vernon Square", "Mt. Pleasant", "Mt. Vernon Square", "Naylor Gardens", 
        "Near Northeast", "Near Northeast/H Street Corridor", "North Cleveland Park", "North Michigan Park", 
        "Observatory Circle", "Old Soldiers' Home", "Palisades", "Park View", "Petworth", "Pleasant Plains", "Randle Highlands", 
        "River Terrace", "Shaw", "Shepherd Park", "Shipley Terrace", "Skyland", "Southwest Waterfront", "Spring Valley", 
        "St. Elizabeths", "Stronghold", "Takoma", "Trinidad", "Truxton Circle", "Twining", "U Street Corridor", "Wesley Heights", 
        "West End", "Woodland", "Woodley Park", "Woodridge"
    ],
    "Boston": [
        "Allston-Brighton", "Back Bay", "Beacon Hill", "Brookline", "Cambridge", "Charlestown", "Chestnut Hill", 
        "Downtown Crossing", "Dorchester", "East Boston", "Fenway/Kenmore", "Government Center", "Hyde Park", "Jamaica Plain", 
        "Leather District", "Mattapan", "Mission Hill", "North End", "Roslindale", "Roxbury", "South Boston", "South End", 
        "West End", "West Roxbury"
    ]
}

# OPCIÓN 1: ANFITRIÓN (PREDICCIÓN)
if perfil == t["host"]:
    st.title(f"{t['title']}")
    st.info(f"{t['info']}")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader(t["host_header"])
        
        city = st.selectbox(t["city"], list(ubicaciones.keys()))
        district = st.selectbox(t["district"], ubicaciones[city])
        acc = st.slider(t["people"], 1, 16, 2)
        beds = st.number_input("Número de camas", min_value=1, max_value=16, step=1)
        bedrooms = st.number_input(t["bedrooms"], min_value=1, max_value=10, step=1)
        baths = st.number_input(t["bathrooms"], min_value=1.0, max_value=8.0, step=0.5)
        n_amenities = st.number_input("Cantidad de servicios", min_value=1, max_value=60, value=10)
        fee = st.checkbox(t["fee"])

        with col2:
            st.write("###") 
            if st.button(t["btn_calc"]):
                if recursos:
                    modelo = recursos['modelo']
                    # Recuperamos la lista de todas las columnas que el modelo espera
                    todas_las_features = recursos['features'] 
                    
                    # 1. Creamos un DataFrame inicial de ceros con TODAS las columnas del entrenamiento
                    input_data = pd.DataFrame(0, index=[0], columns=todas_las_features)
                    
                    # 2. Llenamos los datos numéricos que sí tenemos
                    input_data['accommodates'] = acc
                    input_data['bedrooms'] = bedrooms
                    input_data['beds'] = beds
                    input_data['bathrooms'] = baths
                    input_data['n_amenities'] = n_amenities
                    
                    # 3. Activamos (One-Hot Encoding manual) el barrio y la ciudad
                    # IMPORTANTE: El nombre debe coincidir EXACTAMENTE con como estaba en el CSV original
                    if district in todas_las_features:
                        input_data[district] = 1
                    
                    if city in todas_las_features:
                        input_data[city] = 1

                    # 4. Predicción
                    try:
                        log_precio = modelo.predict(input_data)[0]
                        precio_real = np.exp(log_precio)
                        precio_final = max(20.0, precio_real)
                        
                        st.metric(label=t["btn_calc"], value=f"${precio_final:,.2f} USD")
                        st.success("Análisis completado con éxito.")
                        
                        # Gráfico
                        chart_data = pd.DataFrame({
                            'Precios': [precio_final, precio_final * 0.85, precio_final * 1.15], 
                            'Categoría': ['Tu Propuesta', 'Económico', 'Premium']
                        })
                        st.bar_chart(chart_data, x='Categoría', y='Precios')
                    except Exception as e:
                        st.error(f"Error en la predicción: {e}")
                else:
                    st.error("Modelo no encontrado.")

# OPCIÓN 2: VIAJERO (RECOMENDACIONES)
else:
    st.title(f"{t['traveler']}")
    
    with st.expander(t["travel_header"], expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            destinos_seleccionados = st.multiselect(t["destination"], list(ubicaciones.keys()), default=["New York"])
        with c2:
            rango_fechas = st.date_input(t["stay_dates"], value=(pd.Timestamp.now(), pd.Timestamp.now() + pd.Timedelta(days=1)))
        with c3:
            presupuesto = st.number_input(t["budget"], min_value=10, value=150)
        
        rating = st.slider(t["min_rating"], 1.0, 5.0, 4.0, step=0.1)

        coords_ciudades = {
            "New York": [40.7128, -74.0060],
            "Los Angeles": [34.0522, -118.2437],
            "San Francisco": [37.7749, -122.4194],
            "Chicago": [41.8781, -87.6298],
            "Miami": [25.7617, -80.1918]
        }

        if st.button(t["btn_search"]):
            if isinstance(rango_fechas, tuple) and len(rango_fechas) == 2:
                fecha_inicio, fecha_fin = rango_fechas
                noches = (fecha_fin - fecha_inicio).days
                
                if noches <= 0:
                    st.error("La fecha de salida debe ser posterior a la de entrada.")
                else:
                    st.write(f"### {t['traveler']} - {noches} noches")

                    import numpy as np # Para generar dispersión
                    
                    datos_viaje = []
                    for ciudad in destinos_seleccionados:
                        centro = coords_ciudades.get(ciudad, [40.7, -74.0])
                        
                        # Generamos 10 puntos aleatorios por cada ciudad seleccionada
                        for i in range(10):
                            precio_noche = presupuesto * (0.5 + np.random.rand() * 0.5)
                            # Dispersión aleatoria para que no se encimen los puntos
                            lat_random = centro[0] + (np.random.rand() - 0.5) * 0.1
                            lon_random = centro[1] + (np.random.rand() - 0.5) * 0.1
                            
                            datos_viaje.append({
                                t["col_city"]: ciudad,
                                t["col_name"]: f"Alojamiento {i+1} en {ciudad}",
                                t["col_price"]: f"${precio_noche:.2f}",
                                t["total_price"]: f"${precio_noche * noches:.2f}",
                                "lat": lat_random,
                                "lon": lon_random
                            })
                    
                    df_recos = pd.DataFrame(datos_viaje)

                    # --- MAPA MÁS PEQUEÑO ---
                    # Usamos columnas para reducir el ancho del mapa si lo deseas
                    col_mapa, col_espacio = st.columns([3, 1]) 
                    with col_mapa:
                        # height=300 hace que el mapa sea más bajito
                        st.map(df_recos, latitude='lat', longitude='lon', size=20, height=350)
                    
                    # --- TABLA DE RESULTADOS ---
                    st.dataframe(df_recos.drop(['lat', 'lon'], axis=1), use_container_width=True)
                    
                    # --- BOTÓN DE EXPORTACIÓN ---
                    df_pdf = df_recos.drop(['lat', 'lon'], axis=1)
                    titulo_pdf = f"{t['traveler']} - {noches} nights"
                    pdf_output = create_pdf(df_pdf, titulo_pdf, lang)

                    st.download_button(
                        label="📄 " + t["export"].replace("(CSV)", "(PDF)"),
                        data=pdf_output,
                        file_name='itinerario_airbnb.pdf',
                        mime='application/pdf'
                    )
            else:
                st.warning("Selecciona un rango completo de fechas.")