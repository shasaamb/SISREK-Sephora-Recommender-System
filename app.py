import os
import time
import random
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

st.set_page_config(
    layout="wide",
    page_title="Sephora Indonesia",
    page_icon=".images/logo/logo-1.png", 
    initial_sidebar_state="collapsed",
)

hide_st_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

custom_layout_navbar_slideshow = """
<style>
div.stVerticalBlock, div.stHorizontalBlock {
    padding: 0;
    margin-top: 0;
}

div.block-container {
    padding-top: 0;
}

body {
    margin: 0;
    padding: 0;
}
</style>
"""
st.markdown(custom_layout_navbar_slideshow, unsafe_allow_html=True)

with open("styles.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="navbar">
        <div class="logo">
            <a class="logo">SEPHORA</a>
        </div>
        <a>Skincare</a>
        <a>Makeup</a>
        <a>Hair</a>
        <a>Fragrance</a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
        .card-container {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            padding: 20px;
        }

        .card {
            flex: 1;
            background-color: white;
            text-align: center;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
            overflow: hidden;
            padding: 15px;
            margin-bottom: 20px;

            min-height: 250px; 
            max-height: 400px; 
            display: flex;
            flex-direction: column; 
            justify-content: space-between; 
        }

        .card a {
            text-decoration: none;
            color: black;
        }

        .card h2 {
            font-family: "Georgia", sans-serif;
            color: black;
            font-size: 25px;
            font-weight: normal;
            margin: 10px 0 5px 0;
            padding: 10px 20px 20px 30px;
        }

        .card p {
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #555;
            margin: 0 0 15px 0;
            line-height: 1.5;
            padding: 10px 20px 20px 30px;
        }

        .shop-button {
            display: inline-block;
            text-decoration: none;
            color: black;
            font-weight: bold;
            border: 2px solid black;
            padding: 8px 16px;
            margin-bottom: 10px;
            border-radius: 4px;
            transition: all 0.3s ease;
        }

        .shop-button:hover {
            background-color: black;
            color: white;
        }

        .section-title {
            text-align: center;
            color: black;
            font-family: "Georgia", serif;
            font-size: 25px;
            font-weight: normal;
            margin-top: 20px;
            margin-bottom: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

with open("slideshow.html", "r") as f:
    html_code = f.read()
components.html(html_code, height=500, scrolling=False)

st.image(".images/member.png", use_container_width=True)

st.markdown('<div class="section-title">Belanja Brands</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6 = st.columns(6, gap="medium", vertical_alignment="center", border=True)
with col1:
    st.image(".images/section-brand/Content-1-SDJ.png", use_container_width=True)
with col2:
    st.image(".images/section-brand/Content-2-KC.png", use_container_width=True)
with col3:
    st.image(".images/section-brand/Content-3-D.png", use_container_width=True)
with col4:
    st.image(".images/section-brand/Content-4-YSL.png", use_container_width=True)
with col5:
    st.image(".images/section-brand/Content-5-TF.png", use_container_width=True)
with col6:
    st.image(".images/section-brand/Content-6-GHD.png", use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.image(".images/section-info/Content-1-GF.png", use_container_width=True)
    st.markdown(
        """
        <div class="card">
            <h2>Give Fragrance</h2>
            <p>Discover gifts for someone who loves smelling good from luxurious perfumes to refreshing body mists with curated scents for every mood and occasion.</p>
            <a class="shop-button">SHOP NOW</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.image(".images/section-info/Content-2-G.png", use_container_width=True)
    st.markdown(
        """
        <div class="card">
            <h2>GIVENCHY</h2>
            <p>Prisme Libre Setting & Finishing Loose Powder featuring captivating fragrances that last all day with a selection of timeless and trendy scents.</p>
            <a class="shop-button">SHOP THE BRAND</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.image(".images/section-info/Content-3-K.png", use_container_width=True)
    st.markdown(
        """
        <div class="card">
            <h2>KAYALI</h2>
            <p>Luxurious scent that will linger with sweet temptation with delightful aromas perfect for gifting or self-indulgence that bring elegance and charm.</p>
            <a class="shop-button">SHOP THE BRAND</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

brand_options = {
    "Skincare": ['-', 'Algenist', 'Alpha-H', 'alpyn beauty', 'Anastasia Beverly Hills', 'Augustinus Bader', 'bareMinerals', 'BeautyBio', 'belif', 'Benefit Cosmetics', 'Biossance', 'Bobbi Brown', 'Caudalie', 'CAY SKIN', 'Charlotte Tilbury', 'Clarins', 'CLINIQUE', 'Community Sixty-Six', 'COOLA', 'DAMDAM', 'Danessa Myricks Beauty', 'DERMAFLASH', 'Dermalogica', 'Dior', 'Dr. Barbara Sturm', 'Dr. Brandt Skincare', 'Dr. Dennis Gross Skincare', 'Dr. Jart+', 'Dr. Lara Devgan Scientific Beauty', 'Dr. Zenovia Skincare', 'Drunk Elephant', 'EADEM', 'Estée Lauder', 'Evian', 'FaceGym', 'Farmacy', 'Fenty Skin', 'First Aid Beauty', 'Flora + Bast', 'FOREO', 'Freck Beauty', 'fresh', 'GLO Science', 'Glossier', 'Glow Recipe', 'goop', 'Gucci', 'GUERLAIN', 'HABIT', 'Hanni', 'Herbivore', 'Hourglass', 'Hyper Skin', 'ILIA', 'INC.redible', 'iNNBEAUTY PROJECT', 'innisfree', 'Isle of Paradise', 'IT Cosmetics', 'Jack Black', 'JLo Beauty', 'Josie Maran', 'Kate McLeod', 'Kate Somerville', "Kiehl's Since 1851", 'Koh Gen Do', 'KORA Organics', 'KORRES', 'Kosas', "L'Occitane", 'La Mer', 'Lancôme', 'LANEIGE', 'LAWLESS', 'MACRENE actives', 'MAKE UP FOR EVER', 'MARA', 'Mario Badescu', 'MERIT', 'MILK MAKEUP', 'Moon Juice', 'Mount Lai', 'Murad', 'Naturally Serious', 'Nécessaire', 'NUDESTIX', 'NuFACE', 'OLEHENRIKSEN', 'ONE/SIZE by Patrick Starrr', 'Origins', "Paula's Choice", 'Peace Out', 'Peter Thomas Roth', 'Prima', 'PROVEN Skincare', 'RANAVAT', 'REN Clean Skincare', 'ROSE INC', 'ROSE Ingleton MD', 'Saie', 'Saint Jane Beauty', 'SEPHORA COLLECTION', 'Shani Darden Skin Care', 'Shiseido', 'SK-II', 'Skinfix', 'SOBEL SKIN Rx', 'Soleil Toujours', 'St. Tropez', 'StriVectin', 'Sulwhasoo', 'Summer Fridays', 'Sunday Riley', 'Supergoop!', 'tarte', 'Tata Harper', 'Tatcha', 'The INKEY List', 'The Nue Co.', 'The Ordinary', 'The Outset', 'Topicals', 'Tower 28 Beauty', 'TULA Skincare', 'Wander Beauty', 'WASO', 'Wishful', 'Youth To The People'],
    "Makeup": ['-', 'AERIN', 'Ami Colé', 'Anastasia Beverly Hills', 'Armani Beauty', 'Artist Couture', 'Augustinus Bader', 'bareMinerals', 'beautyblender', 'Benefit Cosmetics', 'Blinc', 'Bobbi Brown', 'Buxom', 'caliray', 'Charlotte Tilbury', 'Christian Louboutin', 'Cinema Secrets', 'Clarins', 'CLINIQUE', 'Danessa Myricks Beauty', 'Dermalogica', 'Dior', 'DOMINIQUE COSMETICS', 'Dr. Brandt Skincare', 'Dr. Jart+', 'Dr. Lara Devgan Scientific Beauty', 'DUO', 'Estée Lauder', 'Fashion Fair', 'Fenty Beauty by Rihanna', 'First Aid Beauty', 'Freck Beauty', 'fresh', 'Givenchy', 'Glamnetic', 'Glossier', 'Grande Cosmetics', 'Gucci', 'GUERLAIN', 'GXVE BY GWEN STEFANI', 'HAUS LABS BY LADY GAGA', 'Hourglass', 'House of Lashes', 'HUDA BEAUTY', 'Iconic London', 'ILIA', 'INC.redible', 'IT Cosmetics', 'Jo Malone London', 'Josie Maran', 'Jouer Cosmetics', 'Kaja', 'Koh Gen Do', 'Kosas', 'Kulfi', 'KVD Beauty', 'La Mer', 'Lancôme', 'LANEIGE', 'Laura Mercier', 'LAWLESS', 'lilah b.', 'Lilly Lashes', 'LYS Beauty', 'MAKE UP FOR EVER', 'MAKEUP BY MARIO', 'Melt Cosmetics', 'MERIT', 'MILK MAKEUP', 'NARS', 'Natasha Denona', 'NUDESTIX', 'OLEHENRIKSEN', 'ONE/SIZE by Patrick Starrr', 'Origins', 'PAT McGRATH LABS', 'PATRICK TA', 'Peter Thomas Roth', 'Rare Beauty by Selena Gomez', 'REFY', 'rms beauty', 'ROSE INC', 'Saie', 'SEPHORA COLLECTION', 'Shiseido', 'SIMIHAZE BEAUTY', 'Smashbox', 'Soleil Toujours', 'stila', 'StriVectin', 'Summer Fridays', 'Supergoop!', 'tarte', 'Tatcha', 'The Ordinary', 'The Original MakeUp Eraser', 'TOM FORD', 'Too Faced', 'Tower 28 Beauty', 'TULA Skincare', 'TWEEZERMAN', 'Urban Decay', 'Valentino', 'Vegamour', 'Velour Lashes', 'Violet Voss', 'Viseart', 'Wander Beauty', 'Westman Atelier', 'Yves Saint Laurent'],
    "Hair": ['-', 'adwoa beauty', 'ALTERNA Haircare', 'amika', 'Aquis', 'Augustinus Bader', 'BeautyBio', 'Bio Ionic', 'BondiBoost', 'BREAD BEAUTY SUPPLY', 'Briogeo', 'Bumble and bumble', 'Ceremonia', 'Christophe Robin', 'COLOR WOW', 'Crown Affair', 'Curlsmith', 'dae', 'Drunk Elephant', 'Drybar', 'Fable & Mane', 'First Aid Beauty', 'ghd', 'Gisou', 'Good Dye Young', 'goop', 'Grace Eleyae', 'GUERLAIN', 'HUM Nutrition', 'IGK', 'Jack Black', 'JVN', 'K18 Biomimetic Hairscience', 'Kérastase', "Kiehl's Since 1851", "L'Oreal Professionnel", 'Living Proof', 'Melanin Haircare', 'Mizani', 'Moon Juice', 'Moroccanoil', 'Nécessaire', 'Nutrafol', 'Olaplex', 'Oribe', 'OUAI', 'PATTERN by Tracee Ellis Ross', 'Pureology', 'RANAVAT', 'RIES', 'Rossano Ferretti Parma', 'SEPHORA COLLECTION', 'shu uemura', 'Slip', 'Sol de Janeiro', 'SUNDAY II SUNDAY', 'Sunday Riley', 'Susteau', 'T3', 'The INKEY List', 'The Nue Co.', 'The Ordinary', 'Vegamour', 'Verb', 'Viori', 'Virtue'],
    "Fragrance": ['-', '19-69', 'ABBOTT', 'Acqua di Parma', 'AERIN', 'Armani Beauty', 'Azzaro', 'BERDOUES', 'Bobbi Brown', 'Bon Parfumeur', 'Boy Smells', 'BURBERRY', 'By Rosie Jane', 'Calvin Klein', 'CANOPY', 'Capri Blue', 'Carolina Herrera', 'Ceremonia', 'CHANEL', 'Chloé', 'CLEAN RESERVE', 'CLINIQUE', 'Commodity', 'DedCool', 'DEREK LAM 10 CROSBY', 'Dior', 'Dolce&Gabbana', 'Donna Karan', 'Eight & Bob', 'Ellis Brooklyn', 'Fenty Beauty by Rihanna', 'Floral Street', 'FORVR Mood', 'Givenchy', 'Glossier', 'Gucci', 'GUERLAIN', 'HERETIC', 'HERMÈS', 'JIMMY CHOO', 'Jo Malone London', 'Juicy Couture', 'Juliette Has a Gun', 'KAYALI', 'KILIAN Paris', 'Lancôme', 'Maison Louis Marie', 'Maison Margiela', 'Marc Jacobs Fragrances', 'maude', 'Montblanc', 'Moroccanoil', 'Mugler', 'NEST New York', 'OTHERLAND', 'OUAI', 'Overose', 'Paco Rabanne', 'PHLUR', 'Prada', 'Ralph Lauren', 'SEPHORA COLLECTION', 'Sephora Favorites', 'SKYLAR', 'Sol de Janeiro', 'The 7 Virtues', 'The Phluid Project', 'TOCCA', 'TOM FORD', 'Valentino', 'Versace', 'Viktor&Rolf', 'VOLUSPA', 'World of Chris Collins', 'Yves Saint Laurent']
}

st.markdown('<div class="section-title">Direkomendasikan untuk Anda</div>', unsafe_allow_html=True)
personalized = False
col1, col2, col3 = st.columns([0.2, 0.5, 0.3])
with col1:
    primary_category = st.selectbox("Beauty Products", ["Skincare", "Makeup", "Hair", "Fragrance"])
with col3:
    if  primary_category != "Skincare":
        selected_options = st.multiselect(
            "Filter",
            ["On Sale", "New", "Limited Edition"], placeholder="Select a filter"
        )
    else:
        selected_options = st.multiselect(
            "Filter",
            ["On Sale", "New", "Limited Edition"], placeholder="Select a filter", disabled=True
        )

col1, col2 = st.columns([0.5, 0.5])
with col1:
    product_name = st.text_input("Product*", placeholder="Beauty Product", key="text_input_1")
with col2:
    brand_name = st.selectbox(
        "Brand",
        options=brand_options[primary_category], 
        placeholder="Choose a brand",
        index=None,
        key="brand_multiselect"
    )


col1, col2 = st.columns([0.5, 0.5])
with col1:
    if primary_category == "Skincare":
        personalized = st.checkbox("Personalized", value=False)
    else:
        personalized = st.checkbox("Personalized", value=False, disabled=True)

if personalized:
    col1, col2 = st.columns([0.5, 0.5])
    with col1:
        author_id = st.text_input("Member ID", placeholder="Member ID", key="text_input_2")
        dropdown_disabled = bool(author_id.strip())

    col_left, col_right = st.columns(2)
    with col_left:
        skin_tone = st.selectbox(
            "Skin Tone",
            ["lightMedium", "light", "fairLight", "fair", "medium", "notSureST", "mediumTan",
             "tan", "rich", "olive", "deep", "porcelain", "dark", "ebony"],
            key="dropdown1",
            disabled=dropdown_disabled
        )
        skin_type = st.selectbox(
            "Skin Type",
            ["dry", "combination", "normal", "oily"],
            key="dropdown2",
            disabled=dropdown_disabled
        )
    with col_right:
        eye_color = st.selectbox(
            "Eye Color",
            ["brown", "hazel", "blue", "green", "gray", "Grey"],
            key="dropdown3",
            disabled=dropdown_disabled
        )
        hair_color = st.selectbox(
            "Hair Color",
            ["black", "brown", "blonde", "brunette", "gray", "auburn", "red"],
            key="dropdown4",
            disabled=dropdown_disabled
        )
else:
    skin_tone, skin_type, eye_color, hair_color = None, None, None, None

col1, col2 = st.columns([0.5, 0.5])
with col1:
    submit_button = st.button("Look", type="primary")

def load_data():
    product_info = pd.read_csv('processed-data/product/product_info_v2.csv', low_memory=False)
    files = [
        'processed-data/user review/part_2.csv',
        'processed-data/user review/part_1.csv',
        'processed-data/user review//part_0.csv'
    ]
    dataframes = [pd.read_csv(file, low_memory=False) for file in files]
    user_reviews = pd.concat(dataframes, ignore_index=True)

    skincare_products = product_info[product_info['primary_category'] == 'Skincare']
    unique_review_ids = user_reviews['product_id'].dropna().unique()
    matched_products = skincare_products[skincare_products['product_id'].isin(unique_review_ids)]

    matched_ids = set(matched_products['product_id'])

    product_info = product_info[
        (product_info['primary_category'] != 'Skincare') |
        ((product_info['primary_category'] == 'Skincare') & (product_info['product_id'].isin(matched_ids)))
    ]

    user_reviews = user_reviews[user_reviews['product_id'].isin(matched_ids)]

    return product_info, user_reviews

def filter_by_category(data, primary_category):
    return data[data['primary_category'].str.lower() == primary_category.lower()]

def apply_filters(data, on_sale=False, new=False, limited_edition=False):
    filtered_data = data.copy()
    if on_sale:
        filtered_data = filtered_data[filtered_data['on_sale'] == 1]
    if new:
        filtered_data = filtered_data[filtered_data['new'] == 1]
    if limited_edition:
        filtered_data = filtered_data[filtered_data['limited_edition'] == 1]
    return filtered_data

def exact_product_match(data, product_name):
    match = data[data['product_name'].str.lower() == product_name.lower()]
    return match

def ingredient_similarity(data, base_ingredients):
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(data['ingredients'])
        input_vector = vectorizer.transform([base_ingredients])
    except ValueError:  
        return pd.DataFrame()
    similarity_scores = cosine_similarity(input_vector, tfidf_matrix).flatten()
    data['ingredient_similarity'] = similarity_scores
    return data.sort_values(by='ingredient_similarity', ascending=False)

def similar_product_names(data, product_name):
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(data['product_name'])
        input_vector = vectorizer.transform([product_name])
    except ValueError:  # Handle empty vocabulary
        return pd.DataFrame()
    similarity_scores = cosine_similarity(input_vector, tfidf_matrix).flatten()
    data['similarity_score'] = similarity_scores
    return data.sort_values(by='similarity_score', ascending=False)

def filter_by_brand(data, brand_name):
    return data[data['brand_name'].str.lower() == brand_name.lower()]

def rank_by_popularity(data):
    data['popularity_score'] = data['log_loves_count'] * 0.6 + data['weighted_rating'] * 0.4
    return data.sort_values(by='popularity_score', ascending=False)

def find_similar_users(user_reviews, author_id):
    user_product_matrix = user_reviews.pivot_table(index='author_id', columns='product_id', values='rating').fillna(0)

    if author_id not in user_product_matrix.index:
        return pd.DataFrame()

    user_vector = user_product_matrix.loc[author_id].values.reshape(1, -1)
    similarity_scores = cosine_similarity(user_vector, user_product_matrix)[0]

    similarity_df = pd.DataFrame({
        'author_id': user_product_matrix.index,
        'similarity_score': similarity_scores
    }).sort_values(by='similarity_score', ascending=False)

    similar_users = similarity_df[similarity_df['author_id'] != author_id]
    return similar_users

def personalize_by_user(user_reviews, author_id, data, product_name=None, brand_name=None):
    exact_match = exact_product_match(data, product_name)

    def exclude_exact_match(df, exact_match):
        if not exact_match.empty:
            return df[df['product_id'] != exact_match.iloc[0]['product_id']]
        return df

    similar_users = find_similar_users(user_reviews, author_id)
    if similar_users.empty:
        data = similar_product_names(data, product_name)
        data = exclude_exact_match(data, exact_match)
        return rank_by_popularity(data)

    recommended_products = data[data['product_id'].isin(similar_users['author_id'])]

    if product_name:
        recommended_products = similar_product_names(recommended_products, product_name)
        recommended_products = exclude_exact_match(recommended_products, exact_match)
        return rank_by_popularity(recommended_products)

    if brand_name:
        recommended_products = filter_by_brand(recommended_products, brand_name)
        recommended_products = exclude_exact_match(recommended_products, exact_match)
        if not recommended_products.empty:
            return rank_by_popularity(recommended_products)

    recommended_products = exclude_exact_match(recommended_products, exact_match)
    return rank_by_popularity(recommended_products)

def personalize_by_characteristics(user_reviews, characteristics, data, product_name=None, brand_name=None):
    filtered_users = user_reviews.copy()
    for key, value in characteristics.items():
        if value:
            filtered_users = filtered_users[filtered_users[key] == value]

    recommended_products = data[data['product_id'].isin(filtered_users['product_id'])]

    def exclude_exact_match(df, exact_match):
        if not exact_match.empty:
            return df[df['product_id'] != exact_match.iloc[0]['product_id']]
        return df

    if product_name:
        exact_match = exact_product_match(recommended_products, product_name)
        recommended_products = exclude_exact_match(recommended_products, exact_match)
        recommended_products = similar_product_names(recommended_products, product_name)

    if brand_name:
        recommended_products = filter_by_brand(recommended_products, brand_name)
        recommended_products = exclude_exact_match(recommended_products, exact_match)

    return rank_by_popularity(recommended_products)

def recommend(data, user_reviews, product_name=None, brand_name=None, primary_category=None, filters=None, author_id=None, characteristics=None, top_n=16):
    data = filter_by_category(data, primary_category)
    data_temp = data.copy()

    if primary_category != "Skincare" and filters:
        data = apply_filters(data, **filters)
        if data.empty:
            data = data_temp

    if author_id:
        personalized = personalize_by_user(user_reviews, author_id, data, product_name, brand_name)
        if not personalized.empty:
            return personalized.head(top_n)

    if characteristics and any(characteristics.values()):
        personalized = personalize_by_characteristics(user_reviews, characteristics, data, product_name, brand_name)
        if not personalized.empty:
            return personalized.head(top_n)

    base_ingredients = None
    if product_name:
        if data.empty:
            return pd.DataFrame()

        exact_match = exact_product_match(data, product_name)
        if not exact_match.empty:
            base_ingredients = exact_match.iloc[0]['ingredients']
            data = ingredient_similarity(data, base_ingredients)

            if brand_name:
                brand_filtered = filter_by_brand(data, brand_name)
                if not brand_filtered.empty:
                    data = brand_filtered
                    return rank_by_popularity(data).head(top_n)

            return rank_by_popularity(data).head(top_n)

        data = similar_product_names(data, product_name)
        if brand_name:
            brand_filtered = filter_by_brand(data, brand_name)
            if not brand_filtered.empty:
                data = brand_filtered
                return rank_by_popularity(data).head(top_n)

        return rank_by_popularity(data).head(top_n)

    return rank_by_popularity(data).head(top_n)
product_info, user_reviews = load_data()

if submit_button:
    if not product_name.strip():
        st.markdown(
            '<div class="error-message">Product field is mandatory. Please fill it.</div>',
            unsafe_allow_html=True
        )
    else:
        filters = {
            "on_sale": "On Sale" in selected_options,
            "new": "New" in selected_options,
            "limited_edition": "Limited Edition" in selected_options
        }

        characteristics = {
            "skin_tone": skin_tone,
            "skin_type": skin_type,
            "eye_color": eye_color,
            "hair_color": hair_color
        }

        recommendations = recommend(
            data=product_info,
            user_reviews=user_reviews,
            product_name=product_name.strip(),
            brand_name=brand_name,
            primary_category=primary_category,
            filters={
                "on_sale": "On Sale" in selected_options,
                "new": "New" in selected_options,
                "limited_edition": "Limited Edition" in selected_options,
            },
            author_id=author_id.strip() if personalized else None,
            characteristics={
                "skin_tone": skin_tone if personalized else None,
                "skin_type": skin_type if personalized else None,
                "eye_color": eye_color if personalized else None,
                "hair_color": hair_color if personalized else None,
            },
            top_n=16,
        )

        if recommendations.empty:
            st.markdown('<div class="error-message">No recommendations found. Please try different inputs.</div>', unsafe_allow_html=True)
        else:
            recommendations_list = recommendations.to_dict(orient='records')

            image_directory = ".images/section-product-recommendation"
            if not os.path.exists(image_directory):
                st.error("Image directory not found. Please ensure the directory exists.")
                st.stop()
            else:
                image_files = [f for f in os.listdir(image_directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
                if not image_files:
                    st.error("No images found in the directory.")
                    st.stop()
                else:
                    with st.spinner("Searching for recommended products..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.02)
                            progress_bar.progress(i + 1)

                    max_cards = 16  
                    num_columns = 4  

                    recommendations_list = recommendations_list[:max_cards]  
                    for chunk in [recommendations_list[i:i + num_columns] for i in range(0, len(recommendations_list), num_columns)]:
                        cols = st.columns(num_columns)
                        for col, product in zip(cols, chunk):  
                            with col:
                                random_image = os.path.join(image_directory, random.choice(image_files))
                                st.image(
                                    random_image,
                                    use_container_width=True
                                )
                                st.markdown(
                                    f"""
                                    <div class="product-card">
                                        <div class="product-title">{product['product_name']}</div>
                                        <div class="product-brand">Brand: {product['brand_name']}</div>
                                        <div class="product-price">Price: ${product['price_usd']}</div>
                                        <a class="shop-button">View Product</a>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

            